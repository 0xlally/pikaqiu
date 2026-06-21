# XSS Bypass Playbook

按“已证明的阻塞点”选择策略。不要一次叠加多类绕过；每个候选都要能解释当前证据。

## HTML 与 Parser

- `<` 被禁：转向属性逃逸、JS 字符串逃逸、URL sink、上传预览或 DOM decode sink。实体/URL 编码只有在后续解码证据存在时才有意义。
- tag 被禁：先找能存活的最小 tag，再加执行面。优先枚举 `x`、`svg`、`math`、`details`、`input`、`video/source`、`iframe/srcdoc`、`meta refresh`、`base`。
- 边界标签：如果过滤器是字母范围、首字母或黑名单正则，先求补集而不是背常见标签。例：`<[a-yA-Y/]+` 拦 `<a>` 到 `<y>` 和闭合标签，但 `<z autofocus onfocus=...>` 可作为自定义标签存活。黑盒时用 `<a>`、`<m>`、`<y>`、`<z>`、`<zz>` 做最小差异探测。
- 状态变化优先级高于标签枚举：当某个最小标签只改变 challenge 状态而没有保留原始 payload 或产生浏览器执行证据时，先围绕这个状态做最小差分；不要继续堆更多特殊标签。重点比较 raw HTML、最终 DOM、状态文本、是否有 flag、是否需要下一阶段输入或 bot/harness 触发。
- event 被禁：固定 tag 后只换触发方式。常见无交互信号包括 `onerror`、`onload`、`autofocus/onfocus`、`open/ontoggle`、`onanimationstart`、`ontransitionend`、media `source/onerror`、popover/toggle。
- 挑战 harness：检查 `check.js`、bot 脚本或页面辅助 JS 是否会主动触发 `[autofocus]`、`[onfocus]`、click、mouseover、toggle、animation 等事件。如果 harness 会触发 focus，自定义 tag + `autofocus onfocus=...` 是高优先级候选。
- 空格被禁：测试 `/`、tab、换行、form-feed、回车和无引号属性；只换分隔符，不换载体。
- raw-text/RCDATA：在 `script/style/textarea/title/xmp/plaintext` 中优先测试对应闭合标签，再进入 HTML 载体。
- parser 差异：保留“服务端输出 -> sanitizer 输出 -> 最终 DOM”三态。只有最终 DOM 产生 active markup 才算进入 mXSS 阶段。
- DOM clobbering：当代码读取 `window.foo`、`document.foo`、form/name/id、配置对象或 sanitizer wrapper 时，测试 `id/name` 是否能覆盖对象引用，再连接后续 sink。

## JavaScript 上下文

- 字符串逃逸：分别处理单引号、双引号、反引号模板、反斜杠转义、换行和注释闭合。保持原脚本语法有效比 payload 花哨更重要。
- script block：如果能写 `</script>`，可转回 HTML parser；如果不能，留在 JS 字符串/表达式内解决。
- JSON-in-script：先判断数据是否只被 `JSON.parse` 使用，还是会被拼进 HTML/JS。纯 JSON 反射不是执行证据。
- 无括号：测试 tagged template、事件 handler、`throw` + `onerror`、导航型 `javascript:`，不要一开始上 JSFuck 系。
- 无空格：优先压缩表达式、使用换行/tab 或属性 `/` 分隔；必要时用 `terser` 先缩短 proof。
- 禁数字：用 `print()`、字符串 marker、`+[]`、`+!+[]` 等构造，先只替换数字。
- 禁字母：只有 JS 表达式可执行且 `[]()+!` 等字符可用时，用 `jscrewit` 生成最小 proof，并核对长度和字符集合。
- token 被禁：`alert` 被禁时轮换到 `console.log`、`document.title`、`window.xss_proof`、image/beacon 或同源状态变化。

## URL、协议与导航

- `javascript:` 只对导航 sink 有意义；对 `fetch/src/import` 等资源加载 sink 通常不是脚本执行。
- `data:`、`blob:`、`srcdoc` 依赖 CSP、sandbox 和目标属性；必须用真实浏览器或挑战 harness 验证。
- URL 过滤弱点：大小写、tab/newline/control char、实体编码、URL 编码、双重解码、协议相对 URL、userinfo、路径归一化、open redirect。
- `<base>`：当 CSP `base-uri` 缺失且页面有相对脚本/链接时，测试 base tag 是否能改变加载路径。
- admin bot URL 校验：先证明 bot 会跟随 URL，再区分当前页面 CSP 和新导航页面 CSP。

