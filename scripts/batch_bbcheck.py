#!/usr/bin/env python3
"""
Batch research using bbcheck.py on all 234 domains
Parallel processing with proper result aggregation
"""

import subprocess
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def run_bbcheck(domain):
    """Run bbcheck on a single domain and return structured result"""
    try:
        result = subprocess.run(
            ['python3', '/home/code/bbcheck.py', domain, '--json'],
            capture_output=True,
            text=True,
            timeout=15
        )
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return domain, data
        else:
            return domain, {"error": "bbcheck failed"}
    except subprocess.TimeoutExpired:
        return domain, {"error": "timeout"}
    except Exception as e:
        return domain, {"error": str(e)}

def parse_result(domain, data):
    """Convert bbcheck result to pipe-delimited format"""
    if "error" in data:
        return f"{domain}|NOT_FOUND|N/A|none||||Error: {data['error']}"
    
    verdict = data.get("verdict", "no evidence found")
    confidence = data.get("confidence_summary", "none")
    
    # Determine if FOUND
    is_found = "confirmed" in verdict.lower()
    
    program_type = "N/A"
    source_step = "none"
    program_url = ""
    platform = ""
    contact_email = ""
    notes = confidence
    
    # Check security.txt
    st = data.get("security_txt", {})
    if st.get("found"):
        is_found = True
        source_step = "security.txt"
        program_url = st.get("source_url", "")
        fields = st.get("fields", {})
        if "contact" in fields:
            contact_email = fields["contact"][0] if fields["contact"] else ""
        notes = f"security.txt: {', '.join(fields.keys())}"
    
    # Check disclose.io lookup
    dl = data.get("disclose_lookup", {})
    if dl.get("found"):
        is_found = True
        if not source_step or source_step == "none":
            source_step = "disclose_lookup"
        raw = dl.get("raw", {})
        contacts = raw.get("contacts", [])
        if contacts:
            contact = contacts[0]
            contact_email = contact.get("value") or contact.get("url") or ""
            contact_type = contact.get("type", "unknown")
            if not notes or notes == "none":
                notes = f"disclose.io: {contact_type}"
    
    # Check diodb
    db = data.get("diodb", {})
    if db.get("found"):
        is_found = True
        matches = db.get("matches", [])
        if matches:
            match = matches[0]
            if not source_step or source_step == "none":
                source_step = "diodb"
            program_url = match.get("contact_url") or match.get("submission_url") or ""
            if not notes or notes == "none":
                notes = f"diodb: {match.get('name', 'unknown')}"
    
    verdict_str = "FOUND" if is_found else "NOT_FOUND"
    
    return f"{domain}|{verdict_str}|{program_type}|{source_step}|{program_url}|{platform}|{contact_email}|{notes}"

def main():
    # Read domains
    with open('/home/code/new_domains.txt', 'r') as f:
        domains = [line.strip() for line in f if line.strip()]
    
    print(f"[*] Starting batch research on {len(domains)} domains")
    print(f"[*] Using 10 parallel workers (disclose.io API rate limits)")
    print(f"[*] Timeout: 15 seconds per domain")
    print()
    
    results = []
    found_count = 0
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(run_bbcheck, domain): domain for domain in domains}
        
        completed = 0
        for future in as_completed(futures):
            completed += 1
            domain, data = future.result()
            
            # Parse and format result
            line = parse_result(domain, data)
            results.append(line)
            
            # Check if found
            if "|FOUND|" in line:
                found_count += 1
                # Extract contact info for display
                parts = line.split('|')
                contact = parts[6] if len(parts) > 6 else ""
                print(f"[+] {completed:3d}. FOUND: {domain:30s} | {contact}")
            else:
                if completed % 20 == 0:
                    print(f"[*] Progress: {completed}/{len(domains)}")
    
    # Save results
    with open('/home/code/research_advanced_results.txt', 'w') as f:
        f.write("domain|verdict|program_type|source_step|program_url|platform|contact_email|notes\n")
        for line in results:
            f.write(line + '\n')
    
    elapsed = time.time() - start_time
    
    print()
    print("=" * 80)
    print(f"[✓] Research complete in {elapsed:.1f} seconds!")
    print(f"[✓] FOUND: {found_count}/{len(domains)} ({100*found_count/len(domains):.1f}%)")
    print(f"[✓] Results saved to /home/code/research_advanced_results.txt")
    print("=" * 80)

if __name__ == '__main__':
    main()
