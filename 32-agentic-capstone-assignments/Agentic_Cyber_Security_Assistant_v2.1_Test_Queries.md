# Agentic Cyber Security Assistant v2.1

## Test Queries

This document contains recommended test queries for validating Project
v2.1.

## Test Coverage

  Execution Path         Queries
  ---------------------- ---------
  RAG Only               1--2
  CVE Only               3--4
  RAG + CVE (Parallel)   5--10

## Test Cases

  ------------------------------------------------------------------------------
  \#   Test Query         Expected Planner Decision       Expected Workflow
  ---- ------------------ ------------------------------- ----------------------
  1    How do I disable   use_rag=true, use_cve=false     Planner → Retrieval →
       SMBv1 according to                                 Validation → Report
       the CIS benchmark?                                 

  2    What does CIS      use_rag=true, use_cve=false     Planner → Retrieval →
       recommend for                                      Validation → Report
       Windows password                                   
       policies?                                          

  3    Show the latest    use_rag=false, use_cve=true     Planner → Threat →
       vulnerabilities                                    Validation → Report
       affecting Windows                                  
       SMB.                                               

  4    List the latest    use_rag=false, use_cve=true     Planner → Threat →
       critical CVEs for                                  Validation → Report
       OpenSSL.                                           

  5    How can I secure   use_rag=true, use_cve=true      Planner → Retrieval +
       Windows SMB                                        Threat (Parallel) →
       against recent                                     Validation → Report
       attacks?                                           

  6    Recommend CIS      use_rag=true, use_cve=true      Planner → Retrieval +
       controls for                                       Threat (Parallel) →
       Apache HTTP Server                                 Validation → Report
       and include recent                                 
       CVEs.                                              

  7    How should I       use_rag=true, use_cve=true      Planner → Retrieval +
       harden OpenSSH                                     Threat (Parallel) →
       based on CIS                                       Validation → Report
       recommendations                                    
       and current                                        
       vulnerabilities?                                   

  8    Explain how to     use_rag=true, use_cve=true      Planner → Retrieval +
       secure Remote                                      Threat (Parallel) →
       Desktop Protocol                                   Validation → Report
       (RDP) and identify                                 
       any known                                          
       vulnerabilities.                                   

  9    What CIS           use_rag=true, use_cve=true      Planner → Retrieval +
       recommendations                                    Threat (Parallel) →
       exist for Windows                                  Validation → Report
       Firewall, and are                                  
       there any recent                                   
       Windows                                            
       Firewall-related                                   
       CVEs?                                              

  10   Prepare a security use_rag=true, use_cve=true      Planner → Retrieval +
       assessment for                                     Threat (Parallel) →
       Microsoft Exchange                                 Validation → Report
       Server including                                   
       CIS guidance and                                   
       the latest                                         
       vulnerabilities.                                   
  ------------------------------------------------------------------------------

## Expected Behaviour

### RAG Only

Planner invokes only the Retrieval Agent.

### CVE Only

Planner invokes only the Threat Intelligence Agent.

### RAG + CVE

Planner invokes both agents in parallel, followed by Validation and
Report generation.

## Features Validated

-   Planner Agent
-   Conditional Routing
-   Pinecone RAG Retrieval
-   NVD CVE Lookup
-   Parallel Agent Execution
-   Validation Agent
-   Report Generation
-   End-to-End Orchestration
