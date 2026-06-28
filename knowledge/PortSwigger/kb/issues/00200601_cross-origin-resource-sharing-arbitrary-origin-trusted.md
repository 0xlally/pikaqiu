# Cross-origin resource sharing: arbitrary origin trusted

Source: https://portswigger.net/kb/issues/00200601_cross-origin-resource-sharing-arbitrary-origin-trusted
Fetched: 2026-06-28T09:17:09.863898+00:00

Support Center

Issue Definitions

Cross-origin resource sharing: arbitrary origin trusted

Cross-origin resource sharing: arbitrary origin trusted

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Cross-origin resource sharing: arbitrary origin trusted

An HTML5 cross-origin resource sharing (CORS) policy controls whether and how content running on other domains can perform two-way interaction with the domain that publishes the policy. The policy is fine-grained and can apply access controls per-request based on the URL and other features of the request.

Trusting arbitrary origins effectively disables the same-origin policy, allowing two-way interaction by third-party web sites. Unless the response consists only of unprotected public content, this policy is likely to present a security risk.

If the site specifies the header Access-Control-Allow-Credentials: true, third-party sites may be able to carry out privileged actions and retrieve sensitive information. Even if it does not, attackers may be able to bypass any IP-based access controls by proxying through users' browsers.

Remediation: Cross-origin resource sharing: arbitrary origin trusted

Rather than using a wildcard or programmatically verifying supplied origins, use a whitelist of trusted domains.

References

Web Security Academy: Cross-origin resource sharing (CORS)

Exploiting CORS Misconfigurations

Vulnerability classifications

CWE-942: Overly Permissive Cross-domain Whitelist

Typical severity

High

Type index (hex)

0x00200601

Type index (decimal)

2098689

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
