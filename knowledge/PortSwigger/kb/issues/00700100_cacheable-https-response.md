# Cacheable HTTPS response

Source: https://portswigger.net/kb/issues/00700100_cacheable-https-response
Fetched: 2026-06-28T09:17:17.509069+00:00

Support Center

Issue Definitions

Cacheable HTTPS response

Cacheable HTTPS response

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Cacheable HTTPS response

Unless directed otherwise, browsers may store a local cached copy of content received from web servers. Some browsers, including Internet Explorer, cache content accessed via HTTPS. If sensitive information in application responses is stored in the local cache, then this may be retrieved by other users who have access to the same computer at a future time.

Remediation: Cacheable HTTPS response

Applications should return caching directives instructing browsers not to store local copies of any sensitive data. Often, this can be achieved by configuring the web server to prevent caching for relevant paths within the web root. Alternatively, most web development platforms allow you to control the server's caching directives from within individual scripts. Ideally, the web server should return the following HTTP headers in all responses containing sensitive content:

Cache-control: no-store

Pragma: no-cache

References

Web Security Academy: Information disclosure

Vulnerability classifications

CWE-524: Information Exposure Through Caching

CWE-525: Information Exposure Through Browser Caching

CAPEC-37: Retrieve Embedded Sensitive Data

Typical severity

Information

Type index (hex)

0x00700100

Type index (decimal)

7340288

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
