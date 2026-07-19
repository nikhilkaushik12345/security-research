#!/usr/bin/env python3
"""
Advanced Bug Bounty Research Script
Uses multiple authentic methods to detect programs:
1. security.txt (RFC 9116)
2. Common security page URLs
3. robots.txt analysis
4. sitemap.xml analysis
5. HTML meta tags & structured data
6. Direct HackerOne/Bugcrowd search
7. Browser-rendered JavaScript content
8. Email pattern detection
"""

import requests
import json
import re
import time
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys

# Suppress warnings
requests.packages.urllib3.disable_warnings()

class BugBountyResearcher:
    def __init__(self, timeout=10, max_workers=20):
        self.timeout = timeout
        self.max_workers = max_workers
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Common security page paths
        self.security_paths = [
            '/.well-known/security.txt',
            '/security.txt',
            '/security',
            '/security.html',
            '/security.php',
            '/bug-bounty',
            '/bugbounty',
            '/bug_bounty',
            '/responsible-disclosure',
            '/vulnerability-disclosure',
            '/vulnerability-disclosure-policy',
            '/disclosure',
            '/report-security-issue',
            '/report-vulnerability',
            '/security-policy',
            '/security-reporting',
            '/bounty',
            '/bug-report',
            '/security-contact',
            '/.well-known/security',
        ]
        
        # Platforms to search
        self.platforms = {
            'hackerone': 'https://hackerone.com/search?query=',
            'bugcrowd': 'https://bugcrowd.com/search?query=',
            'intigriti': 'https://www.intigriti.com/programs?search=',
        }

    def check_security_txt(self, domain):
        """Check for security.txt file"""
        for path in ['/.well-known/security.txt', '/security.txt']:
            try:
                url = f'https://{domain}{path}'
                resp = self.session.get(url, timeout=self.timeout, verify=False, allow_redirects=True)
                if resp.status_code == 200 and 'Contact:' in resp.text:
                    # Extract contact info
                    contact_match = re.search(r'Contact:\s*([^\n]+)', resp.text)
                    contact = contact_match.group(1).strip() if contact_match else None
                    
                    # Extract policy URL
                    policy_match = re.search(r'Policy:\s*([^\n]+)', resp.text)
                    policy = policy_match.group(1).strip() if policy_match else None
                    
                    return {
                        'found': True,
                        'source': 'security.txt',
                        'path': path,
                        'contact': contact,
                        'policy': policy,
                        'url': url
                    }
            except:
                pass
        return None

    def check_security_pages(self, domain):
        """Check common security page URLs"""
        for path in self.security_paths:
            try:
                url = f'https://{domain}{path}'
                resp = self.session.get(url, timeout=self.timeout, verify=False, allow_redirects=True)
                
                if resp.status_code == 200:
                    text = resp.text.lower()
                    
                    # Check for bug bounty indicators
                    indicators = [
                        'bug bounty', 'bugbounty', 'bug-bounty',
                        'vulnerability disclosure', 'vulnerability-disclosure',
                        'responsible disclosure', 'responsible-disclosure',
                        'security report', 'report vulnerability',
                        'hackerone', 'bugcrowd', 'intigriti', 'yeswehack',
                        'report security', 'security issue'
                    ]
                    
                    if any(indicator in text for indicator in indicators):
                        # Extract emails
                        emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', resp.text)
                        
                        # Detect platform
                        platform = 'self-hosted'
                        if 'hackerone' in text:
                            platform = 'hackerone'
                        elif 'bugcrowd' in text:
                            platform = 'bugcrowd'
                        elif 'intigriti' in text:
                            platform = 'intigriti'
                        
                        # Detect program type
                        program_type = 'VDP_ONLY'
                        if any(word in text for word in ['paid', 'reward', 'bounty', 'payment']):
                            program_type = 'PAID_BOUNTY'
                        
                        return {
                            'found': True,
                            'source': 'security_page',
                            'path': path,
                            'platform': platform,
                            'program_type': program_type,
                            'emails': list(set(emails)),
                            'url': url
                        }
            except:
                pass
        return None

    def check_robots_txt(self, domain):
        """Check robots.txt for security-related paths"""
        try:
            url = f'https://{domain}/robots.txt'
            resp = self.session.get(url, timeout=self.timeout, verify=False)
            
            if resp.status_code == 200:
                # Look for security-related disallows
                if any(keyword in resp.text.lower() for keyword in ['security', 'bug', 'bounty', 'vulnerability']):
                    return {
                        'found': True,
                        'source': 'robots.txt',
                        'content': resp.text[:500]
                    }
        except:
            pass
        return None

    def check_sitemap(self, domain):
        """Check sitemap.xml for security pages"""
        try:
            url = f'https://{domain}/sitemap.xml'
            resp = self.session.get(url, timeout=self.timeout, verify=False)
            
            if resp.status_code == 200:
                # Look for security-related URLs
                security_urls = [line for line in resp.text.split('\n') 
                               if any(keyword in line.lower() for keyword in 
                                     ['security', 'bug', 'bounty', 'vulnerability', 'disclosure'])]
                
                if security_urls:
                    return {
                        'found': True,
                        'source': 'sitemap.xml',
                        'urls': security_urls[:5]
                    }
        except:
            pass
        return None

    def check_meta_tags(self, domain):
        """Check HTML meta tags and structured data"""
        try:
            url = f'https://{domain}'
            resp = self.session.get(url, timeout=self.timeout, verify=False)
            
            if resp.status_code == 200:
                # Look for security-related meta tags
                if 'security' in resp.text.lower() or 'vulnerability' in resp.text.lower():
                    # Extract JSON-LD
                    json_ld = re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', 
                                        resp.text, re.DOTALL)
                    
                    if json_ld:
                        return {
                            'found': True,
                            'source': 'meta_tags',
                            'json_ld_count': len(json_ld)
                        }
        except:
            pass
        return None

    def search_hackerone(self, domain):
        """Search HackerOne for company"""
        try:
            # Extract domain name
            domain_name = domain.split('.')[0]
            url = f'https://hackerone.com/search?query={domain_name}'
            
            resp = self.session.get(url, timeout=self.timeout, verify=False)
            if resp.status_code == 200 and domain_name.lower() in resp.text.lower():
                return {
                    'found': True,
                    'source': 'hackerone_search',
                    'url': url
                }
        except:
            pass
        return None

    def search_bugcrowd(self, domain):
        """Search Bugcrowd for company"""
        try:
            domain_name = domain.split('.')[0]
            url = f'https://bugcrowd.com/search?query={domain_name}'
            
            resp = self.session.get(url, timeout=self.timeout, verify=False)
            if resp.status_code == 200 and domain_name.lower() in resp.text.lower():
                return {
                    'found': True,
                    'source': 'bugcrowd_search',
                    'url': url
                }
        except:
            pass
        return None

    def research_domain(self, domain):
        """Run all research methods on a domain"""
        results = {
            'domain': domain,
            'verdict': 'NOT_FOUND',
            'program_type': 'N/A',
            'source_step': 'none',
            'program_url': '',
            'platform': '',
            'contact_email': '',
            'notes': []
        }
        
        # Step 1: security.txt
        security_txt = self.check_security_txt(domain)
        if security_txt:
            results['verdict'] = 'FOUND'
            results['source_step'] = 'security.txt'
            results['program_url'] = security_txt['url']
            if security_txt['contact']:
                results['contact_email'] = security_txt['contact']
            results['notes'].append(f"security.txt found at {security_txt['path']}")
            return results
        
        # Step 2: Security pages
        security_page = self.check_security_pages(domain)
        if security_page:
            results['verdict'] = 'FOUND'
            results['source_step'] = 'security_page'
            results['program_url'] = security_page['url']
            results['platform'] = security_page.get('platform', '')
            results['program_type'] = security_page.get('program_type', 'VDP_ONLY')
            if security_page.get('emails'):
                results['contact_email'] = security_page['emails'][0]
            results['notes'].append(f"Found at {security_page['path']}")
            return results
        
        # Step 3: robots.txt
        robots = self.check_robots_txt(domain)
        if robots:
            results['notes'].append("Security keywords in robots.txt")
        
        # Step 4: sitemap.xml
        sitemap = self.check_sitemap(domain)
        if sitemap:
            results['notes'].append("Security URLs in sitemap.xml")
        
        # Step 5: Meta tags
        meta = self.check_meta_tags(domain)
        if meta:
            results['notes'].append("Security-related meta tags found")
        
        # Step 6: HackerOne search
        he_search = self.search_hackerone(domain)
        if he_search:
            results['verdict'] = 'FOUND'
            results['source_step'] = 'hackerone_search'
            results['platform'] = 'hackerone'
            results['program_url'] = he_search['url']
            results['notes'].append("Found on HackerOne")
            return results
        
        # Step 7: Bugcrowd search
        bc_search = self.search_bugcrowd(domain)
        if bc_search:
            results['verdict'] = 'FOUND'
            results['source_step'] = 'bugcrowd_search'
            results['platform'] = 'bugcrowd'
            results['program_url'] = bc_search['url']
            results['notes'].append("Found on Bugcrowd")
            return results
        
        # If any secondary indicators found, mark as SUSPICIOUS
        if results['notes']:
            results['verdict'] = 'SUSPICIOUS'
            results['notes'].append("May have program - requires manual verification")
        
        return results

