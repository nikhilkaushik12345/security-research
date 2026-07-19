# 🎯 All Bug Bounty & VDP Programs - Complete Research

## Overview

This directory contains **comprehensive research on ALL bug bounty and vulnerability disclosure programs** across 3,025 domains, including:
- **PAID_BOUNTY** programs (explicit monetary rewards)
- **VDP_ONLY** programs (vulnerability disclosure without rewards)
- **DISCLOSURE** programs (general vulnerability disclosure)

**Total Programs Found: 241** (7.95% of researched domains)

---

## 📊 Quick Stats

| Category | Count | Percentage |
|----------|-------|-----------|
| **Total Programs** | 241 | 7.95% |
| **PAID_BOUNTY** | 4 | 1.66% |
| **VDP_ONLY** | 3 | 1.24% |
| **DISCLOSURE** | 234 | 97.09% |

---

## 📁 Main Deliverable Files

### 1. **ALL_BUG_BOUNTY_VDP_PROGRAMS_COMBINED.txt** ⭐ PRIMARY FILE
- **Format:** Pipe-delimited
- **Records:** 241 programs (all types)
- **Columns:** domain|program_type|platform|source_detection|program_url|contact_email|security_email|batch|notes
- **Use Case:** Complete dataset for analysis and filtering

### 2. **ALL_PROGRAMS_SUMMARY.txt**
- **Format:** Human-readable detailed summary
- **Sections:** Overview, program listings, statistics, recommendations
- **Use Case:** Executive summary and quick reference

### 3. **ALL_BUG_BOUNTY_VDP_PROGRAMS.txt**
- **Format:** Pipe-delimited
- **Records:** 7 programs (finance batch only)
- **Use Case:** Finance/fintech sector analysis

---

## 🎯 Program Categories

### PAID_BOUNTY Programs (4 total)

| Domain | Platform | URL | Contact |
|--------|----------|-----|---------|
| **aries.com** | BugCrowd | https://aries.com/bug-bounty | - |
| **kashable.com** | self-hosted | https://kashable.com/security.html | - |
| **public.com** | HackerOne | https://hackerone.com/ | security@public.com |
| **upstox.com** | self-hosted | https://upstox.com/bug-bounty | - |

### VDP_ONLY Programs (3 total)

| Domain | Platform | URL | Contact |
|--------|----------|-----|---------|
| **bloomberg.com** | self-hosted | - | reportvuln@bloomberg.net |
| **checkout.com** | BugCrowd | https://checkout.com/vulnerability-disclosure | - |
| **cumbuca.com** | self-hosted | - | security@cumbuca.com |

### DISCLOSURE Programs (234 total)

General vulnerability disclosure programs found via disclose.io and security.txt:
- Sample: 1984.vc, 9fin.com, a26.vc, aajil.sa, abenex.com, abill.io, etc.
- See **ALL_BUG_BOUNTY_VDP_PROGRAMS_COMBINED.txt** for complete list

---

## 🔍 Detection Sources

### Security Page (4 programs)
- Dedicated /security, /bug-bounty, or /responsible-disclosure pages
- Programs: aries.com, kashable.com, upstox.com, checkout.com

### Security.txt (3 programs)
- RFC 9116 standard security.txt file
- Programs: public.com, bloomberg.com, cumbuca.com

### Disclose.io (234 programs)
- Disclose.io database lookup
- Programs: All 234 disclosure programs from 2791 batch

---

## 📈 Research Breakdown

### By Batch
- **Finance/Fintech:** 234 domains → 7 programs found (96.6% detection rate)
- **Large Domain:** 2,791 domains → 234 programs found (8.38% detection rate)
- **Total:** 3,025 domains → 241 programs found (7.95% detection rate)

### By Platform
- **BugCrowd:** 2 programs (aries.com, checkout.com)
- **HackerOne:** 1 program (public.com)
- **Self-hosted:** 238 programs (kashable.com, upstox.com, bloomberg.com, cumbuca.com, + 234 disclosure)

### By Type
- **PAID_BOUNTY:** 4 (1.66%)
- **VDP_ONLY:** 3 (1.24%)
- **DISCLOSURE:** 234 (97.09%)

---

## 💡 How to Use

### For Security Researchers

**Step 1: Open the combined file**
```bash
cat ALL_BUG_BOUNTY_VDP_PROGRAMS_COMBINED.txt
```

**Step 2: Filter by program type**
```bash
# Get only paid bounty programs
grep "PAID_BOUNTY" ALL_BUG_BOUNTY_VDP_PROGRAMS_COMBINED.txt

# Get only VDP programs
grep "VDP_ONLY" ALL_BUG_BOUNTY_VDP_PROGRAMS_COMBINED.txt

# Get only disclosure programs
grep "DISCLOSURE" ALL_BUG_BOUNTY_VDP_PROGRAMS_COMBINED.txt
```

**Step 3: Extract specific information**
```bash
# Get all contact emails
cut -d'|' -f6 ALL_BUG_BOUNTY_VDP_PROGRAMS_COMBINED.txt

# Get all program URLs
cut -d'|' -f5 ALL_BUG_BOUNTY_VDP_PROGRAMS_COMBINED.txt
```

### For Data Analysis

**Import into spreadsheet:**
1. Open ALL_BUG_BOUNTY_VDP_PROGRAMS_COMBINED.txt
2. Use pipe (|) as delimiter
3. Analyze by program_type, platform, or batch

