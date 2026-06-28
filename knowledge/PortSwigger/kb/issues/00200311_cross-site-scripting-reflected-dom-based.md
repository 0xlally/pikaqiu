# Cross-site scripting (reflected DOM-based)

Source: https://portswigger.net/kb/issues/00200311_cross-site-scripting-reflected-dom-based
Fetched: 2026-06-28T09:17:07.144132+00:00

Support Center

Issue Definitions

Cross-site scripting (reflected DOM-based)

Cross-site scripting (reflected DOM-based)

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Cross-site scripting (reflected DOM-based)

Reflected DOM-based vulnerabilities arise when data is copied from a request and echoed into the application's immediate response within a part of the DOM that is then processed in an unsafe way by a client-side script. An attacker can leverage the reflection to control a part of the response (for example, a JavaScript string) that can be used to trigger the DOM-based vulnerability.

DOM-based cross-site scripting arises when a script writes controllable data into the HTML document in an unsafe way. An attacker may be able to use the vulnerability to construct a URL that, if visited by another application user, will cause JavaScript code supplied by the attacker to execute within the user's browser in the context of that user's session with the application.

The attacker-supplied code can perform a wide variety of actions, such as stealing the victim's session token or login credentials, performing arbitrary actions on the victim's behalf, and logging their keystrokes.

Users can be induced to visit the attacker's crafted URL in various ways, similar to the usual attack delivery vectors for reflected cross-site scripting vulnerabilities.

Burp Suite automatically identifies this issue using dynamic and static code analysis. Static analysis can lead to false positives that are not actually exploitable. If Burp Scanner has not provided any evidence resulting from dynamic analysis, you should review the relevant code and execution paths to determine whether this vulnerability is indeed present, or whether mitigations are in place that would prevent exploitation.

Remediation: Cross-site scripting (reflected DOM-based)

The most effective way to avoid DOM-based cross-site scripting vulnerabilities is not to dynamically write data from any untrusted source into the HTML document. If the desired functionality of the application means that this behavior is unavoidable, then defenses must be implemented within the client-side code to prevent malicious data from introducing script code into the document. In many cases, the relevant data can be validated on a whitelist basis, to allow only content that is known to be safe. In other cases, it will be necessary to sanitize or encode the data. This can be a complex task, and depending on the context that the data is to be inserted may need to involve a combination of JavaScript escaping, HTML encoding, and URL encoding, in the appropriate sequence.

References

Web Security Academy: Cross-site scripting

Web Security Academy: Reflected cross-site scripting

Web Security Academy: DOM-based cross-site scripting

Vulnerability classifications

CWE-79: Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')

CWE-80: Improper Neutralization of Script-Related HTML Tags in a Web Page (Basic XSS)

CWE-116: Improper Encoding or Escaping of Output

CWE-159: Failure to Sanitize Special Element

CAPEC-591: Reflected XSS

Typical severity

High

Type index (hex)

0x00200311

Type index (decimal)

2097937

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
