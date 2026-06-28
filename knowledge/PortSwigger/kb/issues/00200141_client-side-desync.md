# Client-side desync

Source: https://portswigger.net/kb/issues/00200141_client-side-desync
Fetched: 2026-06-28T09:17:06.986178+00:00

Support Center

Issue Definitions

Client-side desync

Client-side desync

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Client-side desync

Client-side desync (CSD) vulnerabilities occur when a web server fails to correctly process the Content-Length of POST requests. By exploiting this behavior, an attacker can force a victim's browser to desynchronize its connection with the website, typically leading to XSS.

Remediation: Client-side desync

You can resolve this vulnerability by patching the server so that it either processes POST requests correctly, or closes the connection after handling them. You could also disable connection reuse entirely, but this may reduce performance. You can also resolve this issue by enabling HTTP/2.

References

HTTP Request Smuggling

Browser-Powered Desync Attacks

Vulnerability classifications

CWE-444: Inconsistent Interpretation of HTTP Requests ('HTTP Request Smuggling')

CAPEC-33: HTTP Request Smuggling

Typical severity

High

Type index (hex)

0x00200141

Type index (decimal)

2097473

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
