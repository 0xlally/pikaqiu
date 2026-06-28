# Frameable response (potential Clickjacking)

Source: https://portswigger.net/kb/issues/005009a0_frameable-response-potential-clickjacking
Fetched: 2026-06-28T09:17:14.219757+00:00

Support Center

Issue Definitions

Frameable response (potential Clickjacking)

Frameable response (potential Clickjacking)

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Frameable response (potential Clickjacking)

If a page fails to set an appropriate X-Frame-Options or Content-Security-Policy HTTP header, it might be possible for a page controlled by an attacker to load it within an iframe. This may enable a clickjacking attack, in which the attacker's page overlays the target application's interface with a different interface provided by the attacker. By inducing victim users to perform actions such as mouse clicks and keystrokes, the attacker can cause them to unwittingly carry out actions within the application that is being targeted. This technique allows the attacker to circumvent defenses against cross-site request forgery, and may result in unauthorized actions.

Note that some applications attempt to prevent these attacks from within the HTML page itself, using "framebusting" code. However, this type of defense is normally ineffective and can usually be circumvented by a skilled attacker.

You should determine whether any functions accessible within frameable pages can be used by application users to perform any sensitive actions within the application.

Remediation: Frameable response (potential Clickjacking)

To effectively prevent framing attacks, the application should return a response header with the name X-Frame-Options and the value DENY to prevent framing altogether, or the value SAMEORIGIN to allow framing only by pages on the same origin as the response itself. Note that the SAMEORIGIN header can be partially bypassed if the application itself can be made to frame untrusted websites.

References

Web Security Academy: Clickjacking

X-Frame-Options

Vulnerability classifications

CWE-693: Protection Mechanism Failure

CWE-1021: Improper Restriction of Rendered UI Layers or Frames

CAPEC-103: Clickjacking

Typical severity

Information

Type index (hex)

0x005009a0

Type index (decimal)

5245344

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
