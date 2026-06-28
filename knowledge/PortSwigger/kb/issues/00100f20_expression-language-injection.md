# Expression Language injection

Source: https://portswigger.net/kb/issues/00100f20_expression-language-injection
Fetched: 2026-06-28T09:17:05.999403+00:00

Support Center

Issue Definitions

Expression Language injection

Expression Language injection

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Expression Language injection

Server-side code injection vulnerabilities arise when an application incorporates user-controllable data into a string that is dynamically evaluated by a code interpreter. If the user data is not strictly validated, an attacker can use crafted input to modify the code to be executed, and inject arbitrary code that will be executed by the server.

Server-side code injection vulnerabilities are usually very serious and lead to complete compromise of the application's data and functionality, and often of the server that is hosting the application. It may also be possible to use the server as a platform for further attacks against other systems.

Remediation: Expression Language injection

Whenever possible, applications should avoid incorporating user-controllable data into dynamically evaluated code. In almost every situation, there are safer alternative methods of implementing application functions, which cannot be manipulated to inject arbitrary code into the server's processing.

If it is considered unavoidable to incorporate user-supplied data into dynamically evaluated code, then the data should be strictly validated. Ideally, a whitelist of specific accepted values should be used. Otherwise, only short alphanumeric strings should be accepted. Input containing any other data, including any conceivable code metacharacters, should be rejected.

References

Spring Expression Language Injection

Remote Code Execution with Spring Expression Language Injection

Vulnerability classifications

CWE-116: Improper Encoding or Escaping of Output

CWE-159: Failure to Sanitize Special Element

CWE-917: Improper Neutralization of Special Elements used in an Expression Language Statement ('Expression Language Injection')

CAPEC-242: Code Injection

Typical severity

High

Type index (hex)

0x00100f20

Type index (decimal)

1052448

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
