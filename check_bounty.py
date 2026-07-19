#!/usr/bin/env python3
"""
Bug Bounty Research Script
5-step process for each domain:
1. Check security.txt
2. Check security pages
3. Classify
4. External search (HackerOne/Bugcrowd/Intigriti APIs)
5. Final verdict
"""

import urllib.request
import urllib.error
import json
import time
import concurrent.futures
import ssl
import socket

# Disable SSL verification for speed
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

DOMAINS = [
    "1-commerce.com","1000ps.at","100hires.com","1688.com","1984.vc","1fit.app","1up.ai",
    "2cloudnine.com","30x.com","3doptix.com","3i.ai","4degrees.ai","58pic.com","5centscdn.net",
    "8m.eu","99c.co.za","a-leads.co","aajil.sa","abacum.ai","abatable.com","abble.com",
    "abcam.com","abcfintech.com","abcmouse.com","abcnews.go.com","abcsmarttech.com",
    "abctechnologies.com","abcwholesale.com","abe.ai","abeautifulsite.net","abeka.com",
    "abercrombie.com","aberdeen.com","abide.com","ableto.com","abmglobal.com",
    "abnormalsecurity.com","abra.com","abrigo.com","abs-cbn.com","absci.com","abtasty.com",
    "abuse.ch","abuseat.org","abuseipdb.com","abusix.com","academia.edu","accenture.com",
    "accion.org","acciona.com","acclaro.com","acquia.com","acronis.com","actblue.com",
    "actian.com","actionfigure.ai","actioniq.com","activecampaign.com","activefence.com",
    "activision.com","acuityscheduling.com","acunetix.com","acxiom.com","adafruit.com",
    "adguard.com","adidas.com","adobe.com","adp.com","adroll.com","adyen.com",
    "aerojet.com","aeromexico.com","affirm.com","agoda.com","agora.io","ahrefs.com",
    "akamai.com","akeyless.io","akto.io","airbnb.com","aircanada.com","airfrance.com",
    "airship.com","airslate.com","airtable.com","airtel.in","airwallex.com","aisera.com",
    "albert.ai","albertsons.com","alchemer.com","alchemy.com","alcion.io","algolia.com",
    "alibaba.com","alibabacloud.com","aliexpress.com","alipay.com","allbirds.com",
    "allegro.pl","allscripts.com","allstate.com","ally.com","almalinux.org","alodokter.com",
    "alphasense.com","altair.com","alteryx.com","altium.com","altruist.com","amadeus.com",
    "amazon.com","amboss.com","amd.com","amex.com","amgen.com","amplitude.com","amwell.com",
    "anaplan.com","andela.com","android.com","angi.com","ansible.com","ansys.com",
    "anthropic.com","aon.com","apache.org","apexon.com","apigee.com","apify.com",
    "apollo.io","appdome.com","appfolio.com","appgate.com","appian.com","apple.com",
    "applovin.com","appnexus.com","appomni.com","appsflyer.com","appsmith.com",
    "appwrite.io","aptible.com","aptiv.com","aquasecurity.io","arcgis.com","ardoq.com",
    "arista.com","armorcode.com","armory.io","arnica.io","arqit.com","artera.ai",
    "aruba.com","arxiv.org","asana.com","asapp.com","ascend.io","aserto.com","ashby.com",
    "asml.com","aspentech.com","assent.com","astrazeneca.com","astronomer.io","ataccama.com",
    "athenahealth.com","atlassian.com","atob.com","atscale.com","attentive.com","attest.com",
    "audible.com","auditboard.com","augury.com","auth0.com","authomize.com","autify.com",
    "autodesk.com","automox.com","autorabit.com","avanan.com","avast.com","avaya.com",
    "aviatrix.com","avid.com","aws.amazon.com","axonius.com","ayasdi.com","aylanetworks.com",
    "azure.microsoft.com","b2w.io","backblaze.com","backmarket.com","badoo.com","baidu.com",
    "bamboohr.com","bandcamp.com","bandwidth.com","bankofamerica.com","barclays.com",
    "basecamp.com","basistheory.com","bayer.com","bazaarvoice.com","bbc.co.uk","bbva.com",
    "beachbody.com","beamery.com","behance.net","benchling.com","bettercloud.com",
    "betterhelp.com","betterup.com","bigcommerce.com","bigpanda.io","bigtincan.com",
    "bilibili.com","bitbucket.org","bitcoin.org","bitdefender.com","bitglass.com",
    "bitsight.com","bitwarden.com","blackbaud.com","blackberry.com","blackduck.com",
    "blackkite.com","blackline.com","blackrock.com","blinkist.com","blockchain.com",
    "bloomberg.com","bluejeans.com","blueshift.com","bluevoyant.com","bmc.com","boeing.com",
    "bolt.com","bolttech.com","booking.com","boomi.com","boozallen.com","box.com",
    "braze.com","breachlock.com","broadcom.com","browserstack.com","bugcrowd.com",
    "bugsnag.com","buildkite.com","bupa.com","bynder.com","bytedance.com","c3.ai",
    "calix.com","callrail.com","camunda.com","canva.com","carbonblack.com","carbonite.com",
    "cardlytics.com","careem.com","cargurus.com","carta.com","catchpoint.com","celigo.com",
    "censys.io","centene.com","centrify.com","cequence.ai","cerby.com","certik.com",
    "certinia.com","chainguard.dev","chainalysis.com","chargebee.com","checkmarx.com",
    "checkr.com","chef.io","chime.com","chronicle.security","cisco.com","citrix.com",
    "clari.com","claroty.com","clearbit.com","clickup.com","cloudflare.com","cloudinary.com",
    "cloudsek.com","cloudsmith.io","cobalt.io","coda.io","codefresh.io","cofense.com",
    "cognite.com","cohesity.com","coinbase.com","coindcx.com","collibra.com","comcast.com",
    "commvault.com","confluent.io","contentful.com","contentsquare.com","contrast.security",
    "conviva.com","coralogix.com","corelight.com","coupa.com","coverity.com",
    "crowdstrike.com","cyberark.com","cybereason.com","cybersixgill.com","cycode.com",
    "cypress.io","d2iq.com","darktrace.com","databricks.com","datadog.com","dataminr.com",
    "datariskmanager.com","datarobot.com","datastax.com","datto.com","deepfence.io",
    "deepl.com","deepsource.io","delinea.com","dell.com","deloitte.com","detectify.com",
    "devrev.ai","devtron.ai","digitalocean.com","discord.com","docusign.com","doppler.com",
    "drata.com","drift.com","dropbox.com","druva.com","duo.com","dynatrace.com",
    "elastic.co","elasticpath.com","elevenlabs.io","endor.ai","envoy.com","epic.com",
    "epiq.com","eset.com","esper.io","exabeam.com","expel.io","experian.com",
    "extrahop.com","f5.com","facebook.com","fairwinds.com","fastly.com","featurespace.com",
    "figma.com","fireeye.com","fivetran.com","flashpoint.io","flexera.com","fluentd.org",
    "forcepoint.com","ford.com","forescout.com","forestadmin.com","forgerock.com",
    "fortinet.com","freshdesk.com","freshworks.com","frontegg.com","fullstory.com",
    "gartner.com","gcp.com","gemini.google.com","github.com","gitlab.com","gitleaks.io",
    "globant.com","glovo.com","gong.io","google.com","grafana.com","grammarly.com",
    "greenhouse.io","guardicore.com","gusto.com","hackerone.com","hashicorp.com",
    "heap.io","heroku.com","highspot.com","hootsuite.com","hubspot.com","humio.com",
    "huntress.com","ibm.com","illumio.com","imperva.com","indeed.com","infoblox.com",
    "informatica.com","intigriti.com","invicti.com","ionic.io","ironnet.com","ivanti.com",
    "jamf.com","jfrog.com","jira.com","jumpcloud.com","juniper.net","kandji.io",
    "keeper.io","keyfactor.com","knowbe4.com","lacework.com","launchdarkly.com",
    "leapwork.com","legalzoom.com","linear.app","linkedin.com","linode.com","logrhythm.com",
    "looker.com","lumu.io","malwarebytes.com","mandiant.com","mattermost.com","maxmind.com",
    "mcafee.com","medallia.com","medium.com","mend.io","meta.com","microsoft.com",
    "mimecast.com","mixpanel.com","mongodb.com","mulesoft.com","netscout.com","netspi.com",
    "netskope.com","netsuite.com","newrelic.com","nexthink.com","nightfall.ai","nmap.org",
    "nokia.com","noname.security","notion.so","nowsecure.com","nozominetworks.com",
    "nvidia.com","okta.com","onfido.com","onspring.com","openai.com","opsgenie.com",
    "oracle.com","orca.security","outreach.io","pagerduty.com","palo-alto.com",
    "paloaltonetworks.com","panaseer.com","panther.com","paypal.com","pentera.io",
    "perimeter81.com","ping.com","pingidentity.com","plaid.com","pluralsight.com",
    "postman.com","proofpoint.com","qualys.com","rapid7.com","recorded-future.com",
    "recordedfuture.com","redcanary.com","reddit.com","relativity.com","resilinc.com",
    "rubrik.com","sailpoint.com","salesforce.com","samsara.com","sap.com","secureworks.com",
    "securityscorecard.com","semgrep.dev","sendgrid.com","sentinelone.com","servicenow.com",
    "shopify.com","signal.org","slack.com","snyk.io","sonatype.com","sophos.com",
    "splunk.com","spotify.com","square.com","stackhawk.com","stytch.com","sumo-logic.com",
    "sumologic.com","supabase.com","swimlane.com","synopsys.com","tableau.com","tanium.com",
    "tenable.com","terraform.io","threatlocker.com","tines.com","trendmicro.com",
    "trivy.dev","twilio.com","twitter.com","uptycs.com","vanta.com","varonis.com",
    "vectra.ai","veracode.com","vercel.com","verizon.com","vmware.com","wazuh.com",
    "webex.com","wiz.io","workday.com","xdr.com","yelp.com","zendesk.com","zoom.us",
    "zscaler.com","zynga.com"
]

