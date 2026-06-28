# Cross-origin resource sharing: unencrypted origin trusted

Source: https://portswigger.net/kb/issues/00200602_cross-origin-resource-sharing-unencrypted-origin-trusted
Fetched: 2026-06-28T09:17:10.112211+00:00

Support Center

Issue Definitions

Cross-origin resource sharing: unencrypted origin trusted

Cross-origin resource sharing: unencrypted origin trusted

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Cross-origin resource sharing: unencrypted origin trusted

An HTML5 cross-origin resource sharing (CORS) policy controls whether and how content running on other domains can perform two-way interaction with the domain that publishes the policy. The policy is fine-grained and can apply access controls per-request based on the URL and other features of the request.

If a site allows interaction from an origin that uses unencrypted HTTP communications, then it is vulnerable to an attacker who is in a position to view and modify a user's unencrypted network traffic. The attacker can control the responses from unencrypted origins, thereby injecting content that is able to interact with the application that publishes the policy. This means that the application is effectively extending trust to all such attackers, thereby undoing much of the benefit of using HTTPS communications.

Remediation: Cross-origin resource sharing: unencrypted origin trusted

Only trust origins that use encrypted HTTPS communications.

References

Web Security Academy: Cross-origin resource sharing (CORS)

Exploiting CORS Misconfigurations

Vulnerability classifications

CWE-942: Overly Permissive Cross-domain Whitelist

Typical severity

Low

Type index (hex)

0x00200602

Type index (decimal)

2098690

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
