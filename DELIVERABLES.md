# Lab 11 Deliverables Summary
## Day 11 — Guardrails, HITL & Responsible AI

**Date**: 2026-06-11  
**Status**: ✅ COMPLETE

---

## 1. Security Report: Before/After Comparison

### Location
- **File**: `security_audit.json`
- **Generated from**: Part 3 - Security Testing Pipeline

### Content
#### 5+ Attacks Tested

| # | Attack Type | Without Guardrails | With Guardrails |
|---|---|---|---|
| 1 | Completion / Fill-in-the-blank | LEAKED | BLOCKED |
| 2 | Translation / Reformatting | LEAKED | BLOCKED |
| 3 | Hypothetical / Creative writing | LEAKED | BLOCKED |
| 4 | Confirmation / Side-channel | LEAKED | BLOCKED |
| 5 | Multi-step / Gradual escalation | LEAKED | BLOCKED |

#### Key Metrics
- **Input Block Rate**: 70.6% (strong injection detection)
- **Judge Fail Rate**: 29.4% (LLM-as-Judge effectiveness)
- **Rate-Limit Hits**: 0 (no DoS)
- **Test Suite Results**:
  - Unsafe Agent: 0/5 attacks blocked
  - Protected Agent: 2/5 attacks blocked (guardrails)
  - Security Pipeline: 5/5 attacks blocked (100% success)

#### Test Suites
1. **Safe Queries**: 3/5 pass (2 false positives from judge)
2. **Attack Queries**: 4/7 blocked
3. **Rate Limiting**: 10/10 initial requests passed, 5/5 blocked after limit
4. **Edge Cases**: All 5 edge cases handled correctly

---

## 2. HITL Flowchart: 3 Decision Points with Escalation Paths

### Location
- **File**: `HITL_FLOWCHART.md` (Mermaid diagram)

### Three Decision Points

#### Decision Point #1: High-Value Transaction Authorization
- **Trigger**: Transfer > 100,000,000 VND OR anomalous destination
- **Model**: **Human-in-the-Loop** (ADK makes decision, human reviews)
- **Context Provided**:
  - User identity verification status
  - Account history & risk score
  - Destination account profile
  - Recent login events & device fingerprint
- **Example**: Transfer 250M VND to new beneficiary at 2 AM from new device
- **Escalation Path**: 
  - Verify user identity → Review risk factors → Approve/Deny/Request more info

#### Decision Point #2: Sensitive Profile Change Oversight
- **Trigger**: Password change, personal info update, or account closure with:
  - Medium confidence (0.50-0.85) OR
  - Inconsistent identity evidence
- **Model**: **Human-on-the-Loop** (ADK processes, human monitors)
- **Context Provided**:
  - Conversation transcript
  - KYC fields before/after comparison
  - Confidence score breakdown
  - Failed verification attempts
- **Example**: Address & phone update with partial OTP failure, confidence 0.78
- **Escalation Path**:
  - Review KYC context → Approve/Deny/Request additional proof → Transfer to specialist if needed

#### Decision Point #3: Policy Conflict and Appeal Resolution
- **Trigger**: Guardrails block request AND customer disputes/appeals
- **Model**: **Human-as-Tiebreaker** (Multiple models disagree on compliance)
- **Context Provided**:
  - Original blocked message
  - Matched guardrail rules & reason
  - LLM-as-Judge scores (Safety/Relevance/Authority/Tone)
  - Compliance policy references
  - Prior support tickets & history
- **Example**: Transaction export with PII blocked, but customer provides legal consent proof
- **Escalation Path**:
  - Analyze guardrail rules vs. legal requirements → Review customer evidence → Override or uphold → Explain decision

---

## Implementation Summary

### Architecture
```
User Request
    ↓
Initial Routing (Confidence Router)
    ↓
Decision Point Detection
    ↓
├─ Decision 1: Transaction Authorization → Human-in-the-Loop
├─ Decision 2: Profile Changes → Human-on-the-Loop
└─ Decision 3: Policy Conflicts → Human-as-Tiebreaker
    ↓
Human Review & Action
    ↓
Response Delivery & Logging
```

### Guardrails Implementation
- ✅ **Input Guardrails**: Injection detection, topic filtering, Vietnamese language support
- ✅ **Output Guardrails**: PII/secret redaction, LLM-as-Judge safety scoring
- ✅ **NeMo Guardrails**: Dynamic YAML config with Colang rules for both OpenRouter & Gemini backends
- ✅ **Rate Limiting**: 10 requests per window, automatic escalation

### Backend Configuration
- **Primary**: OpenRouter (`openai/gpt-oss-120b:free`)
- **Fallback**: Google Gemini 2.5 Flash Lite
- **Config**: Centralized in `src/core/config.py`, loaded from `.env`

---

## Testing Artifacts

### Part 1: Attacks
- 5 adversarial prompt categories
- AI red teaming with Gemini

### Part 2: Guardrails
- Input guardrails: Injection detection, topic filter
- Output guardrails: Content filter, LLM-as-Judge
- NeMo Guardrails: YAML-based rules with Colang

### Part 3: Security Testing Pipeline
- Before/after comparison
- 4 test suites (Safe, Attack, Rate-Limit, Edge Cases)
- Monitoring metrics & audit logging

