#!/usr/bin/env python3
"""
Export research results to multiple formats
"""

import csv
import json

# Read the pipe-delimited results
results = []
with open('/home/code/research_advanced_results.txt', 'r') as f:
    lines = f.readlines()
    header = lines[0].strip().split('|')
    
    for line in lines[1:]:
        parts = line.strip().split('|')
        if len(parts) >= len(header):
            result = {header[i]: parts[i] for i in range(len(header))}
            results.append(result)

# Statistics
found_count = sum(1 for r in results if r['verdict'] == 'FOUND')
not_found_count = sum(1 for r in results if r['verdict'] == 'NOT_FOUND')

# Export to CSV
with open('/home/code/research_results.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=header)
    writer.writeheader()
    writer.writerows(results)

# Export to JSON
with open('/home/code/research_results.json', 'w') as f:
    json.dump({
        'metadata': {
            'total_domains': len(results),
            'found': found_count,
            'not_found': not_found_count,
            'detection_rate': f"{100*found_count/len(results):.1f}%"
        },
        'results': results
    }, f, indent=2)

# Create summary statistics
print("=" * 80)
print("RESEARCH RESULTS EXPORT SUMMARY")
print("=" * 80)
print()
print(f"Total Domains: {len(results)}")
print(f"Programs Found: {found_count} ({100*found_count/len(results):.1f}%)")
print(f"Not Found: {not_found_count} ({100*not_found_count/len(results):.1f}%)")
print()

# Contact email statistics
emails = [r['contact_email'] for r in results if r['contact_email']]
print(f"Contact Emails Extracted: {len(emails)}/{found_count}")
print()

# Source statistics
sources = {}
for r in results:
    if r['verdict'] == 'FOUND':
        source = r['source_step']
        sources[source] = sources.get(source, 0) + 1

print("Discovery Sources:")
for source, count in sorted(sources.items(), key=lambda x: -x[1]):
    print(f"  - {source}: {count}")
print()

# Platform statistics
platforms = {}
for r in results:
    if r['verdict'] == 'FOUND' and r['platform']:
        platform = r['platform']
        platforms[platform] = platforms.get(platform, 0) + 1

if platforms:
    print("Platforms Identified:")
    for platform, count in sorted(platforms.items(), key=lambda x: -x[1]):
        print(f"  - {platform}: {count}")
print()

# Email pattern analysis
email_patterns = {}
for email in emails:
    if '@' in email:
        pattern = email.split('@')[0]
        email_patterns[pattern] = email_patterns.get(pattern, 0) + 1

print("Top Email Prefixes:")
for pattern, count in sorted(email_patterns.items(), key=lambda x: -x[1])[:10]:
    print(f"  - {pattern}@: {count}")
print()

print("=" * 80)
print("Files Generated:")
print("  - /home/code/research_results.csv")
print("  - /home/code/research_results.json")
print("  - /home/code/research_advanced_results.txt (pipe-delimited)")
print("=" * 80)

