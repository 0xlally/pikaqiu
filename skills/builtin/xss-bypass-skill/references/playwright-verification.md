# Playwright Verification

HTTP 响应只能证明服务端输出；以下情况必须用 Playwright 证明浏览器语义和影响：

- DOM source/sink、postMessage、前端路由、storage、window.name。
- 事件触发、focus/click/toggle/animation/media error。
- CSP、Trusted Types、sandbox、iframe、mXSS、DOMPurify。
- 文件上传预览、Markdown/HTML renderer、admin preview。
- admin bot、report/share/review 流程的本地近似验证。

## 证据清单

尽量保留：

- 最终 URL、状态码、响应头和关键响应片段。
- console、dialog、pageerror、request/response、request failure。
- CSP/Trusted Types/sandbox 相关错误。
- JavaScript 执行后的 DOM 片段。
- `document.title`、`window.xss_proof`、DOM marker、同源状态变化。
- 资源请求列表，尤其是 script/img/connect/frame/form 请求。
- bot 场景下的 callback、挑战返回、同源可回读状态变化或 flag。

## 最小模板

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

## DOM Source/Sink 验证

一次只改变一个 source：

```text
location.hash
location.search
window.name
postMessage
localStorage/sessionStorage
API response
uploaded file metadata
```

记录 source 到 sink 的链条：

```text
source:
transform:
sink:
final_dom:
runtime_signal:
blocked_by:
```

危险 sink 重点看：

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

收集：

- 完整 CSP header/meta。
- `script-src`、`script-src-elem`、`script-src-attr`、`base-uri`、`object-src`、`frame-src`、`connect-src`、`form-action`。
- script nonce/hash、meta CSP、sandbox flags、iframe origin。
- Trusted Types 是否启用、policy 名称、wrapper 或 sanitizer 行为。

判断：

- 没有 callback 不等于未执行；可能是 `connect-src` 或外连被禁。
- 没有 dialog 不等于未执行；可能是 dialog token 被过滤或 API 被重写。
- 没有 `allow-scripts` 的 sandbox 不应声称 JS 执行。
- 没有 `allow-same-origin` 时，即使执行也可能读不到同源敏感数据。

## Admin Bot

本地 Playwright 只证明路线，不能直接等价真实 bot。最终证据必须来自：

- bot callback。
- challenge response。
- 同源可回读状态变化。
- admin-only 内容。
- flag 或题目定义的成功文本。

外连被禁时，优先找同源可回读位置：profile、draft、logs、notifications、report result、webhook history。
