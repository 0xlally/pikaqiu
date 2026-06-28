# Content type is not specified

Source: https://portswigger.net/kb/issues/00800500_content-type-is-not-specified
Fetched: 2026-06-28T09:17:17.919653+00:00

Support Center

Issue Definitions

Content type is not specified

Content type is not specified

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Content type is not specified

If a response does not specify a content type, then the browser will usually analyze the response and attempt to determine the MIME type of its content. This can have unexpected results, and if the content contains any user-controllable data may lead to cross-site scripting or other client-side vulnerabilities.

In most cases, the absence of a content type statement does not constitute a security flaw, particularly if the response contains static content. You should review the contents of affected responses, and the context in which they appear, to determine whether any vulnerability exists.

Remediation: Content type is not specified

For every response containing a message body, the application should include a single Content-type header that correctly and unambiguously states the MIME type of the content in the response body.

References

Web Security Academy: Cross-site scripting

Vulnerability classifications

CWE-16: Configuration

CAPEC-63: Cross-Site Scripting (XSS)

Typical severity

Information

Type index (hex)

0x00800500

Type index (decimal)

8389888

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
