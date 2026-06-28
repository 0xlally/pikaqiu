# Content type incorrectly stated

Source: https://portswigger.net/kb/issues/00800400_content-type-incorrectly-stated
Fetched: 2026-06-28T09:17:17.825596+00:00

Support Center

Issue Definitions

Content type incorrectly stated

Content type incorrectly stated

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Content type incorrectly stated

If a response specifies an incorrect content type then browsers may process the response in unexpected ways. If the content type is specified to be a renderable text-based format, then the browser will usually attempt to interpret the response as being in that format, regardless of the actual contents of the response. Additionally, some other specified content types might sometimes be interpreted as HTML due to quirks in particular browsers. This behavior might lead to otherwise "safe" content such as images being rendered as HTML, enabling cross-site scripting attacks in certain conditions.

The presence of an incorrect content type statement typically only constitutes a security flaw when the affected resource is dynamically generated, uploaded by a user, or otherwise contains user input. You should review the contents of affected responses, and the context in which they appear, to determine whether any vulnerability exists.

Remediation: Content type incorrectly stated

For every response containing a message body, the application should include a single Content-type header that correctly and unambiguously states the MIME type of the content in the response body.

Additionally, the response header "X-content-type-options: nosniff" should be returned in all responses to reduce the likelihood that browsers will interpret content in a way that disregards the Content-type header.

References

Web Security Academy: Cross-site scripting

Vulnerability classifications

CWE-16: Configuration

CWE-436: Interpretation Conflict

CAPEC-63: Cross-Site Scripting (XSS)

Typical severity

Low

Type index (hex)

0x00800400

Type index (decimal)

8389632

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
