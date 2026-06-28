# DOM-based cookie manipulation

Source: https://portswigger.net/web-security/dom-based/cookie-manipulation
Fetched: 2026-06-28T09:17:48.295156+00:00

Web Security Academy

DOM-based

Cookie manipulation

DOM-based cookie manipulation

In this section, we'll describe DOM-based cookie manipulation, look at what impact it can have, and suggest ways to reduce your exposure to cookie-manipulation vulnerabilities.

What is DOM-based cookie manipulation?

Some DOM-based vulnerabilities allow attackers to manipulate data that they do not typically control. This transforms normally-safe data types, such as cookies, into potential sources. DOM-based cookie-manipulation vulnerabilities arise when a script writes attacker-controllable data into the value of a cookie.

An attacker may be able to use this vulnerability to construct a URL that, if visited by another user, will set an arbitrary value in the user's cookie. Many sinks are largely harmless on their own, but DOM-based cookie-manipulation attacks demonstrate how low-severity vulnerabilities can sometimes be used as part of an exploit chain for a high-severity attack. For example, if JavaScript writes data from a source into document.cookie without sanitizing it first, an attacker can manipulate the value of a single cookie to inject arbitrary values:

document.cookie = 'cookieName='+location.hash.slice(1);

If the website unsafely reflects values from cookies without HTML-encoding them, an attacker can use cookie-manipulation techniques to exploit this behavior.

What is the impact of a DOM-based cookie-manipulation attack?

The potential impact of this vulnerability depends on the role that the cookie plays within the website. If the cookie is used to control the behavior that results from certain user actions (for example, a production versus demo mode setting), then the attacker may be able to cause the user to perform unintended actions by manipulating the cookie's value.

If the cookie is used to track the user's session, then the attacker may be able to perform a session fixation attack, in which they set the cookie's value to a valid token that they have obtained from the website, and then hijack the session during the victim's subsequent interaction with the website. A cookie-manipulation vulnerability like this can be used to attack not only the vulnerable website, but any other website under the same parent domain.

Which sinks can lead to DOM-based cookie-manipulation vulnerabilities?

The document.cookie sink can lead to DOM-based cookie-manipulation vulnerabilities.

How to prevent DOM-based cookie-manipulation vulnerabilities

In addition to the general measures described on the DOM-based vulnerabilities page, you should avoid dynamically writing to cookies using data that originated from any untrusted source.

Find DOM-based vulnerabilities using Burp Suite

Try for free
