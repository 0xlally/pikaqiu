# HTTP request smuggling

Source: https://portswigger.net/kb/issues/00200140_http-request-smuggling
Fetched: 2026-06-28T09:17:06.533545+00:00

Support Center

Issue Definitions

HTTP request smuggling

HTTP request smuggling

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: HTTP request smuggling

HTTP request smuggling vulnerabilities arise when websites route HTTP requests through web servers with inconsistent HTTP parsing.

By supplying a request that different servers interpret as having different lengths, an attacker can poison the back-end TCP/TLS socket and prepend arbitrary data to the next request. Depending on the website's functionality, this can be used to bypass front-end security rules, access internal systems, poison web caches, and launch assorted attacks on users who are actively browsing the site.

Remediation: HTTP request smuggling

You can resolve all variants of this vulnerability by configuring the front-end server to exclusively use HTTP/2 when communicating with back-end systems. Alternatively, you could ensure all servers in the chain run the same web server software with the same configuration. Disabling back-end connection reuse is likely to reduce the impact of this vulnerability, but does not mitigate all possible exploits.

Specific instances of this vulnerability can be resolved by reconfiguring the front-end server to normalize ambiguous requests before routing them onward. Alternatively, you could configure the back-end server to reject the message and close the connection when it encounters an ambiguous request.

References

HTTP Request Smuggling

HTTP Desync Attacks

Vulnerability classifications

CWE-444: Inconsistent Interpretation of HTTP Requests ('HTTP Request Smuggling')

CAPEC-33: HTTP Request Smuggling

Typical severity

High

Type index (hex)

0x00200140

Type index (decimal)

2097472

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