def fetch_url(url, timeout=8):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 SecurityResearch'})
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            content = resp.read(4096).decode('utf-8', errors='ignore')
            return resp.status, content
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception:
        return 0, ""

BOUNTY_KEYWORDS = [
    'bug bounty', 'vulnerability disclosure', 'responsible disclosure',
    'security.txt', 'hackerone.com', 'bugcrowd.com', 'intigriti.com',
    'yeswehack.com', 'synack.com', 'cobalt.io', 'report a vulnerability',
    'report vulnerability', 'security report', 'hall of fame', 'security researcher',
    'bounty program', 'vdp', 'cvd', 'coordinated vulnerability'
]

PAID_KEYWORDS = [
    'bug bounty', 'bounty program', 'reward', 'paid', 'compensation',
    'hackerone.com', 'bugcrowd.com', 'intigriti.com', 'yeswehack.com',
    'synack.com', 'cobalt.io'
]

VDP_KEYWORDS = [
    'vulnerability disclosure', 'responsible disclosure', 'vdp',
    'coordinated vulnerability', 'report a vulnerability', 'no reward',
    'no monetary', 'hall of fame', 'acknowledgement', 'cvd'
]

def detect_platform(text):
    text_lower = text.lower()
    if 'hackerone.com' in text_lower: return 'hackerone'
    if 'bugcrowd.com' in text_lower: return 'bugcrowd'
    if 'intigriti.com' in text_lower: return 'intigriti'
    if 'yeswehack.com' in text_lower: return 'yeswehack'
    if 'synack.com' in text_lower: return 'synack'
    if 'cobalt.io' in text_lower: return 'cobalt'
    return 'self-hosted'

