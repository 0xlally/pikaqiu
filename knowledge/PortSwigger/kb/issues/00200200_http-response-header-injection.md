# HTTP response header injection

Source: https://portswigger.net/kb/issues/00200200_http-response-header-injection
Fetched: 2026-06-28T09:17:06.879856+00:00

Support Center

Issue Definitions

HTTP response header injection

HTTP response header injection

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: HTTP response header injection

HTTP response header injection vulnerabilities arise when user-supplied data is copied into a response header in an unsafe way. If an attacker can inject newline characters into the header, then they can inject new HTTP headers and also, by injecting an empty line, break out of the headers into the message body and write arbitrary content into the application's response.

Various kinds of attack can be delivered via HTTP response header injection vulnerabilities. Any attack that can be delivered via cross-site scripting can usually be delivered via response header injection, because the attacker can construct a request that causes arbitrary JavaScript to appear within the response body. Further, it is sometimes possible to leverage response header injection vulnerabilities to poison the cache of any proxy server via which users access the application. Here, an attacker sends a crafted request that results in a "split" response containing arbitrary content. If the proxy server can be manipulated to associate the injected response with another URL used within the application, then the attacker can perform a "stored" attack against this URL, which will compromise other users who request that URL in future.

Remediation: HTTP response header injection

If possible, applications should avoid copying user-controllable data into HTTP response headers. If this is unavoidable, then the data should be strictly validated to prevent response header injection attacks. In most situations, it will be appropriate to allow only short alphanumeric strings to be copied into headers, and any other input should be rejected. At a minimum, input containing any characters with ASCII codes less than 0x20 should be rejected.

Vulnerability classifications

CWE-113: Improper Neutralization of CRLF Sequences in HTTP Headers ('HTTP Response Splitting')

CAPEC-34: HTTP Response Splitting

Typical severity

High

Type index (hex)

0x00200200

Type index (decimal)

2097664

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
