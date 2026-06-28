# JWT arbitrary x5u header supported

Source: https://portswigger.net/kb/issues/00200905_jwt-arbitrary-x5u-header-supported
Fetched: 2026-06-28T09:17:10.935413+00:00

Support Center

Issue Definitions

JWT arbitrary x5u header supported

JWT arbitrary x5u header supported

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: JWT arbitrary x5u header supported

The JSON Web Signature specification defines the optional "x5u" header, which contains a URL pointing to the X.509 public key certificate or certificate chain for the key used to digitally sign the JWT. This parameter is particularly useful for servers that are configured to use multiple different keys because it can help to determine which key to use when verifying the signature.

If the target application trusts this header, it may verify the signature using an arbitrary public key obtained from the provided URL, essentially relying on data that can be controlled by a third party.

A malicious user could insert or modify an "x5u" header so that it points to an external server containing a public key certificate that they've generated themselves. They could then re-sign the token using the matching private key certificate and check whether the server still accepts it.

If it does, they could exploit this vulnerability by supplying an arbitrary claim in the JWT payload to escalate their privileges or impersonate other users. For example, if the token contains a "username": "joe" claim, they could change this to "username": "admin".

Remediation: JWT arbitrary x5u header supported

Configure the server so that it does not implicitly trust the "x5u" header parameter. If this is present, the server should verify it against the whitelist of trusted values if possible.

We recommend that you only use verification keys obtained from trusted sources, rather than from data that can be modified client-side. Even if the application does not directly use the "x5u" header, it's important to make sure that it is restricted by the underlying JWT parsing library.

Typical severity

High

Type index (hex)

0x00200905

Type index (decimal)

2099461

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
