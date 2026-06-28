# DOM-data manipulation

Source: https://portswigger.net/web-security/dom-based/dom-data-manipulation
Fetched: 2026-06-28T09:17:48.702195+00:00

Web Security Academy

DOM-based

DOM-data manipulation

DOM-data manipulation

In this section, we'll look at what DOM-data manipulation is, discuss the potential impact of this kind of attack, and look at ways to reduce your exposure to DOM-data manipulation vulnerabilities.

What is DOM-data manipulation?

DOM-data manipulation vulnerabilities arise when a script writes attacker-controllable data to a field within the DOM that is used within the visible UI or client-side logic. An attacker may be able to use this vulnerability to construct a URL that, if visited by another user, will modify the appearance or behavior of the client-side UI. DOM-data manipulation vulnerabilities can be exploited by both reflected and stored DOM-based attacks.

What is the impact of DOM-data manipulation?

At the lesser end of the scale, an attacker may be able to leverage this vulnerability to perform virtual defacement of the website, such as changing text or images that are displayed on a particular page. However, attacks can be more severe. For example, if the attacker is able to change the src property of an element, they could potentially induce the user to perform unintended actions by importing a malicious JavaScript file.

Which sinks can lead to DOM-data manipulation vulnerabilities?

The following are some of the main sinks that can lead to DOM-data manipulation vulnerabilities:

script.src

script.text

script.textContent

script.innerText

element.setAttribute()

element.search

element.text

element.textContent

element.innerText

element.outerText

element.value

element.name

element.target

element.method

element.type

element.backgroundImage

element.cssText

element.codebase

document.title

document.implementation.createHTMLDocument()

history.pushState()

history.replaceState()

How to prevent DOM-data manipulation vulnerabilities

In addition to the general measures described on the DOM-based vulnerabilities page, you should avoid allowing data from any untrusted source to be dynamically written to DOM-data fields.

Note that Burp Suite automatically identifies this issue using static code analysis, which may lead to false positives that are not actually exploitable. The relevant code and execution paths should be reviewed to determine whether this vulnerability is indeed present, or whether mitigations are in place that would prevent exploitation.

Find DOM-based vulnerabilities using Burp Suite

Try for free
