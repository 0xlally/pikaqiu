# HTML5 web message manipulation (stored DOM-based)

Source: https://portswigger.net/kb/issues/00500e02_html5-web-message-manipulation-stored-dom-based
Fetched: 2026-06-28T09:17:14.503829+00:00

Support Center

Issue Definitions

HTML5 web message manipulation (stored DOM-based)

HTML5 web message manipulation (stored DOM-based)

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: HTML5 web message manipulation (stored DOM-based)

Stored DOM-based vulnerabilities arise when user input is stored and later embedded into a response within a part of the DOM that is then processed in an unsafe way by a client-side script. An attacker can leverage the data storage to control a part of the response (for example, a JavaScript string) that can be used to trigger the DOM-based vulnerability.

HTML5 web message manipulation arises when a script sends controllable data as a web message to another document within the browser. An attacker may be able to use the vulnerability to construct a URL that, if visited by another application user, will cause the user's browser to send a web message containing data that is under the attacker's control.

The potential impact of the vulnerability depends on the destination document's handling of the incoming message. If the destination document trusts the sender not to transmit malicious data in the message, and handles the data in an unsafe manner, then the joint behavior of the two documents may allow an attacker to compromise the application user.

Burp Suite automatically identifies this issue using dynamic and static code analysis. Static analysis can lead to false positives that are not actually exploitable. If Burp Scanner has not provided any evidence resulting from dynamic analysis, you should review the relevant code and execution paths to determine whether this vulnerability is indeed present, or whether mitigations are in place that would prevent exploitation.

Remediation: HTML5 web message manipulation (stored DOM-based)

The most effective way to avoid DOM-based HTML5 web message manipulation vulnerabilities is not to send a web message containing data that originated from any untrusted source. If the desired functionality of the application means that this behavior is unavoidable, then defenses must be implemented within the client-side code to prevent malicious data from compromising the user. This validation can be carried out by the document that sends the message, or by the document that receives the message, or both, depending on the trust relationship between the two documents.

References

Web Security Academy: Web message manipulation (DOM-based)

Vulnerability classifications

CWE-20: Improper Input Validation

CAPEC-153: Input Data Manipulation

Typical severity

Information

Type index (hex)

0x00500e02

Type index (decimal)

5246466

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
