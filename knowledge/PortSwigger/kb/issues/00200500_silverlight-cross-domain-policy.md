# Silverlight cross-domain policy

Source: https://portswigger.net/kb/issues/00200500_silverlight-cross-domain-policy
Fetched: 2026-06-28T09:17:08.938031+00:00

Support Center

Issue Definitions

Silverlight cross-domain policy

Silverlight cross-domain policy

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Silverlight cross-domain policy

The Silverlight cross-domain policy controls whether Silverlight client components running on other domains can perform two-way interaction with the domain that publishes the policy. If another domain is allowed by the policy, then that domain can potentially attack users of the application. If a user is logged in to the application, and visits a domain allowed by the policy, then any malicious content running on that domain can potentially gain full access to the application within the security context of the logged in user.

Even if an allowed domain is not overtly malicious in itself, security vulnerabilities within that domain could potentially be leveraged by a third-party attacker to exploit the trust relationship and attack the application that allows access. Any domains that are allowed by the Silverlight cross-domain policy should be reviewed to determine whether it is appropriate for the application to fully trust both their intentions and security posture.

Remediation: Silverlight cross-domain policy

Any inappropriate entries in the Silverlight cross-domain policy file should be removed.

Vulnerability classifications

CWE-942: Overly Permissive Cross-domain Whitelist

Typical severity

High

Type index (hex)

0x00200500

Type index (decimal)

2098432

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
