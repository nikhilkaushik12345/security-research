#!/usr/bin/env python3
"""
Bug Bounty Research Script - 5-Step Process
Running on NEW domains (known to have programs)
"""

import urllib.request
import urllib.error
import time
import concurrent.futures
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Read new domains from file
with open('/home/code/new_domains.txt', 'r') as f:
    DOMAINS = [line.strip() for line in f if line.strip()]

print(f"Total domains to research: {len(DOMAINS)}")

def fetch_url(url, timeout=6):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 SecurityResearch'})
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            content = resp.read(8192).decode('utf-8', errors='ignore')
            return resp.status, content
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception:
        return 0, ""

BOUNTY_KEYWORDS = [
    'bug bounty', 'vulnerability disclosure', 'responsible disclosure',
    'security.txt', 'hackerone.com', 'bugcrowd.com', 'intigriti.com',
    'yeswehack.com', 'synack.com', 'cobalt.io', 'report a vulnerability',
    'report vulnerability', 'security report', 'hall of fame', 'security researcher',
    'bounty program', 'vdp', 'cvd', 'coordinated vulnerability'
]

PAID_KEYWORDS = [
    'bug bounty', 'bounty program', 'reward', 'paid', 'compensation',
    'hackerone.com', 'bugcrowd.com', 'intigriti.com', 'yeswehack.com',
    'synack.com', 'cobalt.io'
]

VDP_KEYWORDS = [
    'vulnerability disclosure', 'responsible disclosure', 'vdp',
    'coordinated vulnerability', 'report a vulnerability', 'no reward',
    'no monetary', 'hall of fame', 'acknowledgement', 'cvd'
]

def detect_platform(text):
    text_lower = text.lower()
    if 'hackerone.com' in text_lower: return 'hackerone'
    if 'bugcrowd.com' in text_lower: return 'bugcrowd'
    if 'intigriti.com' in text_lower: return 'intigriti'
    if 'yeswehack.com' in text_lower: return 'yeswehack'
    if 'synack.com' in text_lower: return 'synack'
    if 'cobalt.io' in text_lower: return 'cobalt'
    return 'self-hosted'

def extract_program_url(text, domain):
    import re
    patterns = [
        r'(https?://hackerone\.com/[^\s\'"<>]+)',
        r'(https?://bugcrowd\.com/[^\s\'"<>]+)',
        r'(https?://intigriti\.com/[^\s\'"<>]+)',
        r'(https?://app\.intigriti\.com/[^\s\'"<>]+)',
        r'(https?://yeswehack\.com/[^\s\'"<>]+)',
        r'(https?://synack\.com/[^\s\'"<>]+)',
        r'(https?://cobalt\.io/[^\s\'"<>]+)',
    ]
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            return m.group(1).rstrip('.,;)')
    return ''

def classify_text(text):
    text_lower = text.lower()
    has_bounty = any(k in text_lower for k in BOUNTY_KEYWORDS)
    if not has_bounty:
        return None, None, None
    is_paid = any(k in text_lower for k in PAID_KEYWORDS)
    is_vdp = any(k in text_lower for k in VDP_KEYWORDS)
    if is_paid:
        prog_type = 'PAID_BOUNTY'
    elif is_vdp:
        prog_type = 'VDP_ONLY'
    else:
        prog_type = 'VDP_ONLY'
    platform = detect_platform(text)
    url = extract_program_url(text, '')
    return prog_type, platform, url

def research_domain(domain):
    result = {
        'domain': domain,
        'verdict': 'NOT_FOUND',
        'program_type': 'N/A',
        'source_step': 'not_found',
        'program_url': '',
        'platform': '',
        'notes': ''
    }

    # Step 1: Check security.txt
    for path in [f'https://{domain}/.well-known/security.txt', f'https://{domain}/security.txt']:
        status, content = fetch_url(path)
        if status == 200 and content and len(content) > 20:
            cl = content.lower()
            if any(k in cl for k in ['contact:', 'policy:', 'hiring:', 'acknowledgments:', 'canonical:']):
                prog_type, platform, prog_url = classify_text(content)
                if prog_type:
                    result['verdict'] = 'FOUND'
                    result['program_type'] = prog_type
                    result['source_step'] = 'security.txt'
                    result['program_url'] = prog_url
                    result['platform'] = platform
                    result['notes'] = f'security.txt found'
                    return result
                else:
                    import re
                    contact = re.search(r'Contact:\s*(https?://[^\s]+)', content, re.IGNORECASE)
                    if contact:
                        contact_url = contact.group(1)
                        if any(p in contact_url for p in ['hackerone','bugcrowd','intigriti','yeswehack','synack','cobalt']):
                            result['verdict'] = 'FOUND'
                            result['program_type'] = 'PAID_BOUNTY'
                            result['source_step'] = 'security.txt'
                            result['program_url'] = contact_url
                            result['platform'] = detect_platform(contact_url)
                            result['notes'] = f'security.txt contact points to bounty platform'
                            return result
                break

    # Step 2: Check security pages
    security_paths = [
        f'https://{domain}/security',
        f'https://{domain}/security.html',
        f'https://{domain}/responsible-disclosure',
        f'https://{domain}/vulnerability-disclosure',
        f'https://{domain}/bug-bounty',
        f'https://{domain}/bugbounty',
        f'https://{domain}/disclosure',
    ]
    for path in security_paths:
        status, content = fetch_url(path)
        if status == 200 and content and len(content) > 100:
            prog_type, platform, prog_url = classify_text(content)
            if prog_type:
                result['verdict'] = 'FOUND'
                result['program_type'] = prog_type
                result['source_step'] = 'security_page'
                result['program_url'] = prog_url if prog_url else path
                result['platform'] = platform
                result['notes'] = f'Found at security page'
                return result

    # Step 5: Final verdict
    result['notes'] = 'No program found after full 5-step check'
    return result

def main():
    print("domain|verdict|program_type|source_step|program_url|platform|notes")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=25) as executor:
        futures = {executor.submit(research_domain, d): d for d in DOMAINS}
        for future in concurrent.futures.as_completed(futures):
            r = future.result()
            print(f"{r['domain']}|{r['verdict']}|{r['program_type']}|{r['source_step']}|{r['program_url']}|{r['platform']}|{r['notes']}")

if __name__ == '__main__':
    main()
