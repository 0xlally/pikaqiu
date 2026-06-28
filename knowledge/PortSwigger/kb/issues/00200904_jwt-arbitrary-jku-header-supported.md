# JWT arbitrary jku header supported

Source: https://portswigger.net/kb/issues/00200904_jwt-arbitrary-jku-header-supported
Fetched: 2026-06-28T09:17:10.834187+00:00

Support Center

Issue Definitions

JWT arbitrary jku header supported

JWT arbitrary jku header supported

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: JWT arbitrary jku header supported

The JSON Web Signature specification defines the optional "jku" header, which contains a URL pointing to a set of keys used by the server to digitally sign the JWT. This parameter is particularly useful for servers that are configured to use multiple different keys because it can help to determine which key to use when verifying the signature.

If the target application implicitly trusts this header, it may verify the signature using an arbitrary public key obtained from the provided URL, essentially relying on data that can be tampered with client-side.

A malicious user could insert or modify a "jku" header so that it points to an external server containing a JSON Web Key Set that they've generated themselves. They could then re-sign the token using the matching private key and check whether the server still accepts it.

If it does, they could exploit this vulnerability by supplying an arbitrary claim in the JWT payload to escalate their privileges or impersonate other users. For example, if the token contains a "username": "joe" claim, they could change this to "username": "admin".

Remediation: JWT arbitrary jku header supported

Configure the server so that it does not implicitly trust the "jku" header parameter. If this is present, the server should verify it against the whitelist of trusted values if possible.

We recommend that you only use verification keys obtained from trusted sources, rather than from data that can be modified client-side. Even if the application does not directly use the "jku" header, it's important to make sure that it is restricted by the underlying JWT parsing library.

Typical severity

High

Type index (hex)

0x00200904

Type index (decimal)

2099460

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
