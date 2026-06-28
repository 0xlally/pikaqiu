# Link manipulation (DOM-based)

Source: https://portswigger.net/kb/issues/00501000_link-manipulation-dom-based
Fetched: 2026-06-28T09:17:15.143655+00:00

Support Center

Issue Definitions

Link manipulation (DOM-based)

Link manipulation (DOM-based)

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Link manipulation (DOM-based)

DOM-based vulnerabilities arise when a client-side script reads data from a controllable part of the DOM (for example, the URL) and processes this data in an unsafe way.

DOM-based link manipulation arises when a script writes controllable data to a navigation target within the current page, such as a clickable link or the submission URL of a form. An attacker may be able to use the vulnerability to construct a URL that, if visited by another application user, will modify the target of links within the response. An attacker may be able to leverage this to perform various attacks, including:

Causing the user to redirect to an arbitrary external URL, to facilitate a phishing attack.

Causing the user to submit sensitive form data to a server controlled by the attacker.

Causing the user to perform an unintended action within the application, by changing the file or query string associated with a link.

Bypassing browser anti-XSS defenses by injecting on-site links containing XSS exploits, since browser anti-XSS defenses typically do not operate on on-site links.

Burp Suite automatically identifies this issue using dynamic and static code analysis. Static analysis can lead to false positives that are not actually exploitable. If Burp Scanner has not provided any evidence resulting from dynamic analysis, you should review the relevant code and execution paths to determine whether this vulnerability is indeed present, or whether mitigations are in place that would prevent exploitation.

Remediation: Link manipulation (DOM-based)

The most effective way to avoid DOM-based link manipulation vulnerabilities is not to dynamically set the target URLs of links or forms using data that originated from any untrusted source. If the desired functionality of the application means that this behavior is unavoidable, then defenses must be implemented within the client-side code to prevent malicious data from introducing an arbitrary URL as a link target. In general, this is best achieved by using a whitelist of URLs that are permitted link targets, and strictly validating the target against this list before setting the link target.

References

Web Security Academy: Link manipulation (DOM-based)

Vulnerability classifications

CWE-20: Improper Input Validation

CAPEC-153: Input Data Manipulation

Typical severity

Low

Type index (hex)

0x00501000

Type index (decimal)

5246976

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
