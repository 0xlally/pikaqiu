# Web cache poisoning

Source: https://portswigger.net/kb/issues/00200180_web-cache-poisoning
Fetched: 2026-06-28T09:17:06.576247+00:00

Support Center

Issue Definitions

Web cache poisoning

Web cache poisoning

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Web cache poisoning

Web caches identify resources using a few specific components of each HTTP request, together known as the cache key. Two requests with the same cache key are regarded by the cache as equivalent.

Web cache poisoning vulnerabilities arise when an application behind a cache processes input that is not included in the cache key. Attackers can exploit this by sending crafted input to trigger a harmful response that the cache will then save and serve to other users.

The impact is potentially serious as the malicious cached page may be served to a large number of users without other interaction. The threat posed by this vulnerability depends largely on what can be achieved with the input. Often the input is vulnerable to XSS, or can be used to trigger a redirect to another domain. Other times, it can simply be used to swap pages around.

Remediation: Web cache poisoning

To resolve this issue, either disable support for the affected input, or disable caching on all affected pages.

If both the affected input and caching behavior are required, configure the cache to ensure that the input is included in the cache key. Depending on which caching solution you use, if the input is in a request header it might be possible to achieve this using the Vary response header.

References

Web Security Academy: Web cache poisoning

PortSwigger Research: Practical Web Cache Poisoning

PortSwigger Research: Web Cache Entanglement

HTTP Vary header

Vulnerability classifications

CWE-436: Interpretation Conflict

CAPEC-141: Cache Poisoning

Typical severity

High

Type index (hex)

0x00200180

Type index (decimal)

2097536

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
