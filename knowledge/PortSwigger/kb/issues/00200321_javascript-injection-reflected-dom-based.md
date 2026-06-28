# JavaScript injection (reflected DOM-based)

Source: https://portswigger.net/kb/issues/00200321_javascript-injection-reflected-dom-based
Fetched: 2026-06-28T09:17:07.207863+00:00

Support Center

Issue Definitions

JavaScript injection (reflected DOM-based)

JavaScript injection (reflected DOM-based)

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: JavaScript injection (reflected DOM-based)

Reflected DOM-based vulnerabilities arise when data is copied from a request and echoed into the application's immediate response within a part of the DOM that is then processed in an unsafe way by a client-side script. An attacker can leverage the reflection to control a part of the response (for example, a JavaScript string) that can be used to trigger the DOM-based vulnerability.

DOM-based JavaScript injection arises when a script executes controllable data as JavaScript. An attacker may be able to use the vulnerability to construct a URL that, if visited by another application user, will cause JavaScript code supplied by the attacker to execute within the user's browser in the context of that user's session with the application.

The attacker-supplied code can perform a wide variety of actions, such as stealing the victim's session token or login credentials, performing arbitrary actions on the victim's behalf, and logging their keystrokes.

Users can be induced to visit the attacker's crafted URL in various ways, similar to the usual attack delivery vectors for reflected cross-site scripting vulnerabilities.

Burp Suite automatically identifies this issue using dynamic and static code analysis. Static analysis can lead to false positives that are not actually exploitable. If Burp Scanner has not provided any evidence resulting from dynamic analysis, you should review the relevant code and execution paths to determine whether this vulnerability is indeed present, or whether mitigations are in place that would prevent exploitation.

Remediation: JavaScript injection (reflected DOM-based)

The most effective way to avoid DOM-based JavaScript injection vulnerabilities is not to execute as JavaScript any data that originated from an untrusted source. If the desired functionality of the application means that this behavior is unavoidable, then defenses must be implemented within the client-side code to prevent malicious data from executing as script. In many cases, the relevant data can be validated on a whitelist basis, to allow only content that is known to be safe. In other cases, it will be necessary to sanitize or encode the data. This can be a complex task, and may need to involve a combination of JavaScript escaping and HTML encoding, in the appropriate sequence.

References

Web Security Academy: JavaScript injection (DOM-based)

Vulnerability classifications

CWE-94: Improper Control of Generation of Code ('Code Injection')

CWE-95: Improper Neutralization of Directives in Dynamically Evaluated Code ('Eval Injection')

CWE-116: Improper Encoding or Escaping of Output

CAPEC-63: Cross-Site Scripting (XSS)

Typical severity

High

Type index (hex)

0x00200321

Type index (decimal)

2097953

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
