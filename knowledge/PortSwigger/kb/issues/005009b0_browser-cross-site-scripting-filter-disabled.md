# Browser cross-site scripting filter disabled

Source: https://portswigger.net/kb/issues/005009b0_browser-cross-site-scripting-filter-disabled
Fetched: 2026-06-28T09:17:13.700972+00:00

Support Center

Issue Definitions

Browser cross-site scripting filter disabled

Browser cross-site scripting filter disabled

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Browser cross-site scripting filter disabled

Some browsers, including Internet Explorer, contain built-in filters designed to protect against cross-site scripting (XSS) attacks. Applications can instruct browsers to disable this filter by setting the following response header:

X-XSS-Protection: 0

This behavior does not in itself constitute a vulnerability; in some cases XSS filters may themselves be leveraged to perform attacks against application users. However, in typical situations XSS filters do provide basic protection for application users against some XSS vulnerabilities in applications. The presence of this header should be reviewed to establish whether it affects the application's security posture.

Remediation: Browser cross-site scripting filter disabled

Review whether the application needs to disable XSS filters. In most cases you can gain the protection provided by XSS filters without the associated risks by using the following response header:

X-XSS-Protection: 1; mode=block

When this header is set, browsers that detect an XSS attack will simply render a blank page instead of attempting to sanitize the injected script. This behavior is considerably less likely to introduce new security issues.

References

Web Security Academy: Cross-site scripting

Controlling the XSS Filter

Vulnerability classifications

CWE-16: Configuration

CAPEC-63: Cross-Site Scripting (XSS)

Typical severity

Information

Type index (hex)

0x005009b0

Type index (decimal)

5245360

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
