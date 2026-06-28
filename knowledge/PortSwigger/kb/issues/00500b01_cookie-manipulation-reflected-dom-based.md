# Cookie manipulation (reflected DOM-based)

Source: https://portswigger.net/kb/issues/00500b01_cookie-manipulation-reflected-dom-based
Fetched: 2026-06-28T09:17:13.800228+00:00

Support Center

Issue Definitions

Cookie manipulation (reflected DOM-based)

Cookie manipulation (reflected DOM-based)

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Cookie manipulation (reflected DOM-based)

Reflected DOM-based vulnerabilities arise when data is copied from a request and echoed into the application's immediate response within a part of the DOM that is then processed in an unsafe way by a client-side script. An attacker can leverage the reflection to control a part of the response (for example, a JavaScript string) that can be used to trigger the DOM-based vulnerability.

DOM-based cookie manipulation arises when a script writes controllable data into the value of a cookie. An attacker may be able to use the vulnerability to construct a URL that, if visited by another application user, will set an arbitrary value in the user's cookie.

The potential impact of the vulnerability depends on the role that the cookie plays within the application. If the cookie is used to control the behavior that results from certain user actions (for example, a 'production' versus 'demo' mode setting), then the attacker may be able to cause the user to perform unintended actions by manipulating the cookie's value. If the cookie is used to track the user's session, then the attacker may be able to perform a session fixation attack, in which they set the cookie's value to a valid token that they have obtained from the application, and then hijack the session during the victim user's subsequent interaction with the application.

Burp Suite automatically identifies this issue using dynamic and static code analysis. Static analysis can lead to false positives that are not actually exploitable. If Burp Scanner has not provided any evidence resulting from dynamic analysis, you should review the relevant code and execution paths to determine whether this vulnerability is indeed present, or whether mitigations are in place that would prevent exploitation.

Remediation: Cookie manipulation (reflected DOM-based)

The most effective way to avoid DOM-based cookie manipulation vulnerabilities is not to dynamically write to cookies using data that originated from any untrusted source. This behavior should never be implemented for cookies that have any role in controlling privileged actions or user sessions within the application.

References

Web Security Academy: Cookie manipulation (DOM-based)

Vulnerability classifications

CWE-565: Reliance on Cookies without Validation and Integrity Checking

CWE-829: Inclusion of Functionality from Untrusted Control Sphere

CAPEC-31: Accessing/Intercepting/Modifying HTTP Cookies

Typical severity

Low

Type index (hex)

0x00500b01

Type index (decimal)

5245697

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