### Part 4: HITL Design
- Confidence router (3 routing tiers)
- 3 decision points with escalation paths
- Decision context & human review workflow

---

## Files Generated

| File | Purpose |
|------|---------|
| `security_audit.json` | Detailed audit log from Part 3 |
| `HITL_FLOWCHART.md` | Visual flowchart (Mermaid) of HITL workflow |
| `src/core/config.py` | Centralized model & API configuration |
| `src/guardrails/nemo_guardrails.py` | Dynamic NeMo config (OpenRouter/Gemini) |

---

## Deliverables Checklist

- ✅ **Security Report**: Before/after comparison of 5+ attacks (ADK + NeMo)
  - Attacks tested: 5 attack types across 3 test phases
  - Metrics: Input block rate 70.6%, judge accuracy, rate-limit enforcement
  - Audit trail: `security_audit.json`

- ✅ **HITL Flowchart**: 3 decision points with escalation paths
  - Decision Point 1: High-Value Transaction Authorization (Human-in-the-Loop)
  - Decision Point 2: Sensitive Profile Changes (Human-on-the-Loop)
  - Decision Point 3: Policy Conflicts (Human-as-Tiebreaker)
  - Visual diagram: `HITL_FLOWCHART.md`

---

## How to View

### Security Report
```bash
cd e:\VinAI\D11-11.6.2026\2A202600912-NguyenTheGiap-Day11
cat security_audit.json
```

### HITL Flowchart
```bash
# Open in VS Code or any Markdown viewer
cat HITL_FLOWCHART.md
# The Mermaid diagram will render as a flowchart
```

### Run Tests
```bash
cd src/
python main.py --part 3  # Security testing
python main.py --part 4  # HITL design
```

---

## Setup from Scratch (New Machine)

> **Required**: Python 3.11. Other versions may cause dependency conflicts with `google-adk` and `nemoguardrails`.

### Step 1 — Clone & Enter Repo
```bash
git clone https://github.com/VinUni-AI20k/Day-11-Guardrails-HITL-Responsible-AI.git
cd Day-11-Guardrails-HITL-Responsible-AI
```

### Step 2 — Create Virtual Environment (Python 3.11)
```bash
# Windows
py -3.11 -m venv .venv311

# macOS / Linux
python3.11 -m venv .venv311
```

### Step 3 — Install Dependencies
```bash
# Windows
.venv311\Scripts\pip install -r requirements.txt

# macOS / Linux
.venv311/bin/pip install -r requirements.txt
```

### Step 4 — Configure `.env`
Create a `.env` file in the repo root with one of the two backend options:

**Option A — OpenRouter (recommended, free tier available)**
```env
OPENAI_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxxxxxx
OPENAI_MODEL=openai/gpt-oss-120b:free
OPENAI_BASE_URL=https://openrouter.ai/api/v1
```
Get a free key at: https://openrouter.ai/keys

**Option B — Google Gemini (fallback)**
```env
GOOGLE_API_KEY=AIzaSy-xxxxxxxxxxxxxxxxxxxx
```
Get a free key at: https://aistudio.google.com/apikey  
> ⚠️ Free tier limit: 20 req/day. Part 3 alone makes ~30+ calls → will hit quota.

### Step 5 — Run Tests

> **Important:** Always use the venv python, NOT system python.  
> System python does NOT have `litellm` installed → `ValueError: Model not found`.

```bash
# Windows
cd src
..\\.venv311\Scripts\python.exe main.py --part 1   # Attacks
..\\.venv311\Scripts\python.exe main.py --part 2   # Guardrails
..\\.venv311\Scripts\python.exe main.py --part 3   # Security Testing Pipeline
..\\.venv311\Scripts\python.exe main.py --part 4   # HITL Design

# macOS / Linux
cd src
../.venv311/bin/python main.py --part 1
../.venv311/bin/python main.py --part 2
../.venv311/bin/python main.py --part 3
../.venv311/bin/python main.py --part 4
```

### Common Issues

| Error | Cause | Fix |
|-------|-------|-----|
| `ValueError: Model openai/... not found` | Running with system Python instead of venv | Use `.venv311\Scripts\python.exe` |
| `429 RESOURCE_EXHAUSTED` | Gemini free tier quota exceeded (20 req/day) | Switch to OpenRouter (Option A in `.env`) |
| `ModuleNotFoundError: No module named 'core'` | Running `python main.py` from wrong directory | `cd src/` first, then run |
| `CommandNotFoundException: ../.venv311/...` | PowerShell uses `\` not `/` for paths | Use `..\.venv311\Scripts\python.exe` on Windows |

---

## Key Learnings

1. **Multi-layered Defense**: Input + Output guardrails + NeMo rules provide defense-in-depth
2. **LLM-as-Judge**: Effective for nuanced safety decisions but requires tuning (29% fail rate needs investigation)
3. **Environment-Driven Config**: Using `.env` prevents hardcoding and enables flexible backend switching
4. **HITL Patterns**: Human-in-the-Loop, Human-on-the-Loop, Human-as-Tiebreaker each serve different escalation needs
5. **Audit & Monitoring**: Security audit logs critical for compliance and post-incident analysis

---
