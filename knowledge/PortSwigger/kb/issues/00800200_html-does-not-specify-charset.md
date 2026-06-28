# HTML does not specify charset

Source: https://portswigger.net/kb/issues/00800200_html-does-not-specify-charset
Fetched: 2026-06-28T09:17:17.729726+00:00

Support Center

Issue Definitions

HTML does not specify charset

HTML does not specify charset

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: HTML does not specify charset

If a response states that it contains HTML content but does not specify a character set, then the browser may analyze the HTML and attempt to determine which character set it appears to be using. Even if the majority of the HTML actually employs a standard character set such as UTF-8, the presence of non-standard characters anywhere in the response may cause the browser to interpret the content using a different character set. This can have unexpected results, and can lead to cross-site scripting vulnerabilities in which non-standard encodings like UTF-7 can be used to bypass the application's defensive filters.

In most cases, the absence of a charset directive does not constitute a security flaw, particularly if the response contains static content. You should review the contents of affected responses, and the context in which they appear, to determine whether any vulnerability exists.

Remediation: HTML does not specify charset

For every response containing HTML content, the application should include within the Content-type header a directive specifying a standard recognized character set, for example charset=ISO-8859-1.

Vulnerability classifications

CWE-16: Configuration

CWE-436: Interpretation Conflict

Typical severity

Information

Type index (hex)

0x00800200

Type index (decimal)

8389120

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
