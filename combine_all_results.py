#!/usr/bin/env python3
"""
Combine results from first 234 domains + remaining 299 domains
Create comprehensive summary for all 533 domains
"""

import csv
from pathlib import Path
from collections import defaultdict

def read_results(filename):
    """Read pipe-delimited results"""
    results = []
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
            for line in lines[1:]:  # Skip header
                if line.strip() and '|' in line:
                    parts = line.strip().split('|')
                    if len(parts) >= 8:
                        results.append({
                            'domain': parts[0],
                            'verdict': parts[1],
                            'program_type': parts[2],
                            'source': parts[3],
                            'program_url': parts[4],
                            'platform': parts[5],
                            'contact_email': parts[6],
                            'notes': parts[7] if len(parts) > 7 else ''
                        })
    except Exception as e:
        print(f"Error reading {filename}: {e}")
    return results

def main():
    print(f"\n{'='*80}")
    print(f"🔄 COMBINING RESULTS FROM ALL 533 DOMAINS")
    print(f"{'='*80}\n")
    
    # Read first batch (234 domains)
    print("📖 Reading first batch (234 domains)...")
    first_batch = read_results('/home/code/research_advanced_results.txt')
    print(f"   ✓ Found {len(first_batch)} results")
    
    # Read remaining batch (299 domains)
    print("📖 Reading remaining batch (299 domains)...")
    remaining_batch = read_results('/home/code/research_remaining_parsed.txt')
    print(f"   ✓ Found {len(remaining_batch)} results")
    
    # Combine all results
    all_results = first_batch + remaining_batch
    print(f"\n✅ Total combined: {len(all_results)} domains")
    
    # Count statistics
    found = sum(1 for r in all_results if r['verdict'] == 'FOUND')
    not_found = sum(1 for r in all_results if r['verdict'] == 'NOT_FOUND')
    
    # Count by source
    sources = defaultdict(int)
    for r in all_results:
        sources[r['source']] += 1
    
    # Count by platform
    platforms = defaultdict(int)
    for r in all_results:
        if r['verdict'] == 'FOUND':
            platforms[r['platform']] += 1
    
    # Count by program type
    program_types = defaultdict(int)
    for r in all_results:
        if r['verdict'] == 'FOUND':
            program_types[r['program_type']] += 1
    
    # Count contacts
    contacts_with_email = sum(1 for r in all_results if r['contact_email'] and r['verdict'] == 'FOUND')
    
    # Write combined results
    output_file = '/home/code/research_all_533_results.txt'
    with open(output_file, 'w') as f:
        f.write("domain|verdict|program_type|source_step|program_url|platform|contact_email|notes\n")
        for r in all_results:
            line = f"{r['domain']}|{r['verdict']}|{r['program_type']}|{r['source']}|{r['program_url']}|{r['platform']}|{r['contact_email']}|{r['notes']}"
            f.write(line + '\n')
    
    # Write CSV version
    csv_file = '/home/code/research_all_533_results.csv'
    with open(csv_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['domain', 'verdict', 'program_type', 'source', 'program_url', 'platform', 'contact_email', 'notes'])
        writer.writeheader()
        writer.writerows(all_results)
    
    # Write JSON version
    import json
    json_file = '/home/code/research_all_533_results.json'
    with open(json_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    # Print summary
    print(f"\n{'='*80}")
    print(f"📊 COMPREHENSIVE SUMMARY - ALL 533 DOMAINS")
    print(f"{'='*80}\n")
    
    print(f"OVERALL STATISTICS:")
    print(f"  Total Domains: {len(all_results)}")
    print(f"  Programs Found: {found} ({found*100//len(all_results)}%)")
    print(f"  Not Found: {not_found} ({not_found*100//len(all_results)}%)")
    print(f"  Contact Emails: {contacts_with_email} ({contacts_with_email*100//found if found > 0 else 0}% of found)")
    
    print(f"\nDISCOVERY SOURCES:")
    for source, count in sorted(sources.items(), key=lambda x: x[1], reverse=True):
        print(f"  • {source}: {count} ({count*100//len(all_results)}%)")
    
    print(f"\nPLATFORM DISTRIBUTION (Found Programs):")
    for platform, count in sorted(platforms.items(), key=lambda x: x[1], reverse=True):
        print(f"  • {platform}: {count} ({count*100//found if found > 0 else 0}%)")
    
    print(f"\nPROGRAM TYPES (Found Programs):")
    for ptype, count in sorted(program_types.items(), key=lambda x: x[1], reverse=True):
        print(f"  • {ptype}: {count} ({count*100//found if found > 0 else 0}%)")
    
    print(f"\n{'='*80}")
    print(f"📁 DELIVERABLES:")
    print(f"  • {output_file} (pipe-delimited)")
    print(f"  • {csv_file} (Excel/Sheets)")
    print(f"  • {json_file} (Structured JSON)")
    print(f"{'='*80}\n")

if __name__ == '__main__':
    main()
