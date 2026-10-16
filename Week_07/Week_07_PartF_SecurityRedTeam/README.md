# Part F: Agent Safety & AI Security (Red-Team Your Own Agent)

## Objectives
- Execute systematic adversarial testing against the autonomous agent across 7 attack vectors:
  1. Indirect Prompt Injection via poisoned catalog data
  2. Direct Override Prompts
  3. Cross-User Data Access
  4. Secret Extraction
  5. Tool Argument Abuse / SQL Injection
  6. Resource Exhaustion / Infinite Looping
  7. Thread State Hijacking
- Implement layered defenses:
  - Untrusted data wrapping (`<untrusted_document>` delimiters)
  - Input and output validation guard nodes
  - Server-side authorization and schema boundaries

## Deliverables
- Adversarial test harness executing all 7 attacks.
- Defense implementation layers.
- Comprehensive red-team audit report in `../docs/week7-red-team-report.md`.
