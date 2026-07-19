#!/usr/bin/env python3
import subprocess
import sys

domains = []
with open('/home/code/new_domains.txt', 'r') as f:
    domains = [line.strip() for line in f if line.strip()]

print(f"[*] Processing {len(domains)} domains...")
print(f"[*] Using curl with 3-second timeout per domain")
print()

results = []
found = 0

for i, domain in enumerate(domains, 1):
    # Quick security.txt check
    try:
        result = subprocess.run(
            ['curl', '-s', '-m', '3', '-L', f'https://{domain}/.well-known/security.txt'],
            capture_output=True,
            text=True,
            timeout=4
        )
        
        if result.returncode == 0 and 'Contact:' in result.stdout:
            contact = ''
            for line in result.stdout.split('\n'):
                if line.startswith('Contact:'):
                    contact = line.replace('Contact:', '').strip().split()[0]
                    break
            
            results.append(f"{domain}|FOUND|N/A|security.txt|https://{domain}/.well-known/security.txt||{contact}|Found via security.txt")
            found += 1
            print(f"[+] {i:3d}. FOUND: {domain} ({contact})")
            continue
    except:
        pass
    
    # Quick security page check
    try:
        result = subprocess.run(
            ['curl', '-s', '-m', '3', '-L', f'https://{domain}/security'],
            capture_output=True,
            text=True,
            timeout=4
        )
        
        if result.returncode == 0 and any(x in result.stdout.lower() for x in ['bug bounty', 'vulnerability', 'hackerone', 'bugcrowd']):
            results.append(f"{domain}|FOUND|N/A|security_page|https://{domain}/security||Found at /security")
            found += 1
            print(f"[+] {i:3d}. FOUND: {domain} (security page)")
            continue
    except:
        pass
    
    results.append(f"{domain}|NOT_FOUND|N/A|none||||")
    
    if i % 25 == 0:
        print(f"[*] Progress: {i}/{len(domains)}")

# Save results
with open('/home/code/research_advanced_results.txt', 'w') as f:
    f.write("domain|verdict|program_type|source_step|program_url|platform|contact_email|notes\n")
    for r in results:
        f.write(r + '\n')

print()
print("=" * 80)
print(f"[✓] Complete! Found: {found}/{len(domains)}")
print(f"[✓] Results saved to research_advanced_results.txt")
print("=" * 80)
