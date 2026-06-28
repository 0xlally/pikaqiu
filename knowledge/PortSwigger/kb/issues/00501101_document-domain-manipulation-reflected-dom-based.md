# Document domain manipulation (reflected DOM-based)

Source: https://portswigger.net/kb/issues/00501101_document-domain-manipulation-reflected-dom-based
Fetched: 2026-06-28T09:17:15.587411+00:00

Support Center

Issue Definitions

Document domain manipulation (reflected DOM-based)

Document domain manipulation (reflected DOM-based)

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Document domain manipulation (reflected DOM-based)

Reflected DOM-based vulnerabilities arise when data is copied from a request and echoed into the application's immediate response within a part of the DOM that is then processed in an unsafe way by a client-side script. An attacker can leverage the reflection to control a part of the response (for example, a JavaScript string) that can be used to trigger the DOM-based vulnerability.

Document domain manipulation arises when a script uses controllable data to set the document.domain property. An attacker may be able to use the vulnerability to construct a URL that, if visited by another application user, will cause the response page to set an arbitrary document.domain value.

The document.domain property is used by browsers in their enforcement of the same origin policy. If two pages from different origins explicitly set the same document.domain value, then those two pages can interact in unrestricted ways. If an attacker can cause a page of a targeted application, and another page they control (either directly, or via an XSS-like vulnerability), to set the same document.domain value, then the attacker may be able to fully compromise the targeted application page via the page they already control, with the same possibilities for exploitation as regular cross-site scripting (XSS) vulnerabilities.

Browsers generally enforce some restrictions on the values that can be assigned to document.domain, and may prevent the use of completely different values than the actual origin of the page. However, there are two important caveats to this. Firstly, browsers allow the use of child or parent domains, so an attacker may be able to switch the domain of the targeted application page to that of a related application with a weaker security posture. Secondly, some browser quirks enable switching to completely unrelated domains. These caveats mean that the ability to manipulate the document.domain property of a page generally represents a security vulnerability whose severity is not far behind regular XSS.

Burp Suite automatically identifies this issue using dynamic and static code analysis. Static analysis can lead to false positives that are not actually exploitable. If Burp Scanner has not provided any evidence resulting from dynamic analysis, you should review the relevant code and execution paths to determine whether this vulnerability is indeed present, or whether mitigations are in place that would prevent exploitation.

Remediation: Document domain manipulation (reflected DOM-based)

The most effective way to avoid DOM-based document domain manipulation vulnerabilities is not to dynamically set the document.domain property using data that originated from any untrusted source. If it is necessary to programmatically set the document.domain property from within client-side code, then the application should employ a set list of acceptable values, and assign only from values in that list.

References

Web Security Academy: Document domain manipulation (DOM-based)

Vulnerability classifications

CWE-20: Improper Input Validation

CAPEC-153: Input Data Manipulation

Typical severity

Medium

Type index (hex)

0x00501101

Type index (decimal)

5247233

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
