# Base64-encoded data in parameter

Source: https://portswigger.net/kb/issues/00700200_base64-encoded-data-in-parameter
Fetched: 2026-06-28T09:17:17.732816+00:00

Support Center

Issue Definitions

Base64-encoded data in parameter

Base64-encoded data in parameter

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Base64-encoded data in parameter

Applications sometimes Base64-encode parameters in an attempt to obfuscate them from users or facilitate transport of binary data. The presence of Base64-encoded data may indicate security-sensitive information or functionality that is worthy of further investigation. The data should be reviewed to determine whether it contains any interesting information, or provides any additional entry points for malicious input.

Vulnerability classifications

CWE-310: Cryptographic Issues

CWE-311: Missing Encryption of Sensitive Data

CAPEC-37: Retrieve Embedded Sensitive Data

Typical severity

Information

Type index (hex)

0x00700200

Type index (decimal)

7340544

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
