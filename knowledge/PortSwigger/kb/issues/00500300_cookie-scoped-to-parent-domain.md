# Cookie scoped to parent domain

Source: https://portswigger.net/kb/issues/00500300_cookie-scoped-to-parent-domain
Fetched: 2026-06-28T09:17:13.112194+00:00

Support Center

Issue Definitions

Cookie scoped to parent domain

Cookie scoped to parent domain

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Cookie scoped to parent domain

A cookie's domain attribute determines which domains can access the cookie. Browsers will automatically submit the cookie in requests to in-scope domains, and those domains will also be able to access the cookie via JavaScript. If a cookie is scoped to a parent domain, then that cookie will be accessible by the parent domain and also by any other subdomains of the parent domain. If the cookie contains sensitive data (such as a session token) then this data may be accessible by less trusted or less secure applications residing at those domains, leading to a security compromise.

Remediation: Cookie scoped to parent domain

By default, cookies are scoped to the issuing domain, and on IE/Edge to subdomains. If you remove the explicit domain attribute from your Set-cookie directive, then the cookie will have this default scope, which is safe and appropriate in most situations. If you particularly need a cookie to be accessible by a parent domain, then you should thoroughly review the security of the applications residing on that domain and its subdomains, and confirm that you are willing to trust the people and systems that support those applications.

Vulnerability classifications

CWE-16: Configuration

Typical severity

Low

Type index (hex)

0x00500300

Type index (decimal)

5243648

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
