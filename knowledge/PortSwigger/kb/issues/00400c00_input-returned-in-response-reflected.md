# Input returned in response (reflected)

Source: https://portswigger.net/kb/issues/00400c00_input-returned-in-response-reflected
Fetched: 2026-06-28T09:17:11.901644+00:00

Support Center

Issue Definitions

Input returned in response (reflected)

Input returned in response (reflected)

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Input returned in response (reflected)

Reflection of input arises when data is copied from a request and echoed into the application's immediate response.

Input being returned in application responses is not a vulnerability in its own right. However, it is a prerequisite for many client-side vulnerabilities, including cross-site scripting, open redirection, content spoofing, and response header injection. Additionally, some server-side vulnerabilities such as SQL injection are often easier to identify and exploit when input is returned in responses. In applications where input retrieval is rare and the environment is resistant to automated testing (for example, due to a web application firewall), it might be worth subjecting instances of it to focused manual testing.

Vulnerability classifications

CWE-20: Improper Input Validation

CWE-116: Improper Encoding or Escaping of Output

Typical severity

Information

Type index (hex)

0x00400c00

Type index (decimal)

4197376

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