def extract_program_url(text, domain):
    import re
    patterns = [
        r'(https?://hackerone\.com/[^\s\'"<>]+)',
        r'(https?://bugcrowd\.com/[^\s\'"<>]+)',
        r'(https?://intigriti\.com/[^\s\'"<>]+)',
        r'(https?://app\.intigriti\.com/[^\s\'"<>]+)',
        r'(https?://yeswehack\.com/[^\s\'"<>]+)',
        r'(https?://synack\.com/[^\s\'"<>]+)',
        r'(https?://cobalt\.io/[^\s\'"<>]+)',
    ]
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            return m.group(1).rstrip('.,;)')
    return ''

def classify_text(text):
    text_lower = text.lower()
    has_bounty = any(k in text_lower for k in BOUNTY_KEYWORDS)
    if not has_bounty:
        return None, None, None
    is_paid = any(k in text_lower for k in PAID_KEYWORDS)
    is_vdp = any(k in text_lower for k in VDP_KEYWORDS)
    if is_paid:
        prog_type = 'PAID_BOUNTY'
    elif is_vdp:
        prog_type = 'VDP_ONLY'
    else:
        prog_type = 'VDP_ONLY'
    platform = detect_platform(text)
    url = extract_program_url(text, '')
    return prog_type, platform, url

