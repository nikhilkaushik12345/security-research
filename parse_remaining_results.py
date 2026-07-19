#!/usr/bin/env python3
"""
Parse verbose bbcheck.py output into clean pipe-delimited format
"""

import re
from pathlib import Path

def parse_bbcheck_output(text):
    """Parse verbose bbcheck output into structured data"""
    
    # Extract domain
    domain_match = re.search(r'=== Bug bounty / VDP check for: (.+?) ===', text)
    if not domain_match:
        return None
    
    domain = domain_match.group(1).strip()
    
    # Extract verdict
    verdict_match = re.search(r'Verdict:\s*(.+?)(?:\n|$)', text)
    verdict = verdict_match.group(1).strip() if verdict_match else "UNKNOWN"
    
    # Determine if FOUND or NOT_FOUND
    if "confirmed" in verdict.lower() or "found" in verdict.lower():
        status = "FOUND"
    elif "not found" in verdict.lower() or "no matching" in verdict.lower():
        status = "NOT_FOUND"
    else:
        status = "UNKNOWN"
    
    # Extract contact email
    contact_email = ""
    email_patterns = [
        r'security@[\w\.-]+',
        r'abuse@[\w\.-]+',
        r'hostmaster@[\w\.-]+',
        r'[\w\.-]+@[\w\.-]+\.[\w]+'
    ]
    
    for pattern in email_patterns:
        match = re.search(pattern, text)
        if match:
            contact_email = match.group(0)
            break
    
    # Extract source
    if "disclose.io" in text:
        source = "disclose.io"
    elif "security.txt" in text:
        source = "security.txt"
    else:
        source = "unknown"
    
    # Extract program URL if present
    program_url = ""
    url_match = re.search(r'https?://[^\s\)]+', text)
    if url_match:
        program_url = url_match.group(0)
    
    return {
        'domain': domain,
        'verdict': status,
        'program_type': 'VDP' if status == 'FOUND' else 'NONE',
        'source': source,
        'program_url': program_url,
        'platform': 'self-hosted' if status == 'FOUND' else 'N/A',
        'contact_email': contact_email,
        'notes': verdict
    }

def main():
    input_file = '/home/code/research_remaining_results.txt'
    output_file = '/home/code/research_remaining_parsed.txt'
    
    with open(input_file, 'r') as f:
        content = f.read()
    
    # Split by domain checks
    checks = re.split(r'=== Bug bounty / VDP check for:', content)
    
    results = []
    for check in checks[1:]:  # Skip first empty split
        full_check = "=== Bug bounty / VDP check for:" + check
        parsed = parse_bbcheck_output(full_check)
        if parsed:
            results.append(parsed)
    
    # Write clean results
    with open(output_file, 'w') as f:
        f.write("domain|verdict|program_type|source_step|program_url|platform|contact_email|notes\n")
        for r in results:
            line = f"{r['domain']}|{r['verdict']}|{r['program_type']}|{r['source']}|{r['program_url']}|{r['platform']}|{r['contact_email']}|{r['notes']}"
            f.write(line + '\n')
    
    # Count results
    found = sum(1 for r in results if r['verdict'] == 'FOUND')
    not_found = sum(1 for r in results if r['verdict'] == 'NOT_FOUND')
    
    print(f"\n{'='*80}")
    print(f"✅ PARSING COMPLETE - REMAINING DOMAINS (235-533)")
    print(f"{'='*80}")
    print(f"Total Domains Parsed: {len(results)}")
    print(f"Programs Found: {found} ({found*100//len(results) if results else 0}%)")
    print(f"Not Found: {not_found} ({not_found*100//len(results) if results else 0}%)")
    print(f"\n📁 Parsed results saved to: {output_file}")
    print(f"{'='*80}\n")
    
    return results

if __name__ == '__main__':
    main()
