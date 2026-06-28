# Cross-site scripting (reflected)

Source: https://portswigger.net/kb/issues/00200300_cross-site-scripting-reflected
Fetched: 2026-06-28T09:17:06.889523+00:00

Support Center

Issue Definitions

Cross-site scripting (reflected)

Cross-site scripting (reflected)

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

What is cross-site scripting?

Cross-site scripting (or XSS) is a common vulnerability that typically allows attackers to hijack other users' online accounts on the affected website.

An attacker can use a cross-site scripting vulnerability to inject some malicious script into the vulnerable application. When a victim user encounters the script, it executes in the victim's browser. The XSS script can then perform any action that the victim is able to perform, and access all of the victim's data. If the victim has special privileges within the application, or has access to sensitive data, this can constitute a serious vulnerability.

Cross-site scripting vulnerabilities normally arise when an application makes use of unvalidated or unencoded data in the responses that it generates. An attacker can manipulate the data to cause their own script code to appear in the application's output to other users.

Note that an attacker does not necessarily need to have direct access to a website in order to exploit it. XSS can sometimes be used to compromise privileged users within an internal application to which the attacker has no direct access.

Description: Cross-site scripting (reflected)

Reflected cross-site scripting vulnerabilities arise when data is copied from a request and echoed into the application's immediate response in an unsafe way. An attacker can use the vulnerability to construct a request that, if issued by another application user, will cause JavaScript code supplied by the attacker to execute within the user's browser in the context of that user's session with the application.

The attacker-supplied code can perform a wide variety of actions, such as stealing the victim's session token or login credentials, performing arbitrary actions on the victim's behalf, and logging their keystrokes.

Users can be induced to issue the attacker's crafted request in various ways. For example, the attacker can send a victim a link containing a malicious URL in an email or instant message. They can submit the link to popular web sites that allow content authoring, for example in blog comments. And they can create an innocuous looking web site that causes anyone viewing it to make arbitrary cross-domain requests to the vulnerable application (using either the GET or the POST method).

The security impact of cross-site scripting vulnerabilities is dependent upon the nature of the vulnerable application, the kinds of data and functionality that it contains, and the other applications that belong to the same domain and organization. If the application is used only to display non-sensitive public content, with no authentication or access control functionality, then a cross-site scripting flaw may be considered low risk. However, if the same application resides on a domain that can access cookies for other more security-critical applications, then the vulnerability could be used to attack those other applications, and so may be considered high risk. Similarly, if the organization that owns the application is a likely target for phishing attacks, then the vulnerability could be leveraged to lend credibility to such attacks, by injecting Trojan functionality into the vulnerable application and exploiting users' trust in the organization in order to capture credentials for other applications that it owns. In many kinds of application, such as those providing online banking functionality, cross-site scripting should always be considered high risk.

Remediation: Cross-site scripting (reflected)

In most situations where user-controllable data is copied into application responses, cross-site scripting attacks can be prevented using two layers of defenses:

Input should be validated as strictly as possible on arrival, given the kind of content that it is expected to contain. For example, personal names should consist of alphabetical and a small range of typographical characters, and be relatively short; a year of birth should consist of exactly four numerals; email addresses should match a well-defined regular expression. Input which fails the validation should be rejected, not sanitized.

User input should be HTML-encoded at any point where it is copied into application responses. All HTML metacharacters, including < > " ' and =, should be replaced with the corresponding HTML entities (&lt; &gt; etc).

In cases where the application's functionality allows users to author content using a restricted subset of HTML tags and attributes (for example, blog comments which allow limited formatting and linking), it is necessary to parse the supplied HTML to validate that it does not use any dangerous syntax; this is a non-trivial task.

References

Web Security Academy: Cross-site scripting

Web Security Academy: Reflected cross-site scripting

Using Burp to Find XSS issues

Vulnerability classifications

CWE-79: Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')

CWE-80: Improper Neutralization of Script-Related HTML Tags in a Web Page (Basic XSS)

CWE-116: Improper Encoding or Escaping of Output

CWE-159: Failure to Sanitize Special Element

CAPEC-591: Reflected XSS

Typical severity

High

Type index (hex)

0x00200300

Type index (decimal)

2097920

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
