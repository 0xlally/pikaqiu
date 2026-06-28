# Cross-domain Referer leakage

Source: https://portswigger.net/kb/issues/00500400_cross-domain-referer-leakage
Fetched: 2026-06-28T09:17:13.395181+00:00

Support Center

Issue Definitions

Cross-domain Referer leakage

Cross-domain Referer leakage

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Cross-domain Referer leakage

When a web browser makes a request for a resource, it typically adds an HTTP header, called the "Referer" header, indicating the URL of the resource from which the request originated. This occurs in numerous situations, for example when a web page loads an image or script, or when a user clicks on a link or submits a form.

If the resource being requested resides on a different domain, then the Referer header is still generally included in the cross-domain request. If the originating URL contains any sensitive information within its query string, such as a session token, then this information will be transmitted to the other domain. If the other domain is not fully trusted by the application, then this may lead to a security compromise.

You should review the contents of the information being transmitted to other domains, and also determine whether those domains are fully trusted by the originating application.

Today's browsers may withhold the Referer header in some situations (for example, when loading a non-HTTPS resource from a page that was loaded over HTTPS, or when a Refresh directive is issued), but this behavior should not be relied upon to protect the originating URL from disclosure.

Note also that if users can author content within the application then an attacker may be able to inject links referring to a domain they control in order to capture data from URLs used within the application.

Remediation: Cross-domain Referer leakage

Applications should never transmit any sensitive information within the URL query string. In addition to being leaked in the Referer header, such information may be logged in various locations and may be visible on-screen to untrusted parties. If placing sensitive information in the URL is unavoidable, consider using the Referer-Policy HTTP header to reduce the chance of it being disclosed to third parties.

References

Referer Policy

Web Security Academy: Information disclosure

Vulnerability classifications

CWE-200: Information Exposure

Typical severity

Information

Type index (hex)

0x00500400

Type index (decimal)

5243904

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
