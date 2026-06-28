# JWT weak HMAC secret

Source: https://portswigger.net/kb/issues/00200903_jwt-weak-hmac-secret
Fetched: 2026-06-28T09:17:10.768974+00:00

Support Center

Issue Definitions

JWT weak HMAC secret

JWT weak HMAC secret

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: JWT weak HMAC secret

The JSON Web Token specification provides several ways for developers to digitally sign payload claims. This ensures data integrity and robust user authentication. Whenever developers use HMAC signatures, they need to provide a secret key, which is used for both signing and verifying tokens. If this secret is not strong enough, the whole signature can be compromised.

For every JWT observed in your traffic, Burp Suite attempts to brute-force the signature using a list of common weak secrets. This process is performed offline, without sending any requests to the server.

If the secret can be brute-forced this way, a malicious user can modify the JWT header and payload, then re-sign the token with a valid signature for the server. They could then exploit this vulnerability by supplying an arbitrary claim in the JWT payload to escalate their privileges or impersonate other users. For example, if the token contains a "username": "joe" claim, they could change this to "username": "admin".

Remediation: JWT weak HMAC secret

Ensure that a strong, unpredictable secret is used for calculating the HMAC signature on the server. We recommend using a randomly generated value at least 32 bytes in length.

Typical severity

High

Type index (hex)

0x00200903

Type index (decimal)

2099459

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
