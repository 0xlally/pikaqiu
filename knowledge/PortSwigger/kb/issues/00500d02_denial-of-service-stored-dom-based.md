# Denial of service (stored DOM-based)

Source: https://portswigger.net/kb/issues/00500d02_denial-of-service-stored-dom-based
Fetched: 2026-06-28T09:17:14.164174+00:00

Support Center

Issue Definitions

Denial of service (stored DOM-based)

Denial of service (stored DOM-based)

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Denial of service (stored DOM-based)

Stored DOM-based vulnerabilities arise when user input is stored and later embedded into a response within a part of the DOM that is then processed in an unsafe way by a client-side script. An attacker can leverage the data storage to control a part of the response (for example, a JavaScript string) that can be used to trigger the DOM-based vulnerability.

DOM-based denial of service arises when a script passes controllable data to a problematic platform API in an unsafe way. An attacker may be able to use the vulnerability to construct a URL that, if visited by another application user, will cause a denial of service condition on the user's computer when the relevant API is invoked. Depending on the nature of the API, the invocation may cause the user's computer to consume excessive amounts of CPU or disk space. This may result in side effects if the web browser restricts application functionality; for example, by rejecting attempts to store data in localStorage or killing busy scripts.

Burp Suite automatically identifies this issue using dynamic and static code analysis. Static analysis can lead to false positives that are not actually exploitable. If Burp Scanner has not provided any evidence resulting from dynamic analysis, you should review the relevant code and execution paths to determine whether this vulnerability is indeed present, or whether mitigations are in place that would prevent exploitation.

Remediation: Denial of service (stored DOM-based)

The most effective way to avoid DOM-based denial of service vulnerabilities is not to dynamically pass data into problematic platform APIs that originated from any untrusted source. If the desired functionality of the application means that this behavior is unavoidable, then defenses must be implemented within the client-side code to prevent malicious data from causing a denial of service condition. In many cases, the relevant data can be validated on a whitelist basis, to allow only content that is known to be safe.

References

Web Security Academy: Denial of service (DOM-based)

Vulnerability classifications

CWE-400: Uncontrolled Resource Consumption ('Resource Exhaustion')

CAPEC-125: Flooding

Typical severity

Low

Type index (hex)

0x00500d02

Type index (decimal)

5246210

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
