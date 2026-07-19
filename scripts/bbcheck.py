#!/usr/bin/env python3
"""
bbcheck.py — Find out whether a domain has a bug bounty / vulnerability
disclosure program, using ONLY the domain as input.

Three independent, authentic sources are cross-checked:

  1. security.txt (RFC 9116)      — the domain's own self-published policy
  2. lookup.disclose.io API       — live, vendor-neutral resolver that maps
                                     ANY asset (domain, IP, package, etc.)
                                     to its official disclosure channel
  3. disclose/diodb program-list  — open-source static database (GitHub)
                                     of known bug bounty / VDP programs,
                                     used as a fallback cross-reference

No API keys, no scraping of platform login pages, no manual searching —
just point it at a domain.

Usage:
    python3 bbcheck.py example.com
    python3 bbcheck.py example.com --json
"""

import sys
import json
import argparse
import urllib.request
import urllib.error

TIMEOUT = 10
UA = "bbcheck/1.0 (+security-research; contact: none)"

DIODB_URL = "https://github.com/disclose/diodb/raw/master/program-list.json"
LOOKUP_URL = "https://lookup.disclose.io/api/lookup"


def _get(url, headers=None, data=None, method="GET"):
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("User-Agent", UA)
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()
    except Exception as e:
        return None, str(e).encode()


# ---------------------------------------------------------------------------
# 1. security.txt — the domain's own self-published disclosure policy
# ---------------------------------------------------------------------------
def check_security_txt(domain):
    paths = [
        f"https://{domain}/.well-known/security.txt",
        f"https://{domain}/security.txt",
    ]
    for url in paths:
        status, body = _get(url)
        if status == 200 and body:
            text = body.decode(errors="ignore")
            if "Contact" in text or "Policy" in text:
                fields = {}
                for line in text.splitlines():
                    line = line.strip()
                    if line.startswith("#") or ":" not in line:
                        continue
                    key, _, val = line.partition(":")
                    key = key.strip().lower()
                    val = val.strip()
                    fields.setdefault(key, []).append(val)
                return {"found": True, "source_url": url, "fields": fields}
    return {"found": False}


# ---------------------------------------------------------------------------
# 2. lookup.disclose.io — live resolver, domain in / disclosure contact out
# ---------------------------------------------------------------------------
def check_disclose_lookup(domain):
    payload = json.dumps({"input": domain}).encode()
    status, body = _get(
        LOOKUP_URL,
        headers={"Content-Type": "application/json"},
        data=payload,
        method="POST",
    )
    if status != 200:
        return {"found": False, "error": f"HTTP {status}"}
    try:
        data = json.loads(body.decode(errors="ignore"))
    except json.JSONDecodeError:
        return {"found": False, "error": "invalid JSON response"}
    return {"found": True, "raw": data}


# ---------------------------------------------------------------------------
# 3. diodb — static open-source program database (fallback cross-reference)
# ---------------------------------------------------------------------------
def check_diodb(domain):
    status, body = _get(DIODB_URL)
    if status != 200:
        return {"found": False, "error": f"HTTP {status}"}
    try:
        programs = json.loads(body.decode(errors="ignore"))
    except json.JSONDecodeError:
        return {"found": False, "error": "invalid JSON"}

    domain_l = domain.lower()
    matches = []
    for entry in programs:
        blob = json.dumps(entry).lower()
        if domain_l in blob:
            matches.append(entry)
    return {"found": bool(matches), "matches": matches}


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------
def run(domain):
    result = {
        "domain": domain,
        "security_txt": check_security_txt(domain),
        "disclose_lookup": check_disclose_lookup(domain),
        "diodb": check_diodb(domain),
    }

    # Verdict: did ANY authentic source confirm a channel?
    verdict = "no evidence found"
    confidence = "none"

    dl = result["disclose_lookup"]
    if dl.get("found") and isinstance(dl.get("raw"), dict):
        status = dl["raw"].get("status")
        contacts = dl["raw"].get("contacts", [])
        if status == "complete" or contacts:
            verdict = "disclosure channel confirmed"
            types = sorted({c.get("type") for c in contacts if c.get("type")})
            confidence = f"via disclose.io lookup ({', '.join(types) or 'unknown type'})"

    if result["security_txt"].get("found"):
        verdict = "disclosure channel confirmed"
        confidence += " + security.txt published" if confidence != "none" else "security.txt published"

    if result["diodb"].get("found"):
        verdict = "disclosure channel confirmed"
        confidence += " + listed in diodb" if confidence != "none" else "listed in diodb"

    result["verdict"] = verdict
    result["confidence_summary"] = confidence
    return result


def pretty_print(result):
    d = result["domain"]
    print(f"\n=== Bug bounty / VDP check for: {d} ===\n")

    print(f"Verdict: {result['verdict']}")
    print(f"Basis:   {result['confidence_summary']}\n")

    st = result["security_txt"]
    print("-- security.txt --")
    if st.get("found"):
        print(f"  Found at: {st['source_url']}")
        for k, v in st["fields"].items():
            print(f"  {k.capitalize()}: {', '.join(v)}")
    else:
        print("  Not published.")
    print()

    dl = result["disclose_lookup"]
    print("-- lookup.disclose.io --")
    if dl.get("found"):
        raw = dl["raw"]
        print(f"  Status: {raw.get('status')}")
        attribution = raw.get("attribution", {})
        if attribution:
            print(f"  Attributed org: {attribution.get('name', 'unknown')}")
        for c in raw.get("contacts", []):
            print(f"  - [{c.get('type')}] {c.get('value') or c.get('url')} "
                  f"(confidence: {c.get('confidence')})")
        if not raw.get("contacts"):
            print("  No contacts returned.")
    else:
        print(f"  Lookup failed: {dl.get('error')}")
    print()

    db = result["diodb"]
    print("-- diodb (open-source program database) --")
    if db.get("found"):
        for m in db["matches"]:
            name = m.get("name") or m.get("program_name") or "unknown"
            url = m.get("contact_url") or m.get("submission_url") or ""
            print(f"  - {name} {('- ' + url) if url else ''}")
    else:
        print("  No matching entry.")
    print()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("domain", help="Domain to check, e.g. example.com")
    parser.add_argument("--json", action="store_true", help="Output raw JSON instead of formatted text")
    args = parser.parse_args()

    domain = args.domain.strip().lower()
    domain = domain.replace("https://", "").replace("http://", "").split("/")[0]

    result = run(domain)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        pretty_print(result)


if __name__ == "__main__":
    main()
