# DOM-based document-domain manipulation

Source: https://portswigger.net/web-security/dom-based/document-domain-manipulation
Fetched: 2026-06-28T09:17:48.495889+00:00

Web Security Academy

DOM-based

Document-domain manipulation

DOM-based document-domain manipulation

In this section, we'll describe DOM-based manipulation of the document.domain property and suggest ways to reduce your exposure to this kind of attack.

What is DOM-based document-domain manipulation?

Document-domain manipulation vulnerabilities arise when a script uses attacker-controllable data to set the document.domain property. An attacker may be able to use the vulnerability to construct a URL that, if visited by another user, will cause the response page to set an arbitrary document.domain value.

The document.domain property is used by browsers in their enforcement of the same origin policy. If two pages from different origins explicitly set the same document.domain value, then those two pages can interact in unrestricted ways. If an attacker can cause a page of a targeted website and another page they control (either directly, or via an XSS-like vulnerability) to set the same document.domain value, then the attacker may be able to fully compromise the target page via the page they already control. This opens up the same possibilities for exploitation as regular cross-site scripting (XSS) vulnerabilities.

Browsers generally enforce some restrictions on the values that can be assigned to document.domain, and may prevent the use of completely different values than the actual origin of the page. However, there are two important caveats to this. Firstly, browsers allow the use of child or parent domains, so an attacker may be able to switch the domain of the target page to that of a related website with a weaker security posture. Secondly, some browser quirks enable switching to completely unrelated domains. These caveats mean that the ability to manipulate the document.domain property of a page generally represents a security vulnerability whose severity is not far behind regular XSS.

Which sinks can lead to DOM-based document-domain manipulation vulnerabilities?

The document.domain sink can lead to DOM-based document-domain manipulation vulnerabilities.

How to prevent DOM-based document-domain manipulation vulnerabilities

In addition to the general measures described on the DOM-based vulnerabilities page, you should avoid allowing data from any untrusted source to dynamically set the document.domain property.

Find DOM-based vulnerabilities using Burp Suite

Try for free
