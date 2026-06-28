# Cross-origin resource sharing

Source: https://portswigger.net/kb/issues/00200600_cross-origin-resource-sharing
Fetched: 2026-06-28T09:17:09.889635+00:00

Support Center

Issue Definitions

Cross-origin resource sharing

Cross-origin resource sharing

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Cross-origin resource sharing

An HTML5 cross-origin resource sharing (CORS) policy controls whether and how content running on other domains can perform two-way interaction with the domain that publishes the policy. The policy is fine-grained and can apply access controls per-request based on the URL and other features of the request.

If another domain is allowed by the policy, then that domain can potentially attack users of the application. If a user is logged in to the application, and visits a domain allowed by the policy, then any malicious content running on that domain can potentially retrieve content from the application, and sometimes carry out actions within the security context of the logged in user.

Even if an allowed domain is not overtly malicious in itself, security vulnerabilities within that domain could potentially be leveraged by an attacker to exploit the trust relationship and attack the application that allows access. CORS policies on pages containing sensitive information should be reviewed to determine whether it is appropriate for the application to trust both the intentions and security posture of any domains granted access.

Remediation: Cross-origin resource sharing

Any inappropriate domains should be removed from the CORS policy.

References

Web Security Academy: Cross-origin resource sharing (CORS)

Exploiting CORS Misconfigurations

Vulnerability classifications

CWE-942: Overly Permissive Cross-domain Whitelist

Typical severity

Information

Type index (hex)

0x00200600

Type index (decimal)

2098688

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
