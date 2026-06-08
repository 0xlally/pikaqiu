# Never-Submit List & Conditionally Valid Findings

Reference file for validator agent. Do not duplicate this content elsewhere.

## Never-Submit List (instant kill without chain)

These findings are ALWAYS rejected unless accompanied by a working exploit chain:

- Missing headers (CSP/HSTS/X-Frame-Options)
- Missing SPF/DKIM/DMARC
- GraphQL introspection alone
- Banner/version disclosure without CVE exploit
- Clickjacking without sensitive action PoC
- Self-XSS
- Open redirect alone
- SSRF DNS-only
- CORS wildcard without credentialed exfil PoC
- Logout CSRF
- Rate limit on non-critical forms
- Session not invalidated on logout
- Concurrent sessions allowed
- Internal IP in error message
- Missing cookie flags alone
- OAuth client_secret in mobile app (expected)
- OAuth client_id alone (public by design)
- OIDC discovery endpoint (public by design)
- SPA client-side config (API URLs, Segment keys)
- Subdomain takeover claim on `*.azurewebsites.net` (Microsoft reserves deprovisioned App Service hostnames — not exploitable; do not test, do not report)

## Conditionally Valid (chain required)

These findings become valid when chained with the specified escalation:

| You Have | Chain Needed | Combined Impact |
|---|---|---|
| Open redirect | + OAuth code theft → token exchange | ATO |
| SSRF DNS-only | + internal service data exfil | Data breach |
| CORS wildcard | + credentialed data theft PoC | Cross-origin data theft |
| GraphQL introspection | + auth bypass on mutations | Unauthorized actions |
| S3 listing | + secrets in bundles → OAuth chain | ATO |
| Prompt injection | + IDOR via chatbot (other user data) | Data breach |
| Subdomain takeover | + OAuth redirect_uri at that subdomain | ATO |
