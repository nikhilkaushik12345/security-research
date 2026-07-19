#!/usr/bin/env python3
"""
Enhanced Bug Bounty Research Script - Extract ALL details from security pages
"""

import urllib.request
import urllib.error
import time
import concurrent.futures
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Read domains from file
with open('/home/code/new_domains.txt', 'r') as f:
    DOMAINS = [line.strip() for line in f if line.strip()]

print(f"Total domains to research: {len(DOMAINS)}")

def fetch_url(url, timeout=6):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 SecurityResearch'})
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            content = resp.read(16384).decode('utf-8', errors='ignore')
            return resp.status, content
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception:
        return 0, ""

def extract_emails(text):
    """Extract all email addresses from text"""
    emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    return list(set(emails))

def extract_contact_info(text):
    """Extract contact information"""
    info = {
        'emails': extract_emails(text),
        'phone': re.findall(r'\+?[\d\s\-\(\)]{10,}', text)[:3],  # First 3 phone numbers
        'urls': re.findall(r'https?://[^\s\'"<>]+', text)[:10],  # First 10 URLs
    }
    return info

def extract_program_details(text):
    """Extract program details from text"""
    details = {
        'has_bounty': False,
        'has_vdp': False,
        'has_paid': False,
        'platforms': [],
        'reward_mentioned': False,
        'scope': '',
    }
    
    text_lower = text.lower()
    
    # Check for program types
    if any(k in text_lower for k in ['bug bounty', 'bounty program', 'reward']):
        details['has_bounty'] = True
    if any(k in text_lower for k in ['vulnerability disclosure', 'vdp', 'responsible disclosure']):
        details['has_vdp'] = True
    if any(k in text_lower for k in ['paid', 'reward', 'compensation', 'bounty']):
        details['has_paid'] = True
    
    # Detect platforms
    if 'hackerone' in text_lower:
        details['platforms'].append('hackerone')
    if 'bugcrowd' in text_lower:
        details['platforms'].append('bugcrowd')
    if 'intigriti' in text_lower:
        details['platforms'].append('intigriti')
    if 'yeswehack' in text_lower:
        details['platforms'].append('yeswehack')
    if 'synack' in text_lower:
        details['platforms'].append('synack')
    if 'cobalt' in text_lower:
        details['platforms'].append('cobalt')
    
    # Extract scope if mentioned
    scope_match = re.search(r'scope[:\s]+([^.\n]+)', text_lower)
    if scope_match:
        details['scope'] = scope_match.group(1).strip()[:100]
    
    return details

def research_domain(domain):
    result = {
        'domain': domain,
        'verdict': 'NOT_FOUND',
        'program_type': 'N/A',
        'source_step': 'not_found',
        'program_url': '',
        'platform': '',
        'contact_email': '',
        'security_email': '',
        'notes': ''
    }

    # Step 1: Check security.txt
    for path in [f'https://{domain}/.well-known/security.txt', f'https://{domain}/security.txt']:
        status, content = fetch_url(path)
        if status == 200 and content and len(content) > 20:
            contact_info = extract_contact_info(content)
            prog_details = extract_program_details(content)
            
            if prog_details['has_bounty'] or prog_details['has_vdp']:
                result['verdict'] = 'FOUND'
                result['source_step'] = 'security.txt'
                result['program_type'] = 'PAID_BOUNTY' if prog_details['has_paid'] else 'VDP_ONLY'
                result['platform'] = ', '.join(prog_details['platforms']) if prog_details['platforms'] else 'self-hosted'
                
                # Extract contact email from security.txt
                if contact_info['emails']:
                    result['contact_email'] = contact_info['emails'][0]
                
                # Extract program URL
                urls = re.findall(r'https?://(?:hackerone|bugcrowd|intigriti|yeswehack|synack|cobalt)[^\s\'"<>]*', content)
                if urls:
                    result['program_url'] = urls[0]
                
                result['notes'] = f'security.txt found | emails: {len(contact_info["emails"])}'
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
        f'https://{domain}/.well-known/security',
    ]
    
    for path in security_paths:
        status, content = fetch_url(path)
        if status == 200 and content and len(content) > 100:
            contact_info = extract_contact_info(content)
            prog_details = extract_program_details(content)
            
            if prog_details['has_bounty'] or prog_details['has_vdp']:
                result['verdict'] = 'FOUND'
                result['source_step'] = 'security_page'
                result['program_type'] = 'PAID_BOUNTY' if prog_details['has_paid'] else 'VDP_ONLY'
                result['platform'] = ', '.join(prog_details['platforms']) if prog_details['platforms'] else 'self-hosted'
                result['program_url'] = path
                
                # Extract emails
                if contact_info['emails']:
                    result['contact_email'] = contact_info['emails'][0]
                    if len(contact_info['emails']) > 1:
                        result['security_email'] = contact_info['emails'][1]
                
                result['notes'] = f'Found at {path.split("/")[-1]} | emails: {len(contact_info["emails"])}'
                return result

    result['notes'] = 'No program found after full check'
    return result

def main():
    print("domain|verdict|program_type|source_step|program_url|platform|contact_email|security_email|notes")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=25) as executor:
        futures = {executor.submit(research_domain, d): d for d in DOMAINS}
        for future in concurrent.futures.as_completed(futures):
            r = future.result()
            print(f"{r['domain']}|{r['verdict']}|{r['program_type']}|{r['source_step']}|{r['program_url']}|{r['platform']}|{r['contact_email']}|{r['security_email']}|{r['notes']}")

if __name__ == '__main__':
    main()
