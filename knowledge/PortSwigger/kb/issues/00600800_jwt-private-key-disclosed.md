# JWT private key disclosed

Source: https://portswigger.net/kb/issues/00600800_jwt-private-key-disclosed
Fetched: 2026-06-28T09:17:17.106633+00:00

Support Center

Issue Definitions

JWT private key disclosed

JWT private key disclosed

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: JWT private key disclosed

The JSON Web Signature specification defines the optional "jwk" header, which contains information about the key used to digitally sign the JWT. Defined in RFC 7517, this data structure contains cryptographic keys for different signature algorithms, such as HMAC or RSA for example. This parameter is particularly useful for servers that are configured to use multiple different keys because it can help to determine which key to use when verifying the signature.

If a server is configured incorrectly, it may accidentally include private key components into the "jwk" header parameter of JWTs that it issues. In this case, a malicious user could use any private keys they've obtained to tamper with the signature of JWT tokens and impersonate other users.

Remediation: JWT private key disclosed

If your JWK is embedded into the JWT header, make sure to omit any private key components. As long as it only contains public key components, using the "jwk" header is not a security threat in itself. In fact, its correct use can help servers to select a proper key for verification.

References

JSON Web Key (JWK)

Vulnerability classifications

CWE-200: Information Exposure

Typical severity

High

Type index (hex)

0x00600800

Type index (decimal)

6293504

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
