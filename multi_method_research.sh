#!/bin/bash

# Multi-Method Bug Bounty Research Script
# Uses: security.txt, security pages, robots.txt, sitemap, HackerOne/Bugcrowd search

DOMAINS_FILE="$1"
OUTPUT_FILE="$2"
TIMEOUT=5
MAX_PARALLEL=20

if [ -z "$DOMAINS_FILE" ] || [ -z "$OUTPUT_FILE" ]; then
    echo "Usage: $0 <domains_file> <output_file>"
    exit 1
fi

# Initialize output file
echo "domain|verdict|program_type|source_step|program_url|platform|contact_email|notes" > "$OUTPUT_FILE"

# Counter
TOTAL=$(wc -l < "$DOMAINS_FILE")
PROCESSED=0
FOUND=0

# Function to research a single domain
research_domain() {
    local domain="$1"
    local verdict="NOT_FOUND"
    local program_type="N/A"
    local source_step="none"
    local program_url=""
    local platform=""
    local contact_email=""
    local notes=""
    
    # Step 1: Check security.txt
    for path in "/.well-known/security.txt" "/security.txt"; do
        local url="https://${domain}${path}"
        local response=$(curl -s -m $TIMEOUT -L "$url" 2>/dev/null)
        
        if echo "$response" | grep -q "Contact:"; then
            verdict="FOUND"
            source_step="security.txt"
            program_url="$url"
            contact_email=$(echo "$response" | grep "Contact:" | head -1 | sed 's/Contact:\s*//' | cut -d' ' -f1)
            notes="Found via security.txt"
            break
        fi
    done
    
    # Step 2: Check common security pages
    if [ "$verdict" = "NOT_FOUND" ]; then
        local security_paths=(
            "/security"
            "/bug-bounty"
            "/bugbounty"
            "/responsible-disclosure"
            "/vulnerability-disclosure"
            "/security.html"
            "/disclosure"
        )
        
        for path in "${security_paths[@]}"; do
            local url="https://${domain}${path}"
            local response=$(curl -s -m $TIMEOUT -L "$url" 2>/dev/null)
            
            if echo "$response" | grep -qi "bug bounty\|vulnerability disclosure\|hackerone\|bugcrowd\|intigriti"; then
                verdict="FOUND"
                source_step="security_page"
                program_url="$url"
                notes="Found at $path"
                
                # Detect platform
                if echo "$response" | grep -qi "hackerone"; then
                    platform="hackerone"
                elif echo "$response" | grep -qi "bugcrowd"; then
                    platform="bugcrowd"
                elif echo "$response" | grep -qi "intigriti"; then
                    platform="intigriti"
                else
                    platform="self-hosted"
                fi
                
                # Extract email
                contact_email=$(echo "$response" | grep -oE '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}' | head -1)
                
                # Detect program type
                if echo "$response" | grep -qi "paid\|reward\|bounty.*\$\|payment"; then
                    program_type="PAID_BOUNTY"
                else
                    program_type="VDP_ONLY"
                fi
                
                break
            fi
        done
    fi
    
    # Step 3: Check robots.txt for security hints
    if [ "$verdict" = "NOT_FOUND" ]; then
        local robots=$(curl -s -m $TIMEOUT "https://${domain}/robots.txt" 2>/dev/null)
        if echo "$robots" | grep -qi "security\|bug\|bounty\|vulnerability"; then
            notes="Security keywords in robots.txt"
        fi
    fi
    
    # Step 4: Check sitemap.xml for security pages
    if [ "$verdict" = "NOT_FOUND" ]; then
        local sitemap=$(curl -s -m $TIMEOUT "https://${domain}/sitemap.xml" 2>/dev/null)
        if echo "$sitemap" | grep -qi "security\|bug\|bounty\|vulnerability\|disclosure"; then
            notes="Security URLs in sitemap.xml"
        fi
    fi
    
    # Output result
    echo "${domain}|${verdict}|${program_type}|${source_step}|${program_url}|${platform}|${contact_email}|${notes}" >> "$OUTPUT_FILE"
    
    if [ "$verdict" = "FOUND" ]; then
        ((FOUND++))
        echo "[+] FOUND: $domain | $platform | $contact_email"
    fi
}

export -f research_domain
export TIMEOUT OUTPUT_FILE

# Process domains in parallel
cat "$DOMAINS_FILE" | xargs -P $MAX_PARALLEL -I {} bash -c 'research_domain "$@"' _ {}

echo ""
echo "=========================================="
echo "Research Complete!"
echo "Results saved to: $OUTPUT_FILE"
echo "=========================================="

