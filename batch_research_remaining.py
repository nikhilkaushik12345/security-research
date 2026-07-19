#!/usr/bin/env python3
"""
Batch Bug Bounty Research - Remaining Domains (235-533)
Uses authentic multi-source verification: security.txt, disclose.io, diodb
"""

import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

def run_bbcheck(domain):
    """Run bbcheck.py on a single domain"""
    try:
        result = subprocess.run(
            ['python3', '/home/code/bbcheck.py', domain],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.stdout.strip()
    except Exception as e:
        return f"{domain}|ERROR|{str(e)}"

def main():
    # Read remaining domains
    domains_file = '/home/code/remaining_domains.txt'
    output_file = '/home/code/research_remaining_results.txt'
    
    with open(domains_file, 'r') as f:
        domains = [line.strip() for line in f if line.strip()]
    
    print(f"🚀 Starting batch research on {len(domains)} remaining domains...")
    print(f"📊 Using: security.txt (RFC 9116), disclose.io API, diodb database")
    print(f"⚙️  Parallel workers: 15")
    print(f"⏱️  Estimated time: ~{len(domains) * 0.65 / 15:.1f} seconds\n")
    
    start_time = time.time()
    results = []
    completed = 0
    
    with ThreadPoolExecutor(max_workers=15) as executor:
        futures = {executor.submit(run_bbcheck, domain): domain for domain in domains}
        
        for future in as_completed(futures):
            completed += 1
            result = future.result()
            results.append(result)
            
            # Progress indicator
            if completed % 25 == 0:
                elapsed = time.time() - start_time
                rate = completed / elapsed
                remaining = (len(domains) - completed) / rate if rate > 0 else 0
                print(f"✓ {completed}/{len(domains)} domains ({completed*100//len(domains)}%) - "
                      f"ETA: {remaining:.1f}s")
    
    # Write results
    with open(output_file, 'w') as f:
        f.write("domain|verdict|program_type|source_step|program_url|platform|contact_email|notes\n")
        for result in results:
            f.write(result + '\n')
    
    elapsed = time.time() - start_time
    
    # Count results
    found = sum(1 for r in results if '|FOUND|' in r)
    not_found = sum(1 for r in results if '|NOT_FOUND|' in r)
    
    print(f"\n{'='*80}")
    print(f"✅ BATCH RESEARCH COMPLETE")
    print(f"{'='*80}")
    print(f"Total Domains: {len(domains)}")
    print(f"Programs Found: {found} ({found*100//len(domains)}%)")
    print(f"Not Found: {not_found} ({not_found*100//len(domains)}%)")
    print(f"Research Time: {elapsed:.1f} seconds")
    print(f"Average per Domain: {elapsed/len(domains):.2f} seconds")
    print(f"Domains per Second: {len(domains)/elapsed:.2f}")
    print(f"\n📁 Results saved to: {output_file}")
    print(f"{'='*80}\n")

if __name__ == '__main__':
    main()
