# JWT none algorithm supported

Source: https://portswigger.net/kb/issues/00200901_jwt-none-algorithm-supported
Fetched: 2026-06-28T09:17:10.441615+00:00

Support Center

Issue Definitions

JWT none algorithm supported

JWT none algorithm supported

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: JWT none algorithm supported

All JSON Web Tokens should contain the "alg" header parameter, which specifies the algorithm that the server should use to verify the signature of the token. In addition to cryptographically strong algorithms, the JWT specification also defines the "none" algorithm, which can be used with "unsecured" (unsigned) JWTs. When this algorithm is supported on the server, it may accept tokens that have no signature at all.

As the JWT header can be tampered with client-side, a malicious user could change the "alg" header to "none", then remove the signature and check whether the server still accepts the token.

If it does, they could exploit this vulnerability by supplying an arbitrary claim in the JWT payload to escalate their privileges or impersonate other users. For example, if the token contains a "username": "joe" claim, they could change this to "username": "admin".

Remediation: JWT none algorithm supported

Ensure that unsecured JWTs are rejected by the server and only cryptographically strong algorithms are accepted and verified. Even if the application does not directly use unsecured JWTs, it's important to make sure that the "alg": "none" header parameter is restricted by the underlying JWT parsing library.

Vulnerability classifications

CWE-345: Insufficient Verification of Data Authenticity

Typical severity

High

Type index (hex)

0x00200901

Type index (decimal)

2099457

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
