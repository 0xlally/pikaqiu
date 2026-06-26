# Playwright Verification

An HTTP response proves server output only. Use Playwright to prove browser semantics and impact for:

- DOM source/sink flows, postMessage, frontend routing, storage, and `window.name`.
- Event triggering, focus/click/toggle/animation/media error behavior.
- CSP, Trusted Types, sandbox, iframe, mXSS, and DOMPurify behavior.
- File upload previews, Markdown/HTML renderers, and admin preview pages.
- Local approximation of admin bot, report, share, or review flows.

## Evidence Checklist

Keep as much as possible:

- Final URL, status code, response headers, and decisive response snippets.
- Console, dialog, pageerror, request/response, and request failure logs.
- CSP, Trusted Types, and sandbox errors.
- DOM snippet after JavaScript execution.
- `document.title`, `window.xss_proof`, DOM markers, and same-origin state changes.
- Resource requests, especially script, image, connect, frame, and form requests.
- For bot cases: callback, challenge response, same-origin readable state change, or flag.

## Minimal Template

```javascript
import { chromium } from "playwright";

const url = process.argv[2];
const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();

page.on("console", msg => console.log("[console]", msg.type(), msg.text()));
page.on("dialog", async dialog => {
  console.log("[dialog]", dialog.type(), dialog.message());
  await dialog.accept().catch(() => {});
});
page.on("pageerror", err => console.log("[pageerror]", err.message));
page.on("requestfailed", req => console.log("[requestfailed]", req.url(), req.failure()?.errorText));
page.on("response", res => {
  const type = res.request().resourceType();
  if (["document", "script", "img", "fetch", "xhr", "frame"].includes(type)) {
    console.log("[response]", res.status(), type, res.url());
  }
});

await page.goto(url, { waitUntil: "networkidle", timeout: 15000 });
await page.waitForTimeout(1000);

console.log("[title]", await page.title());
console.log("[proof]", await page.evaluate(() => ({
  href: location.href,
  title: document.title,
  xssProof: window.xss_proof ?? null,
  body: document.body?.outerHTML.slice(0, 1000) ?? "",
})));

await browser.close();
```

## DOM Source/Sink Verification

Change only one source at a time:

```text
location.hash
location.search
window.name
postMessage
localStorage/sessionStorage
API response
uploaded file metadata
```

Record the source-to-sink chain:

```text
source:
transform:
sink:
final_dom:
runtime_signal:
blocked_by:
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

## CSP / Trusted Types / Sandbox

Collect:

- Full CSP header/meta.
- `script-src`, `script-src-elem`, `script-src-attr`, `base-uri`, `object-src`, `frame-src`, `connect-src`, and `form-action`.
- Script nonce/hash values, meta CSP, sandbox flags, and iframe origin.
- Whether Trusted Types is enabled, policy names, wrappers, and sanitizer behavior.

Judge carefully:

- No callback does not mean no execution; `connect-src` or outbound networking may be blocked.
- No dialog does not mean no execution; dialog tokens may be filtered or APIs may be overwritten.
- Without `allow-scripts`, do not claim JavaScript execution in a sandbox.
- Without `allow-same-origin`, code may execute but fail to read same-origin secrets.

## Admin Bot

Local Playwright only proves the route; it is not equivalent to the real bot. Final evidence must come from:

- Bot callback.
- Challenge response.
- Same-origin readable state change.
- Admin-only content.
- Flag or challenge-defined success text.

If outbound connections are blocked, prefer same-origin readable locations: profile, draft, logs, notifications, report result, or webhook history.
