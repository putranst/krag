# PDPA + IRB Compliance Model

> Compliance is not a checkbox. It is an architectural constraint that shapes every component in the system.

---

## 1. PDPA Data Classification

Four levels, enforced at ingest time and runtime:

| Level | Examples | Cloud escalation | Retention |
|---|---|---|---|
| **PUBLIC** | Published research papers, anonymised aggregate statistics, open datasets | Permitted | Indefinite |
| **INTERNAL** | Research aggregate summaries, non-PII project data, publication metadata | Permitted (anonymised) | 7 years |
| **CONFIDENTIAL** | Individual researcher profiles, grant application details, pre-publication manuscripts | Prohibited | 7 years |
| **RESTRICTED** | Participant identification numbers, interview transcripts, clinical data, IRB investigation records | Prohibited | 10 years (PDPA + IRB) |

**Enforcement points:**
- `suluh.pdpa.classify()` — every document, query, and tool output is classified
- `suluh.pdpa.mask()` — CONFIDENTIAL and RESTRICTED data is masked before any further processing
- The PDPA classification is the **first gate** in the query router. RESTRICTED queries never leave the intranet regardless of any other condition.

**Failure mode: fail-closed.** If `suluh.pdpa` errors for any reason, the query is blocked with an audit log entry. No data passes unmasked.

---

## 2. IRB Research Ethics Controls

| Control point | Implementation | Trigger |
|---|---|---|
| **Pre-screen classifier** | Fine-tuned Qwen 3.6 classifier on 5 research types | Every query before routing |
| **Protocol matcher** | Deterministic matcher cross-references against approved IRB protocols in DB | When human-subject indicators detected |
| **Ethics gate node** | LangGraph hard stop: workflow pauses; human reviewer notified | Unmatched or expired protocol |
| **Post-hoc audit sampler** | Random 10% sample of all agent workflows reviewed weekly | Scheduled weekly |
| **Emergency stop** | One-click kill switch in Admin Console: blocks all human-subject workflows | On IRB officer demand |

**The five research types** for the Phase 0 IRB prototype are identified by the UPSI IRB Chair in Week 1. They will be among:

- Survey research (questionnaires, interviews)
- Clinical / medical research (patient data)
- Educational research (student data, classroom observation)
- Indigenous community research (adat, customary knowledge)
- Vulnerable population research (children, elderly, prisoners)

**The five-question pre-screen:**
1. Does the research involve human participants (directly or via their data)?
2. Does it involve identifiable personal information?
3. Does it involve sensitive categories (health, religion, ethnicity, political opinion)?
4. Does it involve vulnerable populations?
5. Has an IRB protocol been approved for this research type?

Any "yes" on (1), (2), or (3) without an approved protocol → IRB gate.

---

## 3. The dual-gate model

```
Query enters
    │
    ▼
[PDPA Gate]     ←  always runs first; data classification
    │
    ├── RESTRICTED → local only, no cloud
    │
    ▼
[IRB Gate]      ←  runs second; human-subject research check
    │
    ├── Human-subject + approved protocol → pass
    ├── Human-subject + no protocol → block, human review
    └── Non-human-subject → pass
    │
    ▼
[Routing]       ←  only reached if both gates pass
```

Both gates are **deterministic** in their decisions, even when the underlying classifiers are LLM-based. The LLM produces a classification, but the decision rule is a Python function, not a model output. This is non-negotiable.

---

## 4. Audit log events (immutable)

The `ai_audit_log` PostgreSQL table has the following structure. Retention is enforced by trigger; UPDATE and DELETE are rejected.

| Event | Retention | Key fields |
|---|---|---|
| AI query submitted | 7 years | user_id_hash, role, query_hash, routing_label, model, confidence, escalated, latency_ms |
| SQL statement generated & executed | 7 years | query_id, sql_hash, tables_referenced, execution_time_ms, rows_returned |
| Agent swarm invoked | 7 years | swarm_id, agent_list, task_decomposition, consensus_method, execution_time_ms |
| Escalation to Anthropic API | 7 years | query_id, classification_check_pass, anonymization_method, escalation_reason |
| PDPA PII detection event | 10 years | query_id, entity_types_detected, masking_applied, direction (input/output) |
| IRB ethics gate event | 10 years | query_id, risk_classification, protocol_matched, gate_decision, reviewer_id_hash |
| Document ingested / lifecycle changed | 7 years | document_id, file_hash, docling_confidence, new_state, actor_user_hash |
| Routing configuration changed | 7 years | changed_by_user_hash, old_config_hash, new_config_hash, timestamp |
| Failed authentication attempt | 3 years | source_ip_hash, attempted_role, failure_reason, timestamp |

**`user_id_hash` and `source_ip_hash`** are SHA-256 with per-deployment salts. Plaintext identifiers are never logged.

---

## 5. Network perimeter

- The EXO cluster, AI read replica, MinIO, Redis, and LangFuse are on the institution's intranet. They accept connections only from the AI gateway subnet.
- Edge DGX Spark nodes (when deployed) are on isolated faculty VLANs with firewall rules permitting only gateway-subnet outbound connections.
- The FastAPI AI gateway is accessible from the campus network and VPN only — never internet-facing.
- The only permitted outbound internet connection is HTTPS to api.anthropic.com from the quality router, and only when all conditions (anonymised + non-human-subject + low confidence) are met.
- All intra-service communication uses TLS 1.3. No plaintext HTTP on internal segments.

---

## 6. What "compliant by architecture" means in practice

Compliance is enforced in **application code**, not configuration. A misconfigured environment variable cannot bypass a compliance check. Examples:

- The PDPA classification gate is a Python function in `suluh.pdpa.gate()`, not a config value
- The IRB gate is a LangGraph node in the workflow graph, not a runtime toggle
- The RESTRICTED-data cloud-escalation block is a hard `if/raise` in `suluh.router.route()`, not a feature flag
- The audit log immutability is a PostgreSQL trigger, not application logic

If a compliance check needs to be disabled for testing, it requires a `SULUH_TEST_MODE=1` environment variable AND the test instance is on a separate network with synthetic data only.

---

## 7. The annual compliance attestation

Every 12 months, the Compliance & Ethics Forum reviews:
- All audit log events from the past year
- A random 5% sample of agent workflows (full trace review)
- The classification accuracy of the PDPA and IRB classifiers
- Any PDPA or IRB gate failures and their root causes
- Any unauthorised access attempts

The result is a written attestation signed by the IRB Chair, the Legal/Compliance lead, and the Lead Architect. This document is filed with the DVC R&I.

---

*This document is the operational reference for compliance. It is referenced by the architecture doc, the principles doc, and the test plan. Any change to the compliance model requires a Steering Committee vote.*
