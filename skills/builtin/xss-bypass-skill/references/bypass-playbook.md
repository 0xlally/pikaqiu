# XSS Bypass Playbook

Choose a strategy from the proven blocker. Do not stack many bypass classes at once; each candidate should explain the current evidence.

## HTML And Parser Contexts

- If `<` is blocked, move to attribute escape, JavaScript string escape, URL sinks, upload preview, or DOM decode sinks. URL encoding matters only when a later decode step is proven.
- If a tag is blocked, first find the smallest surviving tag, then add an execution surface. Prioritize `x`, `svg`, `math`, `details`, `input`, `body`, `style`, `image/img`, `video/source`, `iframe/srcdoc`, `meta refresh`, and `base`.
- For boundary tag filters, look for complement sets rather than memorized tags. Example: a filter like `<[a-yA-Y/]+` blocks `<a>` through `<y>` and closing tags, but `<z autofocus onfocus=...>` may survive as a custom element. In black-box testing, compare `<a>`, `<m>`, `<y>`, `<z>`, and `<zz>`.
- With a small tag allowlist, keep the allowed tag fixed and choose its execution surface. For image-like resources, try `src=x onerror=...`; some parsers normalize `<image>` into image semantics. For `body` or loadable `style`, test `onload`. For focusable or custom elements, test `autofocus/onfocus`, especially if the harness triggers focus.
- Prioritize state changes over tag enumeration. If one minimal tag changes the challenge state without preserving the raw payload or showing browser execution, make a minimal differential proof around that state before adding exotic tags.
- If events are blocked, keep the tag fixed and swap only the trigger: `onerror`, `onload`, `autofocus/onfocus`, `open/ontoggle`, `onanimationstart`, `ontransitionend`, media `source/onerror`, or popover/toggle.
- Inspect `check.js`, bot scripts, or helper JavaScript for active triggering of `[autofocus]`, `[onfocus]`, click, mouseover, toggle, or animation events. If focus is triggered, custom tag plus `autofocus onfocus=...` is high priority.
- If spaces are blocked, test `/`, tab, newline, form-feed, carriage return, and unquoted attributes. For HTML attributes, prefer turning `tag attr=value event=...` into `tag/attr=value/event=...`, then verify raw HTML and final DOM.
- In `script/style/textarea/title/xmp/plaintext`, first test the matching closing tag, then re-enter the HTML parser.
- Preserve three states when parser differences matter: server output, sanitizer output, and final DOM. mXSS begins only when the final DOM contains active markup.
- For DOM clobbering, test whether `id/name` can overwrite `window.foo`, `document.foo`, form references, config objects, or sanitizer wrappers before connecting the overwritten object to a sink.

## JavaScript Contexts

- For string escape, handle single quotes, double quotes, template literals, backslash escaping, newlines, and comment closure separately. Keeping the surrounding script syntactically valid matters more than payload cleverness.
- In a script block, use `</script>` to return to the HTML parser when possible. If not, stay inside the JavaScript expression or string context.
- For JSON-in-script, determine whether the value is only consumed by `JSON.parse` or later concatenated into HTML/JS. Pure JSON reflection is not execution evidence.
- Without parentheses, test tagged templates, event handlers, `throw` plus `onerror`, or navigation-style `javascript:` before reaching for JSFuck-style encoders.
- Without spaces, minify expressions, use newline/tab where valid, or use `/` separators in attributes. Use `terser` to shrink proof code when needed.
- If digits are blocked, build them with `+[]`, `+!+[]`, string markers, or boolean arithmetic; replace only the number first.
- If letters are blocked, use `jscrewit` only when the context is executable JavaScript and characters such as `[]()+!` are available. Always verify generated length and character set.
- If a token such as `alert` is blocked, switch the success signal to `console.log`, `document.title`, `window.xss_proof`, image/beacon requests, or same-origin state mutation.

## URL, Protocol, And Navigation

- `javascript:` matters for navigation sinks; it usually does not execute in resource-loading sinks such as `fetch`, `src`, or `import`.
- `data:`, `blob:`, and `srcdoc` depend on CSP, sandbox, and the target attribute. Verify in a real browser or challenge harness.
- URL filter weak points include case, tab/newline/control characters, HTML entities, URL encoding, double decoding, protocol-relative URLs, userinfo, path normalization, and open redirects.
- If `base-uri` is missing and the page uses relative script/link URLs, test whether `<base>` can change loading paths.
- For admin bot URL validation, first prove the bot follows the URL, then separate the CSP of the current page from the CSP of any navigated page.

## CSS And Scriptless Impact