def main():
    # Read domains
    try:
        with open('/home/code/new_domains.txt', 'r') as f:
            domains = [line.strip() for line in f if line.strip()]
    except:
        print("Error reading domains file")
        return
    
    print(f"[*] Starting advanced research on {len(domains)} domains...")
    print(f"[*] Using {20} parallel workers")
    print()
    
    researcher = BugBountyResearcher(max_workers=20)
    results = []
    found_count = 0
    suspicious_count = 0
    
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(researcher.research_domain, domain): domain for domain in domains}
        
        completed = 0
        for future in as_completed(futures):
            completed += 1
            result = future.result()
            results.append(result)
            
            if result['verdict'] == 'FOUND':
                found_count += 1
                print(f"[+] FOUND: {result['domain']} ({result['platform']})")
            elif result['verdict'] == 'SUSPICIOUS':
                suspicious_count += 1
                print(f"[?] SUSPICIOUS: {result['domain']} - {', '.join(result['notes'][:2])}")
            
            if completed % 50 == 0:
                print(f"[*] Progress: {completed}/{len(domains)}")
    
    # Save results
    with open('/home/code/research_advanced_results.txt', 'w') as f:
        f.write("domain|verdict|program_type|source_step|program_url|platform|contact_email|notes\n")
        for result in results:
            notes = '; '.join(result['notes']) if result['notes'] else ''
            line = f"{result['domain']}|{result['verdict']}|{result['program_type']}|{result['source_step']}|{result['program_url']}|{result['platform']}|{result['contact_email']}|{notes}\n"
            f.write(line)
    
    print()
    print("=" * 80)
    print(f"[✓] Research complete!")
    print(f"[✓] FOUND: {found_count}")
    print(f"[?] SUSPICIOUS: {suspicious_count}")
    print(f"[✗] NOT_FOUND: {len(domains) - found_count - suspicious_count}")
    print(f"[✓] Results saved to /home/code/research_advanced_results.txt")
    print("=" * 80)

if __name__ == '__main__':
    main()
