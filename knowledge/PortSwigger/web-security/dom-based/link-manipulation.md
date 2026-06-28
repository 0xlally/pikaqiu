# DOM-based link manipulation

Source: https://portswigger.net/web-security/dom-based/link-manipulation
Fetched: 2026-06-28T09:17:48.939202+00:00

Web Security Academy

DOM-based

Link manipulation

DOM-based link manipulation

In this section, we'll talk about what DOM-based link manipulation is, look at the impact of an attack, and suggest ways of preventing them.

What is DOM-based link manipulation?

DOM-based link-manipulation vulnerabilities arise when a script writes attacker-controllable data to a navigation target within the current page, such as a clickable link or the submission URL of a form. An attacker might be able to use this vulnerability to construct a URL that, if visited by another application user, will modify the target of links within the response.

What is the impact of a DOM-based link-manipulation attack?

An attacker may be able to leverage this vulnerability to perform various attacks, including:

Causing the user to be redirected to an arbitrary external URL, which could facilitate a phishing attack.

Causing the user to submit sensitive form data to a server controlled by the attacker.

Changing the file or query string associated with a link, causing the user to perform an unintended action within the application.

Bypassing browser anti-XSS defenses by injecting on-site links containing XSS exploits. This works because anti-XSS defenses do not typically account for on-site links.

Which sinks can lead to DOM-based link-manipulation vulnerabilities?

The following are some of the main sinks can lead to DOM-based link-manipulation vulnerabilities:

element.href

element.src

element.action

How to prevent DOM-based link-manipulation vulnerabilities

In addition to the general measures described on the DOM-based vulnerabilities page, you should avoid allowing data from any untrusted source to dynamically set the target URL for links or forms.

Find DOM-based vulnerabilities using Burp Suite

Try for free
