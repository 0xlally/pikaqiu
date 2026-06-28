# HTTP TRACE method is enabled

Source: https://portswigger.net/kb/issues/00500a00_http-trace-method-is-enabled
Fetched: 2026-06-28T09:17:13.992607+00:00

Support Center

Issue Definitions

HTTP TRACE method is enabled

HTTP TRACE method is enabled

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: HTTP TRACE method is enabled

The HTTP TRACE method is designed for diagnostic purposes. If enabled, the web server will respond to requests that use the TRACE method by echoing in its response the exact request that was received.

This behavior is often harmless, but occasionally leads to the disclosure of sensitive information such as internal authentication headers appended by reverse proxies. This functionality could historically be used to bypass the HttpOnly cookie flag on cookies, but this is no longer possible in modern web browsers.

Remediation: HTTP TRACE method is enabled

The TRACE method should be disabled on production web servers.

References

Web Security Academy: Information disclosure via TRACE method

Vulnerability classifications

CWE-16: Configuration

Typical severity

Information

Type index (hex)

0x00500a00

Type index (decimal)

5245440

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