## CSS 与 Scriptless

- 现代浏览器通常不会从 CSS `javascript:` 直接执行脚本；把 CSS 当作执行证据前必须用真实浏览器或挑战 harness 验证。
- `<style>` 内如果 `<` 可用，优先 `</style>` 逃逸到 HTML。
- 纯 CSS 可用于 import/load beacon、UI redress、CSS exfil 或触发挑战状态，但要标注为 scriptless impact，不要冒充 JS XSS。
- CSS 上下文转义用 `cssesc`，但它只解决 CSS 语法，不提供执行能力。

## CSP、Sandbox、Trusted Types

先收集完整 header/meta，再判断 directive：

- 核对 `default-src`、`script-src`、`script-src-elem`、`script-src-attr`、`object-src`、`base-uri`、`frame-src`、`img-src`、`connect-src`、`form-action`、`navigate-to`。
- inline/event 被禁：寻找允许来源外链、JSONP/callback、现有 script gadget、nonce 可复用或 hash 匹配。
- `strict-dynamic`：nonce script 是否能加载后续脚本取决于现有 trusted script 行为。
- `unsafe-hashes`：只影响匹配 hash 的 inline handler，不等于所有 event 可用。
- `script-src-attr` 和 `script-src-elem` 分开测：event handler 与 script tag 不要混为一谈。
- `base-uri` 缺失：结合相对 script URL 测 `<base>`。
- `connect-src` 禁外连：用 `img-src`、`form-action`、同源状态变化或 challenge callback 替代 exfil 信号。
- sandbox：没有 `allow-scripts` 就不要声称 JS 执行；没有 `allow-same-origin` 时执行也可能读不到同源敏感数据。
- Trusted Types：找已有 `trustedTypes.createPolicy`、弱 sanitizer wrapper、非 TT sink、URL navigation、`srcdoc`、服务端 HTML 或 TT 前模板渲染。

## DOM、Framework 与 Sanitizer

DOM source：

```text
location.href/search/hash
window.name
postMessage
localStorage/sessionStorage
cookie
API response
uploaded file metadata
```

危险 sink：

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

DOMPurify/mXSS：

- 记录 input、sanitized output、final browser DOM。
- 检查配置和 hooks：允许 tag/attr、URI 正则、自定义元素、profile、返回 Trusted Types 的方式。
- 重点方向：SVG/MathML namespace、`template`、raw-text close tag、畸形 table/form、URL protocol、DOM clobbering、sanitizer 后二次拼接。
- 不要只因为版本旧就套 payload；必须证明配置、插入方式和最终 DOM 都匹配。

Framework/CSTI：

- React 默认转义文本；只有 raw HTML、第三方 renderer、URL sink 或 dangerouslySetInnerHTML 才继续。
- Vue/Angular 看模板编译边界：用户输入是否进入模板，而不是只进入文本节点。
- jQuery 老代码重点看 `$()`、`.html()`、`.append()`、selector injection 和 hash router。

## 文件上传与 Admin Bot

上传：

- 先确认渲染位置、origin、Content-Type、`X-Content-Type-Options`、`Content-Disposition`、sandbox 和是否 inline。
- 候选面：SVG、HTML、Markdown HTML passthrough、PDF/HTML 转换、文件名、EXIF/metadata、压缩包预览、source map 或 admin preview。
- 如果只在下载附件中存在 payload，不算浏览器执行；需要 preview、inline render 或 bot 打开。

Admin bot：

- 先用无害 beacon/title/state change 证明 bot visit。
- 再证明权限：能读 admin-only DOM/API，或能执行 privileged action。
- 外连被禁时，优先写同源可回读位置：profile、draft、logs、notifications、report result、webhook history。
- 本地浏览器自动化只能证明路线，最终还要 bot callback、挑战返回、同源状态变化或 flag。

## 最小工具集

- `jscrewit`：JSFuck 系默认工具，仅在 JS 表达式可执行且允许 `[]()+!` 时使用。
- `he`：HTML entity 编解码，用于验证实体是否会被后续 parser/DOM sink 解码。
- `jsesc`：JS 字符串/Unicode 转义。
- `cssesc`：CSS 字符串/标识符转义。
- `terser`：压缩、去空格、缩短 proof。

```bash
npx jscrewit "window.xss_proof=1" > payload.js
npx he --encode "<svg/onload=console.log(1)>"
npx jsesc "console.log('XSSPROBE')" --quotes single
npx cssesc "background:url(/probe)"
npx terser -c -m -- "window.xss_proof=1"
```
