# Client-side XPath injection (DOM-based)

Source: https://portswigger.net/kb/issues/00200360_client-side-xpath-injection-dom-based
Fetched: 2026-06-28T09:17:08.455128+00:00

Support Center

Issue Definitions

Client-side XPath injection (DOM-based)

Client-side XPath injection (DOM-based)

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Client-side XPath injection (DOM-based)

DOM-based vulnerabilities arise when a client-side script reads data from a controllable part of the DOM (for example, the URL) and processes this data in an unsafe way.

DOM-based XPath injection arises when a script incorporates controllable data into an XPath query. An attacker may be able to use this behavior to construct a URL that, if visited by another application user, will cause an arbitrary XPath query to execute, causing different data to be retrieved and processed by the application. Depending on the purpose for which the query results are used, it may be possible to subvert the application's logic, or cause unintended actions on behalf of the user.

Burp Suite automatically identifies this issue using dynamic and static code analysis. Static analysis can lead to false positives that are not actually exploitable. If Burp Scanner has not provided any evidence resulting from dynamic analysis, you should review the relevant code and execution paths to determine whether this vulnerability is indeed present, or whether mitigations are in place that would prevent exploitation.

Remediation: Client-side XPath injection (DOM-based)

The most effective way to avoid DOM-based XPath injection vulnerabilities is not to incorporate into an XPath query any data that originated from an untrusted source. If the desired functionality of the application means that this behavior is unavoidable, then defenses must be implemented within the client-side code to prevent malicious data from modifying the XPath query in inappropriate ways. This may involve strict validation of specific items to ensure they do not contain any characters that may interfere with the structure of the query when it is parsed.

References

Web Security Academy: Client-side XPath injection (DOM-based)

Vulnerability classifications

CWE-79: Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')

CWE-116: Improper Encoding or Escaping of Output

CWE-159: Failure to Sanitize Special Element

CAPEC-83: XPath Injection

Typical severity

Low

Type index (hex)

0x00200360

Type index (decimal)

2098016

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
