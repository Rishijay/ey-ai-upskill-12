
"""
mcp_cyber_tools_server.py

A simple FastMCP server exposing five cybersecurity tools:

1. CIS RAG (calls an existing Flowise Chatflow)
2. NVD CVE Lookup
3. CISA KEV Lookup
4. MITRE ATT&CK Lookup
5. EPSS Lookup

Fill in the configuration values before running.

Requirements:
    pip install fastmcp requests

Run:
    python mcp_cyber_tools_server.py
"""

import requests
from fastmcp import FastMCP

mcp = FastMCP("Cyber Security MCP Server")

# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

FLOWISE_CHATFLOW_URL = ""      # Example: http://localhost:3000/api/v1/prediction/<chatflow-id>
FLOWISE_API_KEY = ""           # Optional

NVD_API_KEY = ""               # Optional but recommended

# ---------------------------------------------------------------------
# Tool 1 : CIS RAG
# ---------------------------------------------------------------------

@mcp.tool
def ask_cis(question: str) -> str:
    """Query the existing Flowise CIS RAG chatflow."""
    if not FLOWISE_CHATFLOW_URL:
        return "FLOWISE_CHATFLOW_URL not configured."

    headers = {}
    if FLOWISE_API_KEY:
        headers["Authorization"] = f"Bearer {FLOWISE_API_KEY}"

    payload = {
        "question": question
    }

    r = requests.post(
        FLOWISE_CHATFLOW_URL,
        json=payload,
        headers=headers,
        timeout=60,
    )
    r.raise_for_status()

    data = r.json()

    if isinstance(data, dict):
        return (
            data.get("text")
            or data.get("answer")
            or data.get("response")
            or str(data)
        )

    return str(data)


# ---------------------------------------------------------------------
# Tool 2 : NVD CVE Lookup
# ---------------------------------------------------------------------

@mcp.tool
def lookup_cve(keyword: str) -> str:
    """Search NVD for CVEs matching a keyword."""

    url = "https://services.nvd.nist.gov/rest/json/cves/2.0"

    headers = {}
    if NVD_API_KEY:
        headers["apiKey"] = NVD_API_KEY

    r = requests.get(
        url,
        params={
            "keywordSearch": keyword,
            "resultsPerPage": 5
        },
        headers=headers,
        timeout=30
    )
    r.raise_for_status()

    vulns = r.json().get("vulnerabilities", [])

    if not vulns:
        return "No CVEs found."

    output = []

    for item in vulns:
        cve = item["cve"]

        output.append(
            f"""
CVE: {cve["id"]}
Description:
{cve["descriptions"][0]["value"]}
"""
        )

    return "\n".join(output)


# ---------------------------------------------------------------------
# Tool 3 : CISA KEV
# ---------------------------------------------------------------------

@mcp.tool
def lookup_cisa_kev(keyword: str) -> str:
    """Search CISA Known Exploited Vulnerabilities."""

    url = (
        "https://www.cisa.gov/sites/default/files/"
        "feeds/known_exploited_vulnerabilities.json"
    )

    r = requests.get(url, timeout=30)
    r.raise_for_status()

    data = r.json()

    results = []

    for item in data["vulnerabilities"]:

        searchable = (
            item["vendorProject"]
            + item["product"]
            + item["shortDescription"]
        ).lower()

        if keyword.lower() in searchable:

            results.append(
                f"""
CVE: {item["cveID"]}
Vendor: {item["vendorProject"]}
Product: {item["product"]}

Description:
{item["shortDescription"]}

Required Action:
{item["requiredAction"]}
"""
            )

    return "\n".join(results) if results else "No KEV entries found."


# ---------------------------------------------------------------------
# Tool 4 : MITRE ATT&CK
# ---------------------------------------------------------------------

@mcp.tool
def lookup_attack(keyword: str) -> str:
    """Search MITRE ATT&CK techniques."""

    url = (
        "https://raw.githubusercontent.com/mitre/cti/master/"
        "enterprise-attack/enterprise-attack.json"
    )

    r = requests.get(url, timeout=60)
    r.raise_for_status()

    data = r.json()

    results = []

    for obj in data["objects"]:

        if obj.get("type") != "attack-pattern":
            continue

        if keyword.lower() in obj.get("name", "").lower():

            results.append(
                f"""
Technique:
{obj["name"]}

Description:
{obj.get("description","")[:500]}
"""
            )

    return "\n".join(results[:5]) if results else "No ATT&CK technique found."


# ---------------------------------------------------------------------
# Tool 5 : EPSS
# ---------------------------------------------------------------------

@mcp.tool
def lookup_epss(cve: str) -> str:
    """Retrieve the EPSS score for a CVE."""

    url = f"https://api.first.org/data/v1/epss?cve={cve}"

    r = requests.get(url, timeout=20)
    r.raise_for_status()

    data = r.json()

    if not data["data"]:
        return "No EPSS score available."

    result = data["data"][0]

    return f"""
CVE:
{result["cve"]}

EPSS Score:
{result["epss"]}

Percentile:
{result["percentile"]}
"""


if __name__ == "__main__":
    mcp.run()
