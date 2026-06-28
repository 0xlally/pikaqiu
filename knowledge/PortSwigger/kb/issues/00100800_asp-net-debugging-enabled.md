# ASP.NET debugging enabled

Source: https://portswigger.net/kb/issues/00100800_asp-net-debugging-enabled
Fetched: 2026-06-28T09:17:05.473083+00:00

Support Center

Issue Definitions

ASP.NET debugging enabled

ASP.NET debugging enabled

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: ASP.NET debugging enabled

ASP.NET allows remote debugging of web applications, if configured to do so. By default, debugging is subject to access control and requires platform-level authentication.

If an attacker can successfully start a remote debugging session, this is likely to disclose sensitive information about the web application and supporting infrastructure that may be valuable in formulating targeted attacks against the system.

Remediation: ASP.NET debugging enabled

To disable debugging, open the Web.config file for the application, and find the <compilation> element within the <system.web> section. Set the debug attribute to "false". Note that it is also possible to enable debugging for all applications within the Machine.config file. You should confirm that the debug attribute in the <compilation> element has not been set to "true" within the Machine.config file.

It is strongly recommended that you refer to your platform's documentation relating to this issue, and do not rely solely on the above remediation.

References

Web Security Academy: Information disclosure

Vulnerability classifications

CWE-11: ASP.NET Misconfiguration: Creating Debug Binary

CAPEC-37: Retrieve Embedded Sensitive Data

Typical severity

Medium

Type index (hex)

0x00100800

Type index (decimal)

1050624

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