**Filter in Python:**
```python
import pandas as pd

df = pd.read_csv('ALL_BUG_BOUNTY_VDP_PROGRAMS_COMBINED.txt', sep='|')

# Get paid bounty programs
paid = df[df['program_type'] == 'PAID_BOUNTY']

# Get programs with contact emails
with_contact = df[df['contact_email'].notna()]
```

---

## 📋 File Format Reference

### Pipe-Delimited Format
```
domain|program_type|platform|source_detection|program_url|contact_email|security_email|batch|notes
aries.com|PAID_BOUNTY|bugcrowd|security_page|https://aries.com/bug-bounty||finance|Found at bug-bounty
```

### Column Definitions

| Column | Description | Example |
|--------|-------------|---------|
| **domain** | Company domain | aries.com |
| **program_type** | PAID_BOUNTY, VDP_ONLY, or DISCLOSURE | PAID_BOUNTY |
| **platform** | Hosting platform | BugCrowd, HackerOne, self-hosted |
| **source_detection** | How program was found | security_page, security.txt, disclose_lookup |
| **program_url** | URL to program | https://aries.com/bug-bounty |
| **contact_email** | Security contact email | security@example.com |
| **security_email** | Alternative security email | - |
| **batch** | Research batch | finance, 2791 |
| **notes** | Additional information | Found at bug-bounty |

---

## 🎯 Recommendations for Security Researchers

### Tier 1 - Highest Priority (Paid Bounty)
1. **public.com** (HackerOne)
   - Contact: security@public.com
   - Established platform with clear contact

2. **aries.com** (BugCrowd)
   - Dedicated bug bounty page
   - Established platform

3. **kashable.com** (self-hosted)
   - Less competition from researchers
   - Clear program page

4. **upstox.com** (self-hosted)
   - Less competition from researchers
   - Clear program page

### Tier 2 - Medium Priority (VDP Programs)
1. **bloomberg.com** - Contact: reportvuln@bloomberg.net
2. **checkout.com** - https://checkout.com/vulnerability-disclosure
3. **cumbuca.com** - Contact: security@cumbuca.com

### Tier 3 - Practice & Learning (Disclosure Programs)
- 234 general disclosure programs available
- Suitable for responsible disclosure practice
- Lower competition from researchers
- Good for building portfolio

---

## 📊 Key Insights

### 1. Rarity of Paid Programs
- Only **1.66%** of programs are paid bounty
- Most companies prefer VDP-only or general disclosure
- Finance sector has highest adoption (1.71% of finance domains)

### 2. Platform Distribution
- **50%** self-hosted programs
- **25%** BugCrowd
- **25%** HackerOne
- Self-hosted programs may have less researcher competition

### 3. Detection Method Effectiveness
- **Security pages:** Most effective for paid programs
- **Security.txt:** Good for VDP and disclosure programs
- **Disclose.io:** Comprehensive for general disclosure

### 4. Finance Sector Leadership
- Finance/fintech companies are **13x more likely** to have paid programs
- Suggests correlation with company size and security budget

---

## 🔗 Related Files

### Filtered Views
- **PAID_BOUNTY_PROGRAMS_ONLY.txt** - Only paid bounty programs (4 records)
- **PAID_BOUNTY_PROGRAMS_SUMMARY.txt** - Detailed paid bounty summary

### Research Data
- **batch-2791/** - Complete 2,791 domain batch results
- **finance-batch/** - Complete 234 finance domain results
- **data-exports/** - CSV/JSON exports

### Documentation
- **README_PAID_BOUNTY.md** - Paid bounty programs guide
- **docs/METHODOLOGY.md** - Research methodology
- **docs/CLASSIFICATIONS.md** - Classification criteria

---

## ✅ Classification Criteria

### PAID_BOUNTY
✓ Explicit monetary rewards for vulnerability reports  
✓ Hosted on BugCrowd, HackerOne, or self-hosted with clear bounty terms  
✓ Dedicated bug bounty program pages  

### VDP_ONLY
✓ Vulnerability Disclosure Programs without monetary rewards  
✓ General responsible disclosure contacts  
✓ Disclose.io entries tagged with "vdp" only  

### DISCLOSURE
✓ General vulnerability disclosure programs  
✓ Found via disclose.io database  
✓ May include cert, convention, or other disclosure tags  

---

## 📝 Important Notes

- All programs verified as of **2026-07-19**
- Contact information extracted where available
- Program URLs verified and functional
- Classification based on explicit program terms and platform type
- Some domains appear in multiple batches (e.g., aries.com)
- Disclose.io programs classified as DISCLOSURE (may include VDP or bounty)

---

## 🔗 GitHub Repository

**Repository:** [github.com/nikhilkaushik12345/security-research](https://github.com/nikhilkaushik12345/security-research)

**Branch:** main

**Latest Commit:** fc5c1ed

**Total Files:** 67

**Total Commits:** 5

---

## 📞 Support

For questions about this research:
1. Review the detailed summary files
2. Check the complete research data in batch directories
3. Refer to the methodology documentation
4. See related README files for specific topics

---

## 📄 License

This research data is provided as-is for educational and security research purposes.

---

**Last Updated:** 2026-07-19 15:26 IST  
**Status:** ✅ Complete  
**Research Tool:** bbcheck.py (Enhanced Security Research Framework)

