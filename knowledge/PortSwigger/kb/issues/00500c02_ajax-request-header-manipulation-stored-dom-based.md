# Ajax request header manipulation (stored DOM-based)

Source: https://portswigger.net/kb/issues/00500c02_ajax-request-header-manipulation-stored-dom-based
Fetched: 2026-06-28T09:17:14.197444+00:00

Support Center

Issue Definitions

Ajax request header manipulation (stored DOM-based)

Ajax request header manipulation (stored DOM-based)

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Ajax request header manipulation (stored DOM-based)

Stored DOM-based vulnerabilities arise when user input is stored and later embedded into a response within a part of the DOM that is then processed in an unsafe way by a client-side script. An attacker can leverage the data storage to control a part of the response (for example, a JavaScript string) that can be used to trigger the DOM-based vulnerability.

Ajax request header manipulation arises when a script writes controllable data into a header of an Ajax request that is issued using XmlHttpRequest. An attacker may be able to use the vulnerability to construct a URL that, if visited by another application user, will set an arbitrary header in the subsequent Ajax request.

The potential impact of the vulnerability depends on the role of specific HTTP headers in the server-side application's processing of the Ajax request. If the header is used to control the behavior that results from the Ajax request, then the attacker may be able to cause the user to perform unintended actions by manipulating the header.

Burp Suite automatically identifies this issue using dynamic and static code analysis. Static analysis can lead to false positives that are not actually exploitable. If Burp Scanner has not provided any evidence resulting from dynamic analysis, you should review the relevant code and execution paths to determine whether this vulnerability is indeed present, or whether mitigations are in place that would prevent exploitation.

Remediation: Ajax request header manipulation (stored DOM-based)

The most effective way to avoid DOM-based Ajax request header manipulation vulnerabilities is not to dynamically set Ajax request headers using data that originated from any untrusted source. This behavior should never be implemented for headers that have any role in controlling the effects of privileged actions within the application.

References

Web Security Academy: Ajax request header manipulation (DOM-based)

Vulnerability classifications

CWE-116: Improper Encoding or Escaping of Output

CAPEC-6: Argument Injection

Typical severity

Low

Type index (hex)

0x00500c02

Type index (decimal)

5245954

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