def research_domain(domain):
    result = {
        'domain': domain,
        'verdict': 'NOT_FOUND',
        'program_type': 'N/A',
        'source_step': 'not_found',
        'program_url': '',
        'platform': '',
        'notes': ''
    }

    # Step 1: Check security.txt
    for path in [f'https://{domain}/.well-known/security.txt', f'https://{domain}/security.txt']:
        status, content = fetch_url(path)
        if status == 200 and content and len(content) > 20:
            cl = content.lower()
            if any(k in cl for k in ['contact:', 'policy:', 'hiring:', 'acknowledgments:', 'canonical:']):
                prog_type, platform, prog_url = classify_text(content)
                if prog_type:
                    result['verdict'] = 'FOUND'
                    result['program_type'] = prog_type
                    result['source_step'] = 'security.txt'
                    result['program_url'] = prog_url
                    result['platform'] = platform
                    result['notes'] = f'security.txt found at {path}'
                    return result
                else:
                    # Has security.txt but no clear bounty — check for contact URL
                    import re
                    contact = re.search(r'Contact:\s*(https?://[^\s]+)', content, re.IGNORECASE)
                    if contact:
                        contact_url = contact.group(1)
                        if any(p in contact_url for p in ['hackerone','bugcrowd','intigriti','yeswehack','synack','cobalt']):
                            result['verdict'] = 'FOUND'
                            result['program_type'] = 'PAID_BOUNTY'
                            result['source_step'] = 'security.txt'
                            result['program_url'] = contact_url
                            result['platform'] = detect_platform(contact_url)
                            result['notes'] = f'security.txt contact points to bounty platform'
                            return result
                        else:
                            result['notes'] = f'security.txt found, contact={contact_url}'
                    else:
                        result['notes'] = 'security.txt found but no bounty indicators'
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
    ]
    for path in security_paths:
        status, content = fetch_url(path)
        if status == 200 and content and len(content) > 100:
            prog_type, platform, prog_url = classify_text(content)
            if prog_type:
                result['verdict'] = 'FOUND'
                result['program_type'] = prog_type
                result['source_step'] = 'security_page'
                result['program_url'] = prog_url if prog_url else path
                result['platform'] = platform
                result['notes'] = f'Found at {path}'
                return result

    # Step 3 & 4: Check known platforms via their APIs/search
    # HackerOne
    h1_url = f'https://hackerone.com/{domain.split(".")[0]}'
    status, content = fetch_url(f'https://api.hackerone.com/v1/hackers/programs?query={domain}&limit=1')
    # Try HackerOne directory search
    status2, content2 = fetch_url(f'https://hackerone.com/programs/search?query={domain}&sort=published_at%3Adescending&limit=1')
    if status2 == 200 and domain.split('.')[0].lower() in content2.lower():
        prog_type, platform, prog_url = classify_text(content2)
        if prog_type:
            result['verdict'] = 'FOUND'
            result['program_type'] = prog_type
            result['source_step'] = 'search'
            result['program_url'] = prog_url
            result['platform'] = 'hackerone'
            result['notes'] = 'Found via HackerOne search'
            return result

    # Bugcrowd
    status3, content3 = fetch_url(f'https://bugcrowd.com/programs.json?q={domain}')
    if status3 == 200 and domain.split('.')[0].lower() in content3.lower():
        result['verdict'] = 'FOUND'
        result['program_type'] = 'PAID_BOUNTY'
        result['source_step'] = 'search'
        result['program_url'] = f'https://bugcrowd.com/programs?q={domain}'
        result['platform'] = 'bugcrowd'
        result['notes'] = 'Found via Bugcrowd search'
        return result

    # Step 5: Final verdict
    result['notes'] = result['notes'] or 'No program found after full 5-step check'
    return result

def main():
    print("domain|verdict|program_type|source_step|program_url|platform|notes")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(research_domain, d): d for d in DOMAINS}
        for future in concurrent.futures.as_completed(futures):
            r = future.result()
            print(f"{r['domain']}|{r['verdict']}|{r['program_type']}|{r['source_step']}|{r['program_url']}|{r['platform']}|{r['notes']}")

if __name__ == '__main__':
    main()
