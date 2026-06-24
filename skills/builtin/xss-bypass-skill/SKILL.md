---
name: xss-bypass-skill
description: 面向授权 CTF/渗透测试的 XSS 绕过专项技能。用于 reflected/stored/DOM XSS、HTML/属性/JavaScript/URL/CSS/DOM sink/文件上传/admin bot 场景，尤其是遇到过滤器、WAF、标签/事件/alert/括号/空格限制、CSP、sandbox、Trusted Types、DOMPurify/mXSS、framework sink、postMessage、受限字符或 bot 投递限制时。Use when Codex needs focused XSS bypass planning, minimal-difference probes, browser/runtime verification, DOM source-sink tracing, or payload construction without broad external payload dictionaries.
---

# xss-bypass-skill

目标：绕过过滤和环境限制，构造能在浏览器或 bot 中执行的 XSS，并拿到可复现的运行时证据。不要喷大字典；先用小批量代表性探针快速分层，出现差异后再单变量复测归因。

## 最短闭环

1. 定位上下文：确认输入最终进入 HTML 文本、属性、JS 字符串/表达式、URL、CSS、DOM sink、上传预览还是 admin bot。
2. 确认限制：用 3-5 个代表性探针快速区分阻塞层，如 `<`、`>`、引号、空格、tag、event、protocol、CSP、TT、sanitizer 或 bot 行为。
3. 生成最小 payload：固定已允许的上下文，只替换缺失的一段：逃逸方式、执行载体、触发事件或成功信号。
4. 用浏览器验真：涉及 DOM、事件、CSP、Trusted Types、sandbox、mXSS、上传预览、admin bot 或页面成功分支时，用 Playwright 记录 dialog/console/DOM/请求/状态变化。
5. 强证据后收束：一旦 payload 改变页面状态、文案、跳转、session、bot callback 或 flag 线索，停止扩面，围绕该状态做最小差分。

## 选择引用

- 已确认上下文或阻塞点，需要构造绕过时，读 `references/bypass-playbook.md`。
- 需要证明浏览器执行、DOM 变化、事件触发、CSP/TT/sandbox 影响、上传预览或 bot 近似行为时，读 `references/playwright-verification.md`。

## 记录卡点

失败时写链条位置，不写“XSS 失败”。例如：入口已确认；反射在 HTML 属性；`>` 可逃逸但空格被删除；`/` 分隔尚未验证；`onload` 被保留但无运行时信号；下一步用 Playwright 比较最终 DOM 和事件触发。
