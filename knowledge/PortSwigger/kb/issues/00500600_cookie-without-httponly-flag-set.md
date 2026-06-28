# Cookie without HttpOnly flag set

Source: https://portswigger.net/kb/issues/00500600_cookie-without-httponly-flag-set
Fetched: 2026-06-28T09:17:13.211280+00:00

Support Center

Issue Definitions

Cookie without HttpOnly flag set

Cookie without HttpOnly flag set

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Cookie without HttpOnly flag set

If the HttpOnly attribute is set on a cookie, then the cookie's value cannot be read or set by client-side JavaScript. This measure makes certain client-side attacks, such as cross-site scripting, slightly harder to exploit by preventing them from trivially capturing the cookie's value via an injected script.

Remediation: Cookie without HttpOnly flag set

There is usually no good reason not to set the HttpOnly flag on all cookies. Unless you specifically require legitimate client-side scripts within your application to read or set a cookie's value, you should set the HttpOnly flag by including this attribute within the relevant Set-cookie directive.

You should be aware that the restrictions imposed by the HttpOnly flag can potentially be circumvented in some circumstances, and that numerous other serious attacks can be delivered by client-side script injection, aside from simple cookie stealing.

References

Web Security Academy: Exploiting XSS vulnerabilities

HttpOnly effectiveness

Vulnerability classifications

CWE-16: Configuration

CAPEC-31: Accessing/Intercepting/Modifying HTTP Cookies

Typical severity

Low

Type index (hex)

0x00500600

Type index (decimal)

5244416

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
