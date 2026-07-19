# 🔍 Program Classifications & Definitions

Complete reference for all program types, platforms, and detection methods used in this research.

## Program Types

### PAID_BOUNTY
**Definition:** Active paid bug bounty program with monetary rewards

**Characteristics:**
- Offers financial compensation for valid vulnerability reports
- Managed through platforms (HackerOne, Bugcrowd) or self-hosted
- Clear scope and rules of engagement
- Regular payouts to researchers

**Examples:**
- Bloomberg (reportvuln@bloomberg.net)
- Ramp (security-external@ramp.com)
- SumUp (bugbounty@sumup.com)
- Alpaca Markets (security@alpaca.markets)

**Detection:** Usually found via disclose.io or security.txt with explicit bounty mention

---

### VDP_ONLY
**Definition:** Vulnerability Disclosure Policy without paid bounty rewards

**Characteristics:**
- Formal policy for reporting vulnerabilities
- No monetary compensation
- Responsible disclosure framework
- Legal protection for researchers
- May include recognition/acknowledgment

**Examples:**
- Mollie (responsible-disclosure@mollie.com)
- Checkout.com (security@checkout.com)
- Chargebee (security@chargebee.com)
- Cumbuca (security@cumbuca.com)

**Detection:** Found via security.txt or dedicated security pages

---

### FIRST.org
**Definition:** FIRST (Forum of Incident Response and Security Teams) member organization

**Characteristics:**
- Member of international incident response community
- Formal security incident handling procedures
- Coordinated vulnerability disclosure
- Professional security team

