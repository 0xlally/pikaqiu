# Link manipulation (stored)

Source: https://portswigger.net/kb/issues/00501004_link-manipulation-stored
Fetched: 2026-06-28T09:17:15.067208+00:00

Support Center

Issue Definitions

Link manipulation (stored)

Link manipulation (stored)

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Link manipulation (stored)

Link manipulation occurs when an application embeds user input into the path or domain of URLs that appear within application responses. An attacker can use this vulnerability to construct a link that, if visited by another application user, will modify the target of URLs within the response. It may be possible to leverage this to perform various attacks, such as:

Manipulating the path of an on-site link that has sensitive parameters in the URL. If the response from the modified path contains references to off-site resources, then the sensitive data might be leaked to external domains via the Referer header.

Manipulating the URL targeted by a form action, making the form submission have unintended side effects.

Manipulating the URL used by a CSS import statement to point to an attacker-uploaded file, resulting in CSS injection.

Injecting on-site links containing XSS exploits, thereby bypassing browser anti-XSS defenses, since those defenses typically do not operate on on-site links.

The security impact of this issue depends largely on the nature of the application functionality. Even if it has no direct impact on its own, an attacker may use it in conjunction with other vulnerabilities to escalate their overall severity.

Stored link manipulation vulnerabilities arise when the applicable input was submitted in an previous request and stored by the application.

Remediation: Link manipulation (stored)

Consider using a whitelist to restrict user input to safe values. Please note that in some situations this issue will have no security impact, meaning no remediation is necessary.

References

Using path manipulation to hijack Flickr accounts

Vulnerability classifications

CWE-73: External Control of File Name or Path

CWE-20: Improper Input Validation

CAPEC-153: Input Data Manipulation

Typical severity

Information

Type index (hex)

0x00501004

Type index (decimal)

5246980

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
