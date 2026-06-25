---
name: ssti-bypass-skill
description: 面向授权 CTF/渗透测试的 SSTI 服务端模板注入专项技能。用于 Jinja2/Django/Mako/Tornado、Twig/Smarty/Blade/Latte、FreeMarker/Velocity/SpEL/OGNL/Thymeleaf/Pebble/Jinjava、EJS/Pug/Handlebars/Nunjucks/Lodash、ERB/Slim/Liquid、Razor/ASP.NET、Go template、EEx 等模板引擎的注入确认、引擎指纹、过滤绕过、sandbox escape、文件读写、配置泄露、盲注/time/OOB/RCE 验证。Use when Codex needs focused SSTI bypass planning, minimal high-signal probes, template engine identification, server-side exploitation, or payload construction without broad dictionary spraying.
---

# ssti-bypass-skill

目标：绕过限制并执行 SSTI，把模板求值原语升级成信息泄露、文件读取、命令执行或 flag 获取。

## 最小思路

1. 证明输入进入服务端模板源码或表达式，而不只是普通 HTML/JSON 反射。
2. 判断大致上下文、模板引擎和过滤条件，选最短可求值 payload。
3. 将求值原语升级为读配置、读源码、读文件、执行命令、OOB 或题目成功分支。
4. 碰到过滤、sandbox、无回显或引擎差异时，读 `references/bypass-playbook.md` 选对应绕过。

主文件只给方向，不限制具体打法；按现场证据自由组合 payload 和验证方式。
