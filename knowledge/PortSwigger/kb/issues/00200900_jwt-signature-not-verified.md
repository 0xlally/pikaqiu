# JWT signature not verified

Source: https://portswigger.net/kb/issues/00200900_jwt-signature-not-verified
Fetched: 2026-06-28T09:17:10.939938+00:00

Support Center

Issue Definitions

JWT signature not verified

JWT signature not verified

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: JWT signature not verified

The JSON Web Token specification provides several ways for developers to digitally sign payload claims. This ensures data integrity and robust user authentication. However, some servers fail to properly verify the signature, which can result in them accepting tokens with invalid signatures.

A malicious user can exploit this vulnerability by supplying an arbitrary claim in the JWT payload to obtain new privileges or impersonate other users. For example, if the token contains a "username": "joe" claim, an attacker could potentially change this to "username": "admin" to grant themselves higher privileges.

Burp Suite detects this vulnerability by comparing responses to multiple requests with proper and improper signatures. Although this is a reliable detection method, it is not bulletproof. When this issue is reported, we recommend manually checking that the difference in responses was indeed caused by the different JWT permutations.

Remediation: JWT signature not verified

Ensure that the signature of the JWT is properly verified for all supported algorithms.

Vulnerability classifications

CWE-345: Insufficient Verification of Data Authenticity

CWE-347: Improper Verification of Cryptographic Signature

Typical severity

High

Type index (hex)

0x00200900

Type index (decimal)

2099456

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
