# Json Web Key Set disclosed

Source: https://portswigger.net/kb/issues/00600700_json-web-key-set-disclosed
Fetched: 2026-06-28T09:17:17.450940+00:00

Support Center

Issue Definitions

Json Web Key Set disclosed

Json Web Key Set disclosed

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Json Web Key Set disclosed

A JSON Web Key Set is a JSON object that represents a set of JSON Web Keys (JWKs). Authorization servers often publish JWK Sets under well-known URLs to tell clients how they can verify the signature of issued JWTs. Defined in RFC 7517, this data structure contains cryptographic keys for different signature algorithms, such as HMAC or RSA for example. If a server is configured incorrectly, it may accidentally expose private key components as well as public ones. In this case, a malicious user could use any private keys they've obtained to tamper with the signature of JWT tokens and impersonate other users.

Even if no secret key components are exposed, the knowledge of public keys may be useful for other attacks, such as algorithm and key confusion for example.

Remediation: Json Web Key Set disclosed

If your JWK Set is exposed publicly, make sure to omit any private key components. As long as it only contains public key components, exposing a JWK Set is not a security threat in itself. In fact, its correct use can represent good practice for non-security reasons.

References

JSON Web Key (JWK)

Vulnerability classifications

CWE-200: Information Exposure

Typical severity

Information

Type index (hex)

0x00600700

Type index (decimal)

6293248

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
