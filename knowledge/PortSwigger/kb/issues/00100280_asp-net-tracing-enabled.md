# ASP.NET tracing enabled

Source: https://portswigger.net/kb/issues/00100280_asp-net-tracing-enabled
Fetched: 2026-06-28T09:17:04.827371+00:00

Support Center

Issue Definitions

ASP.NET tracing enabled

ASP.NET tracing enabled

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: ASP.NET tracing enabled

ASP.NET tracing is a debugging feature that is designed for use during development to help troubleshoot problems. It discloses sensitive information to users, and if enabled in production contexts may present a serious security threat.

Application-level tracing enables any user to retrieve full details about recent requests to the application, including those of other users. This information typically includes session tokens and request parameters, which may enable an attacker to compromise other users and even take control of the entire application.

Page-level tracing returns the same information, but relating only to the current request. This may still contain sensitive data in session and server variables that would be of use to an attacker.

Remediation: ASP.NET tracing enabled

To disable tracing, open the Web.config file for the application, and find the <trace> element within the <system.web> section. Either set the enabled attribute to "false" (to disable tracing) or set the localOnly attribute to "true" (to enable tracing only on the server itself).

Note that even with tracing disabled in this way, it is possible for individual pages to turn on page-level tracing either within the Page directive of the ASP.NET page, or programmatically through application code. If you observe tracing output only on some application pages, you should review the page source and the code behind, to find the reason why tracing is occurring.

It is strongly recommended that you refer to your platform's documentation relating to this issue, and do not rely solely on the above remediation.

References

Web Security Academy: Information disclosure

Vulnerability classifications

CWE-10: ASP.NET Environment Issues

CWE-11: ASP.NET Misconfiguration: Creating Debug Binary

CAPEC-37: Retrieve Embedded Sensitive Data

Typical severity

High

Type index (hex)

0x00100280

Type index (decimal)

1049216

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
