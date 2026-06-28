# Request URL override

Source: https://portswigger.net/kb/issues/00400f00_request-url-override
Fetched: 2026-06-28T09:17:12.476090+00:00

Support Center

Issue Definitions

Request URL override

Request URL override

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Request URL override

Some applications and frameworks support HTTP headers that can be used to override parts of the request URL, potentially affecting the routing and processing of the request.

Intermediate systems are often oblivious to these headers. In the case of reverse proxies and web application firewalls, this can lead to security rulesets being bypassed. If a caching system is in place, this may enable cache poisoning attacks. These headers may also enable forging of log entries.

Even if the application is intended to be accessed directly, some visitors may be using a corporate proxy enabling localised cache poisoning.

Remediation: Request URL override

To fully resolve this issue, locate the component that processes the affected headers, and disable it entirely. If you are using a framework, applying any pending security updates may do this for you.

If this isn't practical, an alternative workaround is to configure an intermediate system to automatically strip the affected headers before they are processed.

References

Web Security Academy: HTTP Host header attacks

Web Security Academy: Web cache poisoning

Practical Web Cache Poisoning

Vulnerability classifications

CWE-436: Interpretation Conflict

CAPEC-141: Cache Poisoning

Typical severity

Information

Type index (hex)

0x00400f00

Type index (decimal)

4198144

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
