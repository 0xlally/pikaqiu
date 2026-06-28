# HTTP PUT method is enabled

Source: https://portswigger.net/kb/issues/00100900_http-put-method-is-enabled
Fetched: 2026-06-28T09:17:05.846784+00:00

Support Center

Issue Definitions

HTTP PUT method is enabled

HTTP PUT method is enabled

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: HTTP PUT method is enabled

The HTTP PUT method is normally used to upload data that is saved on the server at a user-supplied URL. If enabled, an attacker may be able to place arbitrary, and potentially malicious, content into the application. Depending on the server's configuration, this may lead to compromise of other users (by uploading client-executable scripts), compromise of the server (by uploading server-executable code), or other attacks.

Remediation: HTTP PUT method is enabled

Refer to your platform's documentation to determine how to disable the HTTP PUT method on the server.

Vulnerability classifications

CWE-650: Trusting HTTP Permission Methods on the Server Side

Typical severity

High

Type index (hex)

0x00100900

Type index (decimal)

1050880

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
