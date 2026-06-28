# JWT Editor

Source: https://portswigger.net/bappstore/26aaa5ded2f74beea19e2ed8345a93dd
Fetched: 2026-06-28T09:14:36.625419+00:00

Support Center

BApp Store

JWT Editor

Professional

Community

JWT Editor

Download BApp

JWT Editor is a comprehensive tool for analyzing and manipulating JSON Web Tokens (JWTs) within Burp. It provides rich editing capabilities for both JSON Web Signatures (JWS) and JSON Web Encryptions (JWE), as well facilitating some of the common attacks on JWS implementations and their use within Burp.

Features

Top-level JWT Editor tab for managing cryptographic keys, persistent storage of tokens and extension configuration.

Custom JSON Web Token tab within HTTP and WebSocket message editors for viewing and modifying JWTs.

Automatic JWT detection and highlighting in HTTP and WebSocket Proxy History.

Support for signing, verifying, encrypting and decrypting JWTs using stored keys.

Support for a range of common attacks on JWS.

Intruder payload provider for fuzzing within JWS.

Scanner insertion point provider to allow Burp's Scanner to insert payloads within JWS headers.

Usage

The JWT Editor tab allows you to manage keys, store interesting tokens and configure the extension. Configured keys are then available for use throughout the extension.

In the message editor, the JSON Web Token tab is enabled when a JWT is detected within the corresponding message. The editor switches between JWS and JWE modes depending on the token type and editing views for each token component.

Sign: Resigns the JWS and optionally updates the JWS header.

Verify: Attempts to verify the JWS signature using available verification keys.

Encrypt: Encrypts a JWS into a JWE. The editor then switches to JWE mode.

Decrypt: Decrypts a JWE back into a JWS. The editor then switches to JWS mode.

The Attack feature facilitates several known attacks on JWS, including:

'none' Signing Algorithm

HMAC Key Confusion

Embedded JWK

Signing with an empty HMAC key

Psychic signature attack (CVE-2022-21449)

Collaborator payload injection via x5u or jku headers (Burp Suite Professional only)

Brute-forcing weak HMAC secrets

Embedding of Collaborator payloads within jku or x5u to check for servers potentially loading remote JWKS

Author

Author

Dolph Flynn, Fraser Winterborn

Version

Version

2.6.1

Rating

Rating

Popularity

Popularity

Last updated

Last updated

23 April 2026

Estimated system impact

Estimated system impact

Overall impact:

Low

Memory

Low

CPU

Low

General

Low

Scanner

Low

You can install BApps directly within Burp, via the BApp Store feature in the Burp Extender tool. You can also download them from here, for offline installation into Burp.

You can view the source code for all BApp Store extensions on our

GitHub page.

Follow

@BApp_Store on Twitter to receive notifications of all BApp releases and updates.

Please note that extensions are written by third party users of Burp, and PortSwigger Web Security makes no warranty about their quality or usefulness for any particular purpose.

Go back to

BappStore

Note:

Please note that extensions are written by third party users of Burp, and PortSwigger Web Security makes no warranty about their quality or usefulness for any particular purpose.
