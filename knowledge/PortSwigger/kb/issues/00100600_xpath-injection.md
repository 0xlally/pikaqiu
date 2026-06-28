# XPath injection

Source: https://portswigger.net/kb/issues/00100600_xpath-injection
Fetched: 2026-06-28T09:17:05.482235+00:00

Support Center

Issue Definitions

XPath injection

XPath injection

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: XPath injection

XPath injection vulnerabilities arise when user-controllable data is incorporated into XPath queries in an unsafe manner. An attacker can supply crafted input to break out of the data context in which their input appears and interfere with the structure of the surrounding query.

Depending on the purpose for which the vulnerable query is being used, an attacker may be able to exploit an XPath injection flaw to read sensitive application data or interfere with application logic.

Remediation: XPath injection

User input should be strictly validated before being incorporated into XPath queries. In most cases, it will be appropriate to accept input containing only short alphanumeric strings. At the very least, input containing any XPath metacharacters such as " ' / @ = * [ ] ( and ) should be rejected.

References

Web Security Academy: Client-side XPath injection (DOM-based)

Vulnerability classifications

CWE-94: Improper Control of Generation of Code ('Code Injection')

CWE-116: Improper Encoding or Escaping of Output

CWE-159: Failure to Sanitize Special Element

CWE-643: Improper Neutralization of Data within XPath Expressions ('XPath Injection')

CAPEC-83: XPath Injection

Typical severity

High

Type index (hex)

0x00100600

Type index (decimal)

1050112

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
