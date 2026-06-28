# Cross-domain script include

Source: https://portswigger.net/kb/issues/00500500_cross-domain-script-include
Fetched: 2026-06-28T09:17:13.273664+00:00

Support Center

Issue Definitions

Cross-domain script include

Cross-domain script include

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Cross-domain script include

When an application includes a script from an external domain, this script is executed by the browser within the security context of the invoking application. The script can therefore do anything that the application's own scripts can do, such as accessing application data and performing actions within the context of the current user.

If you include a script from an external domain, then you are trusting that domain with the data and functionality of your application, and you are trusting the domain's own security to prevent an attacker from modifying the script to perform malicious actions within your application.

Remediation: Cross-domain script include

Scripts should ideally not be included from untrusted domains. Applications that rely on static third-party scripts should consider using Subresource Integrity to make browsers verify them, or copying the contents of these scripts onto their own domain and including them from there. If that is not possible (e.g. for licensing reasons) then consider reimplementing the script's functionality within application code.

References

Subresource Integrity

Vulnerability classifications

CWE-829: Inclusion of Functionality from Untrusted Control Sphere

Typical severity

Information

Type index (hex)

0x00500500

Type index (decimal)

5244160

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
