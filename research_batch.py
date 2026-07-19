#!/usr/bin/env python3
"""
Batch research using multiple methods
Outputs results for manual verification and API-based searches
"""

import json

# Read domains
with open('/home/code/new_domains.txt', 'r') as f:
    domains = [line.strip() for line in f if line.strip()]

print(f"Total domains to research: {len(domains)}")
print()

# Create batches for different research methods
batch_size = 50

# Batch 1: Direct security.txt checks (first 50)
print("=" * 80)
print("BATCH 1: Security.txt Direct Checks (First 50 domains)")
print("=" * 80)
batch1 = domains[:50]
for i, domain in enumerate(batch1, 1):
    print(f"{i:2d}. {domain}")

print()
print("=" * 80)
print("BATCH 2: Security Page Checks (Next 50 domains)")
print("=" * 80)
batch2 = domains[50:100]
for i, domain in enumerate(batch2, 1):
    print(f"{i:2d}. {domain}")

print()
print("=" * 80)
print("BATCH 3: HackerOne/Bugcrowd Search (Next 50 domains)")
print("=" * 80)
batch3 = domains[100:150]
for i, domain in enumerate(batch3, 1):
    print(f"{i:2d}. {domain}")

print()
print("=" * 80)
print("BATCH 4: Remaining domains (Last 84 domains)")
print("=" * 80)
batch4 = domains[150:]
for i, domain in enumerate(batch4, 1):
    print(f"{i:2d}. {domain}")

# Save batches for processing
with open('/home/code/batch1_domains.txt', 'w') as f:
    f.write('\n'.join(batch1))

with open('/home/code/batch2_domains.txt', 'w') as f:
    f.write('\n'.join(batch2))

with open('/home/code/batch3_domains.txt', 'w') as f:
    f.write('\n'.join(batch3))

with open('/home/code/batch4_domains.txt', 'w') as f:
    f.write('\n'.join(batch4))

print()
print("[✓] Batches created:")
print(f"    - batch1_domains.txt ({len(batch1)} domains)")
print(f"    - batch2_domains.txt ({len(batch2)} domains)")
print(f"    - batch3_domains.txt ({len(batch3)} domains)")
print(f"    - batch4_domains.txt ({len(batch4)} domains)")
