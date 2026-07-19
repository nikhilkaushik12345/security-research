#!/usr/bin/env python3
"""
Efficient Bug Bounty Research - Multiple Methods
Focuses on quick detection without long timeouts
"""

import subprocess
import json
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

class EfficientResearcher:
    def __init__(self):
        self.security_paths = [
            '/.well-known/security.txt',
            '/security.txt',
            '/security',
            '/bug-bounty',
            '/bugbounty',
            '/responsible-disclosure',
            '/vulnerability-disclosure',
        ]

    def curl_check(self, url, timeout=5):
        """Quick curl check with timeout"""
        try:
            result = subprocess.run(
                ['curl', '-s', '-m', str(timeout), '-L', url],
                capture_output=True,
                text=True,
                timeout=timeout+1
            )
            return result.stdout if result.returncode == 0 else None
        except:
            return None

    def check_security_txt(self, domain):
        """Check security.txt"""
        for path in ['/.well-known/security.txt', '/security.txt']:
            url = f'https://{domain}{path}'
            content = self.curl_check(url, timeout=3)
            if content and 'Contact:' in content:
                contact = re.search(r'Contact:\s*([^\n]+)', content)
                return {
                    'found': True,
                    'source': 'security.txt',
                    'contact': contact.group(1).strip() if contact else None,
                    'url': url
                }
        return None

    def check_security_pages(self, domain):
        """Check common security pages"""
        for path in self.security_paths:
            url = f'https://{domain}{path}'
            content = self.curl_check(url, timeout=3)
            if content:
                text_lower = content.lower()
                indicators = ['bug bounty', 'vulnerability disclosure', 'hackerone', 'bugcrowd', 'intigriti']
                if any(ind in text_lower for ind in indicators):
                    emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', content)
                    platform = 'self-hosted'
                    if 'hackerone' in text_lower:
                        platform = 'hackerone'
                    elif 'bugcrowd' in text_lower:
                        platform = 'bugcrowd'
                    
                    return {
                        'found': True,
                        'source': 'security_page',
                        'path': path,
                        'platform': platform,
                        'emails': list(set(emails)),
                        'url': url
                    }
        return None

    def research_domain(self, domain):
        """Research single domain"""
        result = {
            'domain': domain,
            'verdict': 'NOT_FOUND',
            'program_type': 'N/A',
            'source_step': 'none',
            'program_url': '',
            'platform': '',
            'contact_email': '',
            'notes': ''
        }
        
        # Check security.txt
        sec_txt = self.check_security_txt(domain)
        if sec_txt:
            result['verdict'] = 'FOUND'
            result['source_step'] = 'security.txt'
            result['program_url'] = sec_txt['url']
            result['contact_email'] = sec_txt.get('contact', '')
            result['notes'] = 'Found via security.txt'
            return result
        
        # Check security pages
        sec_page = self.check_security_pages(domain)
        if sec_page:
            result['verdict'] = 'FOUND'
            result['source_step'] = 'security_page'
            result['program_url'] = sec_page['url']
            result['platform'] = sec_page.get('platform', '')
            if sec_page.get('emails'):
                result['contact_email'] = sec_page['emails'][0]
            result['notes'] = f"Found at {sec_page['path']}"
            return result
        
        return result

def main():
    # Read domains
    with open('/home/code/new_domains.txt', 'r') as f:
        domains = [line.strip() for line in f if line.strip()]
    
    print(f"[*] Starting efficient research on {len(domains)} domains...")
    print(f"[*] Using 15 parallel workers with 3-5 second timeouts")
    print()
    
    researcher = EfficientResearcher()
    results = []
    found_count = 0
    
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=15) as executor:
        futures = {executor.submit(researcher.research_domain, d): d for d in domains}
        
        completed = 0
        for future in as_completed(futures):
            completed += 1
            result = future.result()
            results.append(result)
            
            if result['verdict'] == 'FOUND':
                found_count += 1
                print(f"[+] FOUND: {result['domain']} | {result['platform']} | {result['contact_email']}")
            
            if completed % 25 == 0:
                elapsed = time.time() - start_time
                rate = completed / elapsed
                print(f"[*] Progress: {completed}/{len(domains)} ({rate:.1f}/sec)")
    
    # Save results
    with open('/home/code/research_advanced_results.txt', 'w') as f:
        f.write("domain|verdict|program_type|source_step|program_url|platform|contact_email|notes\n")
        for result in results:
            line = f"{result['domain']}|{result['verdict']}|{result['program_type']}|{result['source_step']}|{result['program_url']}|{result['platform']}|{result['contact_email']}|{result['notes']}\n"
            f.write(line)
    
    elapsed = time.time() - start_time
    print()
    print("=" * 80)
    print(f"[✓] Research complete in {elapsed:.1f} seconds!")
    print(f"[✓] FOUND: {found_count} programs")
    print(f"[✗] NOT_FOUND: {len(domains) - found_count}")
    print(f"[✓] Results saved to /home/code/research_advanced_results.txt")
    print("=" * 80)

if __name__ == '__main__':
    main()
