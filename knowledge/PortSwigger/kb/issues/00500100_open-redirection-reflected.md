# Open redirection (reflected)

Source: https://portswigger.net/kb/issues/00500100_open-redirection-reflected
Fetched: 2026-06-28T09:17:12.593008+00:00

Support Center

Issue Definitions

Open redirection (reflected)

Open redirection (reflected)

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Open redirection (reflected)

Open redirection vulnerabilities arise when an application incorporates user-controllable data into the target of a redirection in an unsafe way. An attacker can construct a URL within the application that causes a redirection to an arbitrary external domain. This behavior can be leveraged to facilitate phishing attacks against users of the application. The ability to use an authentic application URL, targeting the correct domain and with a valid SSL certificate (if SSL is used), lends credibility to the phishing attack because many users, even if they verify these features, will not notice the subsequent redirection to a different domain.

Remediation: Open redirection (reflected)

If possible, applications should avoid incorporating user-controllable data into redirection targets. In many cases, this behavior can be avoided in two ways:

Remove the redirection function from the application, and replace links to it with direct links to the relevant target URLs.

Maintain a server-side list of all URLs that are permitted for redirection. Instead of passing the target URL as a parameter to the redirector, pass an index into this list.

If it is considered unavoidable for the redirection function to receive user-controllable input and incorporate this into the redirection target, one of the following measures should be used to minimize the risk of redirection attacks:

The application should use relative URLs in all of its redirects, and the redirection function should strictly validate that the URL received is a relative URL.

The application should use URLs relative to the web root for all of its redirects, and the redirection function should validate that the URL received starts with a slash character. It should then prepend http://yourdomainname.com to the URL before issuing the redirect.

The application should use absolute URLs for all of its redirects, and the redirection function should verify that the user-supplied URL begins with http://yourdomainname.com/ before issuing the redirect.

References

Using Burp to Test for Open Redirections

Fun With Redirects

Vulnerability classifications

CWE-601: URL Redirection to Untrusted Site ('Open Redirect')

Typical severity

Low

Type index (hex)

0x00500100

Type index (decimal)

5243136

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
