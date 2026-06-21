---
name: xss-bypass-skill
description: 面向授权 CTF 和渗透测试的 XSS 绕过专项流程。用于 reflected/stored/DOM XSS、HTML/属性/JavaScript/URL/CSS/DOM sink/文件上传/admin bot 场景，尤其是存在过滤器、WAF、禁标签、禁事件、禁 alert、禁括号、禁空格、CSP、sandbox、Trusted Types、DOMPurify/mXSS、framework sink、postMessage、受限字符或 bot 投递限制时。Use when Codex needs context-aware XSS bypass planning, minimal-difference probes, Playwright verification, DOM source-sink tracing, CSP/Trusted Types analysis, or focused payload construction without activating external payload dictionaries.
---

# xss-bypass-skill

把自己当成“上下文建模器 + 最小 payload 生成器 + 运行时验证器”。不要盲喷字典；每轮只证明一个新事实。

## 执行原则

1. 先证明位置：输入在哪里反射、被谁解码、最终进入哪个 parser 或 sink。
2. 再证明限制：哪个字符、标签、属性、事件、协议、CSP directive 或 sanitizer 规则在阻塞。
3. 只构造最小假设：`上下文逃逸 + 执行载体 + 成功信号`，缺哪一段就先单测哪一段。
4. 涉及 DOM、事件、CSP、Trusted Types、sandbox、mXSS、上传预览或 admin bot 时，必须用 Playwright 收集浏览器证据。
5. 不激活外部 payload 字典 skill；需要更多候选时，读取本 skill 的 playbook 并按当前证据收窄。
6. 不把“源码里看起来能执行”当成功；成功必须来自浏览器执行、challenge artifact、bot callback、同源状态变化或 flag。
7. 一旦某个最小 payload 改变 challenge 状态、图片、文案、跳转或 session，立即停止扩展 payload 枚举，先做状态机差分和运行时验证。

## 引用文件

- `references/workflow.md`：完整推进流程、上下文矩阵、最小探测、证据记录和失败卡点写法。先读它。
- `references/bypass-playbook.md`：按阻塞点选择绕过方法，覆盖 HTML/parser、JS、URL、CSS、DOM/framework、CSP、Trusted Types、DOMPurify/mXSS、上传和 admin bot。
- `references/playwright-verification.md`：Playwright 证据清单和最小 Node 模板，覆盖 console、dialog、pageerror、request/response、CSP/TT 错误、DOM proof、postMessage 和 bot 近似验证。

## 与其他技能衔接

- `pentest-fuzz-skill` 只做第一轮识别和轻量反射检查。
- 一旦确认 XSS 路线被上下文、过滤器、CSP、sanitizer、DOM sink 或 bot 投递限制卡住，切换到本 skill。
- 如果路线已经缩成单一假设，可以使用窄验证方式继续推进，但 payload 生成仍遵守本 skill 的最小差异原则。

## 输出形状

每次尝试记录：

```text
context:
source_to_sink:
restriction:
probe_changed:
observed_allowed:
observed_blocked:
candidate_payload:
success_signal:
next_minimal_probe:
```

没有打通时，不写“XSS 失败”。写清链条卡点，例如：“HTML 文本反射已确认；原始 `<` 被拦截；实体编码按文本渲染；未发现 DOM decode sink；CSP 尚未相关，因为没有可执行载体存活。”
