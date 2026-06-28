# HTML5 storage manipulation (DOM-based)

Source: https://portswigger.net/kb/issues/00500f00_html5-storage-manipulation-dom-based
Fetched: 2026-06-28T09:17:14.604374+00:00

Support Center

Issue Definitions

HTML5 storage manipulation (DOM-based)

HTML5 storage manipulation (DOM-based)

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: HTML5 storage manipulation (DOM-based)

DOM-based vulnerabilities arise when a client-side script reads data from a controllable part of the DOM (for example, the URL) and processes this data in an unsafe way.

HTML5 storage manipulation arises when a script stores controllable data in the HTML5 storage of the web browser (either localStorage or sessionStorage). An attacker may be able to use this behavior to construct a URL that, if visited by another application user, will cause the user's browser to store attacker-controllable data.

This behavior does not in itself constitute a security vulnerability. However, if the application later reads the data back from storage and processes it in an unsafe way, then an attacker may be able to leverage the storage mechanism to deliver other DOM-based attacks, such as cross-site scripting and JavaScript injection.

Burp Suite automatically identifies this issue using dynamic and static code analysis. Static analysis can lead to false positives that are not actually exploitable. If Burp Scanner has not provided any evidence resulting from dynamic analysis, you should review the relevant code and execution paths to determine whether this vulnerability is indeed present, or whether mitigations are in place that would prevent exploitation.

Remediation: HTML5 storage manipulation (DOM-based)

The most effective way to avoid DOM-based HTML5 storage manipulation is not to place in HTML5 storage any data that originated from any untrusted source. If the desired functionality of the application means that this behavior is unavoidable, then defenses must be implemented within the client-side code to prevent malicious data from being stored.

References

Web Security Academy: HTML5 storage manipulation (DOM-based)

Vulnerability classifications

CWE-20: Improper Input Validation

CAPEC-153: Input Data Manipulation

Typical severity

Information

Type index (hex)

0x00500f00

Type index (decimal)

5246720

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