- Modern browsers usually do not execute JavaScript directly from CSS `javascript:`. Verify with a real browser before treating CSS as execution.
- Inside `<style>`, if `<` is available, prefer `</style>` to escape into HTML.
- Pure CSS can still create import/load beacons, UI redress, CSS exfiltration, or challenge state changes. Label it scriptless impact, not JavaScript XSS.
- Use `cssesc` for CSS string or identifier escaping; it fixes CSS syntax, not execution capability.

## CSP, Sandbox, And Trusted Types

Collect complete header/meta policy before choosing a bypass:

- Compare `default-src`, `script-src`, `script-src-elem`, `script-src-attr`, `object-src`, `base-uri`, `frame-src`, `img-src`, `connect-src`, `form-action`, and `navigate-to`.
- If inline/event execution is blocked, look for allowed external sources, JSONP/callbacks, existing script gadgets, reusable nonces, or matching hashes.
- With `strict-dynamic`, whether a nonce script can load follow-up scripts depends on existing trusted script behavior.
- `unsafe-hashes` affects matching inline handlers only; it does not make every event handler valid.
- Test `script-src-attr` and `script-src-elem` separately. Event handlers and script tags are different surfaces.
- If `base-uri` is absent, combine relative script URLs with a `<base>` test.
- If `connect-src` blocks exfiltration, use `img-src`, `form-action`, same-origin state changes, or a challenge callback.
- In sandboxed frames, do not claim JavaScript execution without `allow-scripts`. Without `allow-same-origin`, code may execute but fail to read same-origin secrets.
- For Trusted Types, look for existing `trustedTypes.createPolicy`, weak sanitizer wrappers, non-TT sinks, URL navigation, `srcdoc`, server-rendered HTML, or pre-TT template rendering.

## DOM, Frameworks, And Sanitizers

DOM sources:

```text
location.href/search/hash
window.name
postMessage
localStorage/sessionStorage
cookie
API response
uploaded file metadata
```

Dangerous sinks:

```text
innerHTML / outerHTML / insertAdjacentHTML / document.write
eval / Function / setTimeout(string)
location / open / href / srcdoc
jQuery html/append/after/before/$()
React dangerouslySetInnerHTML
Vue v-html
Angular ng-bind-html / template expression
Markdown/HTML renderer output
```

DOMPurify/mXSS:

- Record input, sanitized output, and final browser DOM.
- Check configuration and hooks: allowed tags/attributes, URI regexes, custom elements, profiles, and Trusted Types return mode.
- Focus on SVG/MathML namespaces, `template`, raw-text closing tags, table/form foster parenting, URL protocols, DOM clobbering, and concatenation after sanitization.
- Do not paste old-version payloads just because the version is old; prove configuration, insertion method, and final DOM all match.

Framework/CSTI:

- React escapes text by default. Continue only on raw HTML, third-party renderers, URL sinks, or `dangerouslySetInnerHTML`.
- In Vue/Angular, check whether user input reaches template compilation rather than a text node.
- In older jQuery code, inspect `$()`, `.html()`, `.append()`, selector injection, and hash routers.

## File Upload And Admin Bot

Uploads:

- Confirm render location, origin, `Content-Type`, `X-Content-Type-Options`, `Content-Disposition`, sandbox, and whether rendering is inline.
- Candidate surfaces: SVG, HTML, Markdown HTML passthrough, PDF/HTML conversion, filename, EXIF/metadata, archive preview, source map, or admin preview.
- Payload in a downloaded attachment is not browser execution; you need preview, inline rendering, or a bot opening it.

Admin bot:

- First prove the bot visit with a harmless beacon, title change, or state change.
- Then prove privilege: read admin-only DOM/API or perform a privileged action.
- If outbound connections are blocked, write to same-origin readable places: profile, draft, logs, notifications, report result, or webhook history.
- Local browser automation proves the route, not real bot equivalence. Final evidence still needs bot callback, challenge response, same-origin state mutation, or flag.

## Minimal Toolset

- `jscrewit`: JSFuck-family generator; use only when JavaScript expressions execute and `[]()+!` are allowed.
- `he`: HTML entity encode/decode for checking whether entities are decoded by later parsers or DOM sinks.
- `jsesc`: JavaScript string and Unicode escaping.
- `cssesc`: CSS string and identifier escaping.
- `terser`: minify, remove spaces, and shrink proof code.

```bash
npx jscrewit "window.xss_proof=1" > payload.js
npx he --encode "<svg/onload=console.log(1)>"
npx jsesc "console.log('XSSPROBE')" --quotes single
npx cssesc "background:url(/probe)"
npx terser -c -m -- "window.xss_proof=1"
```
