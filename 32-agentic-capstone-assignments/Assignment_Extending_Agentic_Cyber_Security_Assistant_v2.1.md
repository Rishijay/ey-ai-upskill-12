# Assignment: Extending the Agentic Cyber Security Assistant v2.1

## Objective

Extend the **Agentic Cyber Security Assistant v2.1** by integrating
three additional cybersecurity intelligence sources as custom tools and
incorporating them into the existing agentic workflow.

------------------------------------------------------------------------

# Part 1 -- Study the Technologies

## 1. CISA KEV (Known Exploited Vulnerabilities)

### What is it?

The CISA Known Exploited Vulnerabilities (KEV) Catalog is maintained by
the U.S. Cybersecurity and Infrastructure Security Agency (CISA). It
contains vulnerabilities that are **confirmed to be actively
exploited**.

### Why is it useful?

Unlike the NVD, which lists disclosed vulnerabilities, KEV helps
prioritize patching by identifying vulnerabilities that attackers are
already exploiting.

### Typical Use Cases

-   Patch prioritization
-   Threat intelligence
-   Security operations
-   

### Query
    - Are there any actively exploited Windows SMB vulnerabilities?

------------------------------------------------------------------------

## 2. MITRE ATT&CK

### What is it?

MITRE ATT&CK is a knowledge base of **adversary tactics and techniques**
used during cyber attacks.

### Why is it useful?

It explains *how attackers operate* rather than listing vulnerabilities.

### Typical Use Cases

-   Threat hunting
-   Detection engineering
-   Incident response
-   

### Query
-   Explain Pass-the-Hash.

------------------------------------------------------------------------

## 3. EPSS (Exploit Prediction Scoring System)

### What is it?

EPSS predicts the probability that a vulnerability (CVE) will be
exploited in the next 30 days.

### Why is it useful?

It helps prioritize remediation based on exploitation likelihood rather
than severity alone.

### Typical Use Cases

-   Vulnerability prioritization
-   Risk scoring
-   Patch management

### Query
-   How risky is CVE-2025-12345?

------------------------------------------------------------------------

# Part 2 -- Implement the Tools

## Tool 1 -- CISA KEV

``` python
from langchain.tools import tool
import requests

@tool
def lookup_cisa_kev(keyword: str) -> str:
    url = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    data = response.json()

    results = []

    for item in data["vulnerabilities"]:
        text = (
            item["vendorProject"] +
            item["product"] +
            item["shortDescription"]
        ).lower()

        if keyword.lower() in text:
            results.append(
                f"CVE: {item['cveID']}\n"
                f"Vendor: {item['vendorProject']}\n"
                f"Product: {item['product']}\n"
                f"Description: {item['shortDescription']}\n"
                f"Required Action: {item['requiredAction']}"
            )

    return "\n\n".join(results) if results else "No KEV entries found."
```

------------------------------------------------------------------------

## Tool 2 -- MITRE ATT&CK

``` python
from langchain.tools import tool
import requests

@tool
def lookup_attack(keyword: str) -> str:
    url = "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json"

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    data = response.json()

    results = []

    for obj in data["objects"]:
        if obj.get("type") != "attack-pattern":
            continue

        if keyword.lower() in obj.get("name","").lower():
            results.append(
                f"Technique: {obj['name']}\n"
                f"Description: {obj.get('description','')[:400]}"
            )

    return "\n\n".join(results[:5]) if results else "No ATT&CK technique found."
```

------------------------------------------------------------------------

## Tool 3 -- EPSS

``` python
from langchain.tools import tool
import requests

@tool
def lookup_epss(cve: str) -> str:
    url = f"https://api.first.org/data/v1/epss?cve={cve}"

    response = requests.get(url, timeout=20)
    response.raise_for_status()

    data = response.json()

    if not data["data"]:
        return "No EPSS score available."

    result = data["data"][0]

    return (
        f"CVE: {result['cve']}\n"
        f"EPSS Score: {result['epss']}\n"
        f"Percentile: {result['percentile']}"
    )
```

------------------------------------------------------------------------

# Part 3 -- Integration Task

Modify the existing Agentic Cyber Security Assistant v2.1 by:

1.  Registering the three new tools.
2.  Updating the Planner Agent so it can decide when each tool is
    required.
3.  Updating the routing logic to invoke the appropriate tool(s).
4.  Updating the Validation Agent to merge outputs from all executed
    tools.
5.  Add a Report Agent to include:
    -   Relevant CVEs
    -   CISA KEV findings
    -   MITRE ATT&CK techniques
    -   EPSS scores
    -   Final recommendations

------------------------------------------------------------------------

# Part 4 -- Test Cases

  -----------------------------------------------------------------------
  \#             Test Query
  -------------- --------------------------------------------------------
  1              Show known exploited vulnerabilities affecting Windows
                 SMB.

  2              Explain the MITRE ATT&CK technique for Pass-the-Hash.

  3              What is the EPSS score for CVE-2021-44228?

  4              Secure Apache HTTP Server and include recent CVEs, KEV
                 entries, and ATT&CK techniques.

  5              How should I harden OpenSSH considering current
                 vulnerabilities and attacker techniques?

  6              Prepare a risk assessment for Microsoft Exchange Server
                 using CIS guidance, CVEs, KEV, and EPSS.

  7              Identify actively exploited vulnerabilities affecting
                 VMware ESXi.

  8              Show MITRE ATT&CK techniques related to ransomware.

  9              Prioritize patching for CVE-2023-34362 using its EPSS
                 score.

  10             Generate a complete security assessment for Windows SMB
                 including CIS recommendations, CVEs, KEV, MITRE ATT&CK,
                 and EPSS information.
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# Deliverables

Students should submit:

-   Updated source code
-   Updated agent flow
-   Screenshots of successful execution
-   Outputs for all 10 test cases
-   A short report describing how the new tools improve the overall
    cybersecurity assistant
