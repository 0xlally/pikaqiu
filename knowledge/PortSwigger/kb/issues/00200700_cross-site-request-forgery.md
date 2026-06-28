# Cross-site request forgery

Source: https://portswigger.net/kb/issues/00200700_cross-site-request-forgery
Fetched: 2026-06-28T09:17:10.269604+00:00

Support Center

Issue Definitions

Cross-site request forgery

Cross-site request forgery

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Cross-site request forgery

Cross-site request forgery (CSRF) vulnerabilities may arise when applications rely solely on HTTP cookies to identify the user that has issued a particular request. Because browsers automatically add cookies to requests regardless of their origin, it may be possible for an attacker to create a malicious web site that forges a cross-domain request to the vulnerable application. For a request to be vulnerable to CSRF, the following conditions must hold:

The request can be issued cross-domain, for example using an HTML form. If the request contains non-standard headers or body content, then it may only be issuable from a page that originated on the same domain.

The application relies solely on HTTP cookies or Basic Authentication to identify the user that issued the request. If the application places session-related tokens elsewhere within the request, then it may not be vulnerable.

The request performs some privileged action within the application, which modifies the application's state based on the identity of the issuing user.

The attacker can determine all the parameters required to construct a request that performs the action. If the request contains any values that the attacker cannot determine or predict, then it is not vulnerable.

Remediation: Cross-site request forgery

The most effective way to protect against CSRF vulnerabilities is to include within relevant requests an additional token that is not transmitted in a cookie: for example, a parameter in a hidden form field. This additional token should contain sufficient entropy, and be generated using a cryptographic random number generator, such that it is not feasible for an attacker to determine or predict the value of any token that was issued to another user. The token should be associated with the user's session, and the application should validate that the correct token is received before performing any action resulting from the request.

An alternative approach, which may be easier to implement, is to validate that Host and Referer headers in relevant requests are both present and contain the same domain name. However, this approach is somewhat less robust: historically, quirks in browsers and plugins have often enabled attackers to forge cross-domain requests that manipulate these headers to bypass such defenses.

References

Web Security Academy: Cross-site request forgery

Using Burp to Test for Cross-Site Request Forgery

The Deputies Are Still Confused

Vulnerability classifications

CWE-352: Cross-Site Request Forgery (CSRF)

CAPEC-62: Cross Site Request Forgery

Typical severity

Medium

Type index (hex)

0x00200700

Type index (decimal)

2098944

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
