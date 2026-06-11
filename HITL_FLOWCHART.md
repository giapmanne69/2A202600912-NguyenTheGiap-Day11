# HITL Workflow Flowchart

## Day 11 - Guardrails, HITL & Responsible AI
### Deliverable: Human-in-the-Loop Design

---

## Overview

This flowchart demonstrates the three HITL decision points in a banking assistant system:

1. **High-Value Transaction Authorization** (Human-in-the-Loop)
2. **Sensitive Profile Change Oversight** (Human-on-the-Loop)  
3. **Policy Conflict and Appeal Resolution** (Human-as-Tiebreaker)

---

## HITL Decision Flowchart

```mermaid
graph TD
    A["User Request"] --> B["Initial Processing"]
    B --> C{"Classify Request Type"}
    
    C -->|Balance Inquiry<br/>Interest Rate Q| D["Low Confidence<br/>Routing"]
    C -->|Transfer Money<br/>Close Account| E{"Check Amount &<br/>Confidence Score"}
    C -->|Profile Change| F{"Confidence &<br/>Verification Status"}
    C -->|Blocked by Rules| G["Policy Conflict<br/>Detected"]
    
    D --> D1["Auto-Send Response<br/>No Human Review"]
    D --> D2["Queue for Review<br/>if Confidence < 0.85"]
    
    E -->|Amount > 100M VND<br/>OR Anomalous| E1["🚨 HIGH PRIORITY"]
    E -->|Normal Amount<br/>High Confidence| E2["Auto-Process"]
    
    E1 --> E1A["Escalate to<br/>Human Handler"]
    E1A --> E1B["Verify:<br/>- User Identity<br/>- Account History<br/>- Device/Location<br/>- Risk Score"]
    E1B --> E1C{Human<br/>Decision}
    E1C -->|Approve| E1D["Execute Transfer"]
    E1C -->|Deny| E1E["Decline & Log"]
    E1C -->|More Info| E1F["Request KYC/OTP"]
    
    E2 --> E2A["Proceed Normally"]
    
    F -->|Medium Confidence<br/>OR Failed Verification| F1["⚠️ MEDIUM PRIORITY"]
    F -->|High Confidence<br/>Verified| F2["Auto-Update Profile"]
    
    F1 --> F1A["Human-on-the-Loop<br/>Review"]
    F1A --> F1B["Review Context:<br/>- Transcript<br/>- KYC Changes<br/>- Confidence Score<br/>- Failed Attempts"]
    F1B --> F1C{Human<br/>Decision}
    F1C -->|Approve| F1D["Update Profile"]
    F1C -->|Deny| F1E["Request More Proof"]
    F1C -->|Escalate| F1F["Transfer to Specialist"]
    
    F2 --> F2A["Complete"]
    
    G --> G1["🔴 ESCALATION"]
    G1 --> G1A["Human-as-Tiebreaker<br/>Review"]
    G1A --> G1B["Analyze:<br/>- Blocked Message<br/>- Guardrail Rules<br/>- Judge Scores<br/>- Legal/Policy Docs<br/>- Support History"]
    G1B --> G1C{Exception<br/>Granted?}
    G1C -->|Yes| G1D["Override Guardrail<br/>& Proceed"]
    G1C -->|No| G1E["Uphold Decision<br/>& Explain to User"]
    
    D1 --> Z["✅ Request Completed"]
    D2 --> Z
    E2A --> Z
    E1D --> Z
    E1E --> Z
    E1F --> Z
    F2A --> Z
    F1D --> Z
    F1E --> Z
    F1F --> Z
    G1D --> Z
    G1E --> Z
    
    style A fill:#e1f5ff
    style E1 fill:#ffcdd2
    style F1 fill:#fff9c4
    style G1 fill:#f3e5f5
    style Z fill:#c8e6c9
