# User agent-dependent response

Source: https://portswigger.net/kb/issues/00400120_user-agent-dependent-response
Fetched: 2026-06-28T09:17:12.424445+00:00

Support Center

Issue Definitions

User agent-dependent response

User agent-dependent response

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: User agent-dependent response

Application responses may depend systematically on the value of the User-Agent header in requests. This behavior does not itself constitute a security vulnerability, but may point towards additional attack surface within the application, which may contain vulnerabilities.

This behavior often arises because applications provide different user interfaces for desktop and mobile users. Mobile interfaces have often been less thoroughly tested for vulnerabilities such as cross-site scripting, and often have simpler authentication and session handling mechanisms that may contain problems that are not present in the full interface.

To review the interface provided by the alternate User-Agent header, you can configure a match/replace rule in Burp Proxy to modify the User-Agent header in all requests, and then browse the application in the normal way using your normal browser.

Vulnerability classifications

CWE-16: Configuration

Typical severity

Information

Type index (hex)

0x00400120

Type index (decimal)

4194592

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
