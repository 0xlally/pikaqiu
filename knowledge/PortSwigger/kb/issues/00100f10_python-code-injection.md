# Python code injection

Source: https://portswigger.net/kb/issues/00100f10_python-code-injection
Fetched: 2026-06-28T09:17:06.459457+00:00

Support Center

Issue Definitions

Python code injection

Python code injection

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Python code injection

Server-side code injection vulnerabilities arise when an application incorporates user-controllable data into a string that is dynamically evaluated by a code interpreter. If the user data is not strictly validated, an attacker can use crafted input to modify the code to be executed, and inject arbitrary code that will be executed by the server.

Server-side code injection vulnerabilities are usually very serious and lead to complete compromise of the application's data and functionality, and often of the server that is hosting the application. It may also be possible to use the server as a platform for further attacks against other systems.

Remediation: Python code injection

Whenever possible, applications should avoid incorporating user-controllable data into dynamically evaluated code. In almost every situation, there are safer alternative methods of implementing application functions, which cannot be manipulated to inject arbitrary code into the server's processing.

If it is considered unavoidable to incorporate user-supplied data into dynamically evaluated code, then the data should be strictly validated. Ideally, a whitelist of specific accepted values should be used. Otherwise, only short alphanumeric strings should be accepted. Input containing any other data, including any conceivable code metacharacters, should be rejected.

Vulnerability classifications

CWE-94: Improper Control of Generation of Code ('Code Injection')

CWE-95: Improper Neutralization of Directives in Dynamically Evaluated Code ('Eval Injection')

CWE-116: Improper Encoding or Escaping of Output

CAPEC-242: Code Injection

Typical severity

High

Type index (hex)

0x00100f10

Type index (decimal)

1052432

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
