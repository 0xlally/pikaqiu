# Hidden HTTP 2

Source: https://portswigger.net/kb/issues/01000500_hidden-http-2
Fetched: 2026-06-28T09:17:18.006886+00:00

Support Center

Issue Definitions

Hidden HTTP 2

Hidden HTTP 2

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Hidden HTTP 2

Clients that support HTTP/2 typically default to HTTP/1.1, and only use HTTP/2 if the server advertises support for it via the ALPN field during the TLS handshake.

Some misconfigured servers that do support HTTP/2 fail to advertise this, making it appear as though they only support HTTP/1.1. This can lead to people overlooking viable HTTP/2 attack surface and missing associated vulnerabilities, such as HTTP/2 downgrade-based request smuggling.

Remediation: Hidden HTTP 2

If you want to use HTTP/2, make sure the server is configured to advertise it correctly. Otherwise, consider fully disabling it server-side to reduce unnecessary attack surface.

References

HTTP/2: The Sequel is Always Worse

Vulnerability classifications

CWE-912: Hidden Functionality

Typical severity

Information

Type index (hex)

0x01000500

Type index (decimal)

16778496

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
