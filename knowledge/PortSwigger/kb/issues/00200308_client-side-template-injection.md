# Client-side template injection

Source: https://portswigger.net/kb/issues/00200308_client-side-template-injection
Fetched: 2026-06-28T09:17:07.179980+00:00

Support Center

Issue Definitions

Client-side template injection

Client-side template injection

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Client-side template injection

Client-side template injection vulnerabilities arise when applications using a client-side template framework dynamically embed user input in web pages. When a web page is rendered, the framework will scan the page for template expressions, and execute any that it encounters. An attacker can exploit this by supplying a malicious template expression that launches a cross-site scripting (XSS) attack. As with normal cross-site scripting, the attacker-supplied code can perform a wide variety of actions, such as stealing the victim's session token or login credentials, performing arbitrary actions on the victim's behalf, and logging their keystrokes.

Users can be induced to issue the attacker's crafted request in various ways. For example, the attacker can send a victim a link containing a malicious URL in an email or instant message. They can submit the link to popular web sites that allow content authoring, for example in blog comments. And they can create an innocuous looking web site that causes anyone viewing it to make arbitrary cross-domain requests to the vulnerable application (using either the GET or the POST method).

The security impact of client-side template injection vulnerabilities is dependent upon the nature of the vulnerable application, the kinds of data and functionality that it contains, and the other applications that belong to the same domain and organization. If the application is used only to display non-sensitive public content, with no authentication or access control functionality, then a client-side template injection flaw may be considered low risk. However, if the same application resides on a domain that can access cookies for other more security-critical applications, then the vulnerability could be used to attack those other applications, and so may be considered high risk. Similarly, if the organization that owns the application is a likely target for phishing attacks, then the vulnerability could be leveraged to lend credibility to such attacks, by injecting Trojan functionality into the vulnerable application and exploiting users' trust in the organization in order to capture credentials for other applications that it owns. In many kinds of application, such as those providing online banking functionality, client-side template injection should always be considered high risk.

Client-side template frameworks often implement a sandbox aimed at hindering direct execution of arbitrary JavaScript from within a template expression. However, these sandboxes are not intended to be a security control and can normally be bypassed.

Browser cross-site scripting filters are typically unable to detect or prevent client-side template injection attacks.

Remediation: Client-side template injection

If possible, avoid using server-side code to dynamically embed user input into client-side templates. If this is not practical, consider filtering out template expression syntax from user input prior to embedding it within client-side templates.

Note that HTML-encoding is not sufficient to prevent client-side template injection attacks, because frameworks perform an HTML-decode of relevant content prior to locating and executing template expressions.

References

XSS without HTML: Client-Side Template Injection with AngularJS. This includes a list of known AngularJS sandbox escapes.

Web Security Academy: AngularJS sandbox escapes

AngularJS Security Considerations

JavaScript MVC Security Pitfalls

Vulnerability classifications

CWE-116: Improper Encoding or Escaping of Output

CWE-159: Failure to Sanitize Special Element

CAPEC-588: DOM-Based XSS

Typical severity

High

Type index (hex)

0x00200308

Type index (decimal)

2097928

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