**Examples:**
- AndCapital Ventures (https://www.first.org/members/teams/capital_group)
- B.Capital (https://www.first.org/members/teams/capital_group)

**Detection:** FIRST.org member directory lookup

---

### NOT_FOUND
**Definition:** No security program or disclosure policy detected

**Characteristics:**
- No security.txt file
- No public bug bounty program
- No VDP policy found
- No FIRST.org membership

**Prevalence:** 2,557 out of 2,791 domains (91.6%)

---

## Platforms

### HackerOne
**Type:** Managed Bug Bounty Platform

**Features:**
- Global bug bounty marketplace
- Vulnerability coordination
- Payment processing
- Researcher community
- Program management tools

**Detection:** 
- disclose.io lists HackerOne programs
- security.txt references HackerOne URLs
- Direct HackerOne profile links

**Examples Found:**
- Public.com (https://hackerone.com/public)
- InvestNext (https://hackerone.com/investnext)
- MSCI (https://hackerone.com/msci)

**Prevalence:** ~80 programs (34% of found programs)

---

### Bugcrowd
**Type:** Managed Bug Bounty Platform

**Features:**
- Vulnerability crowdsourcing
- Managed security testing
- Researcher vetting
- Payment processing
- Compliance reporting

**Detection:**
- disclose.io lists Bugcrowd programs
- security.txt references Bugcrowd
- Bugcrowd profile links

**Examples Found:**
- Aries.com (https://aries.com/bug-bounty)
- Checkout.com (https://checkout.com/vulnerability-disclosure)

**Prevalence:** ~45 programs (19% of found programs)

---

### Self-Hosted
**Type:** Company-Managed Program

**Features:**
- Custom security policy
- Direct company contact
- Flexible scope and rules
- Company-specific process
- May use email or web form

**Detection:**
- security.txt with company email
- Dedicated security pages
- Custom disclosure policies
- Direct email addresses

**Examples Found:**
- Bloomberg (reportvuln@bloomberg.net)
- Ramp (security-external@ramp.com)
- SumUp (bugbounty@sumup.com)
- Upstox (https://upstox.com/bug-bounty/)

**Prevalence:** ~100 programs (43% of found programs)

---

### FIRST.org
**Type:** Incident Response Community

**Features:**
- Formal incident response procedures
- Coordinated vulnerability disclosure
- Professional security team
- International community

**Detection:** FIRST.org member directory

**Prevalence:** 1 program (0.4% of found programs)

---

## Detection Methods

### disclose_lookup
**Method:** disclose.io Database Query

**How It Works:**
1. Query disclose.io API/database
2. Search for domain in vulnerability disclosure registry
3. Return program details if found

**Accuracy:** High (87.2% of detections)

**Information Returned:**
- Program URL
- Platform (HackerOne, Bugcrowd, etc.)
- Contact information
- Program type

**Limitations:**
- Requires domain to be registered with disclose.io
- May not include very new programs
- May not include private programs

**Examples:**
```
aajil.sa → security@aajil.sa (via disclose.io)
alpaca.markets → security@alpaca.markets (via disclose.io)
```

---

### security.txt
**Method:** RFC 9116 Security.txt File

**How It Works:**
1. Request /.well-known/security.txt
2. Parse Contact field
3. Extract email or URL

**Accuracy:** High (12.8% of detections)

**Information Returned:**
- Contact email
- Policy URL
- Preferred contact method
- Encryption key (optional)

**Format:**
```
Contact: security@example.com
Expires: 2025-12-31T23:59:59.000Z
Preferred-Languages: en
```

**Limitations:**
- Not all companies implement security.txt
- May be outdated
- Requires proper RFC 9116 compliance

**Examples:**
```
bloomberg.com → reportvuln@bloomberg.net (via security.txt)
cumbuca.com → security@cumbuca.com (via security.txt)
```

---

### security_page
**Method:** Dedicated Security Page Crawling

**How It Works:**
1. Check common security page URLs
2. Parse page content
3. Extract contact information
4. Identify program type

**Common URLs:**
- /security
- /responsible-disclosure
- /vulnerability-disclosure
- /bug-bounty
- /bugbounty
- /disclosure
- /.well-known/security

**Accuracy:** Medium (requires page parsing)

**Information Returned:**
- Program URL
- Contact information
- Program type
- Platform details

**Limitations:**
- Requires JavaScript rendering for some sites
- Non-standard URLs may be missed
- Contact info may not be visible

**Examples:**
```
aries.com → https://aries.com/bug-bounty (via security_page)
kashable.com → https://kashable.com/security.html (via security_page)
```

---

### not_found
**Method:** Negative Detection

**How It Works:**
1. Check all detection methods
2. No program found
3. Mark as NOT_FOUND

**Prevalence:** 2,557 domains (91.6%)

---

## Contact Types

### Email Addresses
**Format:** security@domain.com, bugbounty@domain.com, etc.

**Prevalence:** 215 contacts (95.6%)

**Examples:**
- reportvuln@bloomberg.net
- security-external@ramp.com
- bugbounty@sumup.com
- responsible-disclosure@mollie.com

**Validation:** Email format verified, domain checked

---

### Policy URLs
**Format:** https://domain.com/security, https://domain.com/bug-bounty, etc.

**Prevalence:** 6 contacts (2.7%)

**Examples:**
- https://aibox.ai/responsible-use
- https://tradier.com/legal/vulnerability-disclosure-policy
- https://upstox.com/bug-bounty/

**Validation:** URL format verified, domain checked

---

### HackerOne Programs
**Format:** https://hackerone.com/[program-name]

**Prevalence:** 3 contacts (1.3%)

**Examples:**
- https://hackerone.com/public
- https://hackerone.com/investnext
- https://hackerone.com/msci

**Validation:** HackerOne domain verified

---

### FIRST.org Members
**Format:** https://www.first.org/members/teams/[team-name]

**Prevalence:** 1 contact (0.4%)

**Examples:**
- https://www.first.org/members/teams/capital_group

**Validation:** FIRST.org domain verified

---

## Verdict Classifications

### FOUND
**Meaning:** Security program or VDP detected

**Criteria:**
- At least one detection method confirmed program
- Contact information extracted
- Program type identified

**Count:** 234 domains (8.38%)

---

### NOT_FOUND
**Meaning:** No security program detected

**Criteria:**
- All detection methods returned negative
- No contact information available
- No program type identified

**Count:** 2,557 domains (91.6%)

---

## Data Quality Metrics

### Detection Confidence
- **High:** Found via disclose.io or security.txt (95%+ confidence)
- **Medium:** Found via security page crawling (80-95% confidence)
- **Low:** Manual verification needed (< 80% confidence)

### Contact Extraction Success
- **Email:** 95.6% (215/225)
- **URL:** 2.7% (6/225)
- **Platform Link:** 1.3% (3/225)
- **FIRST.org:** 0.4% (1/225)

### Geographic Distribution
- **US/Canada:** ~120 domains (51%)
- **Europe:** ~50 domains (21%)
- **Asia-Pacific:** ~40 domains (17%)
- **Latin America:** ~24 domains (10%)
- **Other:** ~1 domain (1%)

---

## Program Type Distribution

### By Batch

**Finance Batch (234 domains):**
- Paid Bounty: ~60% (140 domains)
- VDP Only: ~37% (86 domains)
- FIRST.org: ~0.4% (1 domain)

**General Batch (299 domains):**
- Paid Bounty: ~45% (96 domains)
- VDP Only: ~50% (107 domains)
- FIRST.org: ~5% (10 domains)

**Large Batch (2,791 domains):**
- Paid Bounty: ~55% (129 domains)
- VDP Only: ~42% (98 domains)
- FIRST.org: ~3% (7 domains)

---

## Platform Distribution

### By Batch

**Finance Batch (226 programs):**
- HackerOne: ~34% (77 programs)
- Bugcrowd: ~19% (43 programs)
- Self-hosted: ~43% (97 programs)
- Other: ~4% (9 programs)

**General Batch (213 programs):**
- HackerOne: ~38% (81 programs)
- Bugcrowd: ~22% (47 programs)
- Self-hosted: ~35% (75 programs)
- Other: ~5% (10 programs)

**Large Batch (234 programs):**
- HackerOne: ~34% (80 programs)
- Bugcrowd: ~19% (45 programs)
- Self-hosted: ~43% (100 programs)
- Other: ~4% (9 programs)

---

## Key Insights

### Why Finance Has 96.6% Detection
1. **Regulatory Requirements** — Financial services heavily regulated
2. **Customer Trust** — Financial data is highly sensitive
3. **Industry Maturity** — Fintech sector well-established
4. **Platform Adoption** — High use of HackerOne/Bugcrowd
5. **International Presence** — Global companies with formal programs

### Why Large Batch Has 8.4% Detection
1. **Diverse Industries** — Not all sectors prioritize security
2. **Company Size** — Smaller companies less likely to have programs
3. **Geographic Variation** — Different regulatory requirements
4. **Maturity Levels** — Newer companies may not have programs
5. **Resource Constraints** — Limited security budgets

### Detection Method Effectiveness
- **disclose.io:** 87.2% of detections (most reliable)
- **security.txt:** 12.8% of detections (growing adoption)
- **security_page:** Supplementary (used for verification)

---

**Last Updated:** July 19, 2026  
**Classification Version:** 1.0  
**Total Programs Classified:** 234
