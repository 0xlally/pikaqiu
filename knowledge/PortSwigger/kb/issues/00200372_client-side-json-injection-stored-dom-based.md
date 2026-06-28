# Client-side JSON injection (stored DOM-based)

Source: https://portswigger.net/kb/issues/00200372_client-side-json-injection-stored-dom-based
Fetched: 2026-06-28T09:17:08.459819+00:00

Support Center

Issue Definitions

Client-side JSON injection (stored DOM-based)

Client-side JSON injection (stored DOM-based)

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Client-side JSON injection (stored DOM-based)

Stored DOM-based vulnerabilities arise when user input is stored and later embedded into a response within a part of the DOM that is then processed in an unsafe way by a client-side script. An attacker can leverage the data storage to control a part of the response (for example, a JavaScript string) that can be used to trigger the DOM-based vulnerability.

DOM-based JSON injection arises when a script incorporates controllable data into a string that is parsed as a JSON data structure and then processed by the application. An attacker may be able to use this behavior to construct a URL that, if visited by another application user, will cause arbitrary JSON data to be processed. Depending on the purpose for which this data is used, it may be possible to subvert the application's logic, or cause unintended actions on behalf of the user.

Burp Suite automatically identifies this issue using dynamic and static code analysis. Static analysis can lead to false positives that are not actually exploitable. If Burp Scanner has not provided any evidence resulting from dynamic analysis, you should review the relevant code and execution paths to determine whether this vulnerability is indeed present, or whether mitigations are in place that would prevent exploitation.

Remediation: Client-side JSON injection (stored DOM-based)

The most effective way to avoid DOM-based JSON injection vulnerabilities is not to parse as JSON any string containing data that originated from an untrusted source. If the desired functionality of the application means that this behavior is unavoidable, then defenses must be implemented within the client-side code to prevent malicious data from modifying the JSON structure in inappropriate ways. This may involve strict validation of specific items to ensure they do not contain any characters that may interfere with the structure of the JSON when it is parsed.

References

Web Security Academy: Client-side JSON injection (DOM-based)

Vulnerability classifications

CWE-79: Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')

CWE-116: Improper Encoding or Escaping of Output

CWE-159: Failure to Sanitize Special Element

CAPEC-153: Input Data Manipulation

Typical severity

Low

Type index (hex)

0x00200372

Type index (decimal)

2098034

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
