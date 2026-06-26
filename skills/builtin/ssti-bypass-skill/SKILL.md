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
description: Focused server-side template injection skill for authorized CTF, lab, and pentest targets. Use for black-box or white-box SSTI in Jinja2/Flask render_template_string, Django Engine.from_string/from_string, Twig, Smarty, Blade, Latte, FreeMarker, Velocity, SpEL, OGNL, Thymeleaf, Pebble, Jinjava, EJS, Pug, Handlebars, Nunjucks, Lodash, ERB, Slim, Liquid, Razor/ASP.NET, Go template, EEx, and similar engines. Covers response-driven probing, complete input coverage, delayed or second render paths, session/workflow-carried input, engine fingerprinting, blacklist bypass, statement-tag payloads, sandbox escape, file/config reads, output constraints, blind time/OOB/RCE verification, and avoiding overfit payload spraying.
---

# ssti-bypass-skill

Use this skill to confirm SSTI, identify the template engine, bypass constraints, and recover a flag or command execution when the runtime evidence supports it.

## Core Objective

If SSTI exists, prove it with a stable runtime signal and exploit the shortest working path. Do not stop after one failed payload. SSTI probing needs broad input coverage, multiple syntax families, and feedback-driven narrowing.

## Operating Principles

1. Cover every plausible entry: GET/POST parameters, JSON fields, multipart fields, headers, cookies, path segments, template names, include paths, session/profile/cart/workflow state, preview pages, exports, notifications, error pages, and admin review screens.
2. Do not reject SSTI from one failed probe. A miss can mean the wrong engine, wrong context, delayed rendering, blind execution, output escaping, or a need for statement tags instead of expression tags.
3. Let the response drive the next step: evaluated numbers, template errors, object expansion, forbidden characters, raw reflection, format validation errors, timing differences, and out-of-band effects each imply a different branch.
4. Start with a compact probe matrix across syntax families, then fingerprint only the engines that produced evidence.
5. When filters appear, change one constraint at a time: delimiter, quote style, attribute access, keyword construction, whitespace, statement tag, output format, or feedback channel.

## Basic Probes

```text
{{7*7}}                              Jinja2/Twig/Nunjucks/Handlebars
{{364|add:733}}                      Django
${7*7}                               FreeMarker/Java EL/Mako/Groovy
#{7*7}                               SpEL/Thymeleaf/FreeMarker
<%= 7*7 %>                           ERB/EJS/ASP/EEx
@(7*7)                               Razor
{{.}}  {{printf "%d" 49}}            Go template
```

Also test delayed render paths after submission: confirmation pages, previews, profile pages, exports, notifications, email templates, error views, and any admin-facing review path.

## Response-Driven Flow

- Evaluated arithmetic or boolean branch: fingerprint the engine and escalate.
- Template stack trace or syntax error: adapt syntax and context.
- Object/context leakage: enumerate safe objects before reaching for file/config reads.
- Filter or WAF message: identify blocked characters, then switch delimiters, tags, encoding, or construction style.
- Raw reflection or HTML escaping: check delayed render points and second-order consumers.
- No visible output but timing/state changes: use blind time, OOB, or file/state side effects.
- Format validation failure: keep the final output valid and place sensitive work in a statement block.

## Reference

Read `references/bypass-playbook.md` when you need:

- A response classification decision tree.
- Engine-specific payload families.
- Filter and blacklist bypass techniques.
- Blind or no-output handling.
- Sandbox escape patterns.

Use the reference selectively from the observed evidence; do not mechanically try every payload.
