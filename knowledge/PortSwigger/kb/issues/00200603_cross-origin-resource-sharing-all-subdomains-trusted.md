# Cross-origin resource sharing: all subdomains trusted

Source: https://portswigger.net/kb/issues/00200603_cross-origin-resource-sharing-all-subdomains-trusted
Fetched: 2026-06-28T09:17:09.867444+00:00

Support Center

Issue Definitions

Cross-origin resource sharing: all subdomains trusted

Cross-origin resource sharing: all subdomains trusted

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Cross-origin resource sharing: all subdomains trusted

An HTML5 cross-origin resource sharing (CORS) policy controls whether and how content running on other domains can perform two-way interaction with the domain that publishes the policy. The policy is fine-grained and can apply access controls per-request based on the URL and other features of the request.

If an application allows interaction from all subdomains, then this significantly increases its attack surface. For example, a cross-site scripting (XSS) vulnerability in any subdomain could potentially compromise the application that publishes the policy. Some consumer ISPs return custom content when requests are made to unregistered subdomains, which can introduce XSS vulnerabilities even if all of an organization's own applications are secure.

Remediation: Cross-origin resource sharing: all subdomains trusted

Rather than trusting all subdomains, use a whitelisted of trusted subdomains.

References

Web Security Academy: Cross-origin resource sharing (CORS)

Exploiting CORS Misconfigurations

Vulnerability classifications

CWE-942: Overly Permissive Cross-domain Whitelist

Typical severity

Low

Type index (hex)

0x00200603

Type index (decimal)

2098691

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
