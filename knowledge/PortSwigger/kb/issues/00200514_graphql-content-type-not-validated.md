# GraphQL content type not validated

Source: https://portswigger.net/kb/issues/00200514_graphql-content-type-not-validated
Fetched: 2026-06-28T09:17:10.080990+00:00

Support Center

Issue Definitions

GraphQL content type not validated

GraphQL content type not validated

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: GraphQL content type not validated

Cross-site request forgery (CSRF) vulnerabilities enable an attacker to induce users to perform actions that they do not intend to perform. This is done by creating a malicious website that forges a cross-domain request to the vulnerable application.

Cross-site request forgery (CSRF) vulnerabilities in a GraphQL endpoint can arise when the content type is not validated. POST requests using a content-type of application/json are secure against forgery as long as the content type is validated, as an attacker wouldn't be able to make the victim's browser send this request.

However, alternative methods such as GET, or any request that has a content-type of x-www-form-urlencoded, can be sent by a browser and so may leave users vulnerable to attack. Where this is the case, attackers may be able to craft exploits that use a valid CSRF token from a previous request to send malicious requests to the API.

Remediation: GraphQL content type not validated

Ensure that your GraphQL endpoint validates the content type. If the content type cannot be validated, ensure a valid CSRF token is required.

References

Web Security Academy: GraphQL API vulnerabilities

Web Security Academy: Cross-site request forgery

Vulnerability classifications

CWE-352: Cross-Site Request Forgery

CAPEC-62: Cross-Site Request Forgery

Typical severity

Low

Type index (hex)

0x00200514

Type index (decimal)

2098452

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
