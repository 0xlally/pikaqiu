# Server-side template injection

Source: https://portswigger.net/kb/issues/00101080_server-side-template-injection
Fetched: 2026-06-28T09:17:06.258157+00:00

Support Center

Issue Definitions

Server-side template injection

Server-side template injection

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Server-side template injection

Server-side template injection occurs when user input is unsafely embedded into a server-side template, allowing users to inject template directives. Using malicious template directives, an attacker may be able to execute arbitrary code and take full control of the web server.

The severity of this issue varies depending on the type of template engine being used. Template engines range from being trivial to almost impossible to exploit. The following steps should be used when attempting to develop an exploit:

Identify the type of template engine being used.

Review its documentation for basic syntax, security considerations, and built-in methods and variables.

Explore the template environment and map the attack surface.

Audit every exposed object and method.

Template injection vulnerabilities can be very serious and can lead to complete compromise of the application's data and functionality, and often of the server that is hosting the application. It may also be possible to use the server as a platform for further attacks against other systems. On the other hand, some template injection vulnerabilities may pose no significant security risk.

Remediation: Server-side template injection

Wherever possible, avoid creating templates from user input. Passing user input into templates as parameters is normally a safe alternative.

If supporting user-submitted templates is a business requirement, consider using a simple logic-less template engine such as Mustache or one provided by the native language like Python's Template. If this is not an option, review the chosen template engine's documentation for hardening advice, and consider rendering the template within a sandboxed execution environment.

References

Web Security Academy: Server-side template injection

Server-side template injection

Other references:

FreeMarker hardening

Velocity Hardening

Twig hardening

Vulnerability classifications

CWE-94: Improper Control of Generation of Code ('Code Injection')

CWE-95: Improper Neutralization of Directives in Dynamically Evaluated Code ('Eval Injection')

CWE-116: Improper Encoding or Escaping of Output

Typical severity

High

Type index (hex)

0x00101080

Type index (decimal)

1052800

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Burp Scanner

This issue - and many more like it - can be found using our

web vulnerability scanner

Read more

Get Burp

Scan your web application from just $499.00

Find out more
