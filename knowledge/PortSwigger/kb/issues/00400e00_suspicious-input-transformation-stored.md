# Suspicious input transformation (stored)

Source: https://portswigger.net/kb/issues/00400e00_suspicious-input-transformation-stored
Fetched: 2026-06-28T09:17:12.166324+00:00

Support Center

Issue Definitions

Suspicious input transformation (stored)

Suspicious input transformation (stored)

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Suspicious input transformation (stored)

Suspicious input transformation arises when an application receives user input, transforms it in some way, and then performs further processing on the result. The types of transformations that can lead to problems include decoding common formats, such as UTF-8 and URL-encoding, or processing of escape sequences, such as backslash escaping.

Performing these input transformations does not constitute a vulnerability in its own right, but might lead to problems in conjunction with other application behaviors. An attacker might be able to bypass input filters by suitably encoding their payloads, if the input is decoded after the input filters have been applied. Or an attacker might be able to interfere with other data that is concatenated onto their input, by finishing their input with the start of a multi-character encoding or escape sequence, the transformation of which will consume the start of the following data.

Stored suspicious input transformation arises when the transformed input is stored and later embedded into the application's responses.

Remediation: Suspicious input transformation (stored)

Review the transformation that is being applied, to understand whether this is intended and desirable behavior given the nature of the application functionality, and whether it gives rise to any vulnerabilities in relation to bypassing of input filters or character consumption.

References

Backslash Powered Scanning: Hunting Unknown Vulnerability Classes

Vulnerability classifications

CWE-20: Improper Input Validation

CAPEC-153: Input Data Manipulation

Typical severity

Information

Type index (hex)

0x00400e00

Type index (decimal)

4197888

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
