# DOM data manipulation (reflected DOM-based)

Source: https://portswigger.net/kb/issues/00501201_dom-data-manipulation-reflected-dom-based
Fetched: 2026-06-28T09:17:15.737591+00:00

Support Center

Issue Definitions

DOM data manipulation (reflected DOM-based)

DOM data manipulation (reflected DOM-based)

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: DOM data manipulation (reflected DOM-based)

Reflected DOM-based vulnerabilities arise when data is copied from a request and echoed into the application's immediate response within a part of the DOM that is then processed in an unsafe way by a client-side script. An attacker can leverage the reflection to control a part of the response (for example, a JavaScript string) that can be used to trigger the DOM-based vulnerability.

DOM data manipulation arises when a script writes controllable data to a field within the DOM that is used within the visible UI or client-side application logic. An attacker may be able to use the vulnerability to construct a URL that, if visited by another application user, will modify the appearance or behavior of the client-side UI. An attacker may be able to leverage this to perform virtual defacement of the application, or possibly to induce the user to perform unintended actions.

Burp Suite automatically identifies this issue using dynamic and static code analysis. Static analysis can lead to false positives that are not actually exploitable. If Burp Scanner has not provided any evidence resulting from dynamic analysis, you should review the relevant code and execution paths to determine whether this vulnerability is indeed present, or whether mitigations are in place that would prevent exploitation.

Remediation: DOM data manipulation (reflected DOM-based)

The most effective way to avoid DOM-based DOM data manipulation vulnerabilities is not to dynamically write to DOM data fields any data that originated from any untrusted source. If the desired functionality of the application means that this behavior is unavoidable, then defenses must be implemented within the client-side code to prevent malicious data from being stored. In general, this is best achieved by using a whitelist of permitted values.

References

Web Security Academy: DOM data manipulation

Vulnerability classifications

CWE-20: Improper Input Validation

CAPEC-153: Input Data Manipulation

Typical severity

Information

Type index (hex)

0x00501201

Type index (decimal)

5247489

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
