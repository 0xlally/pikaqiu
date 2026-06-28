# DOM-based client-side XPath injection

Source: https://portswigger.net/web-security/dom-based/client-side-xpath-injection
Fetched: 2026-06-28T09:17:48.226291+00:00

Web Security Academy

DOM-based

Client-side XPath injection

DOM-based client-side XPath injection

In this section, we'll look at what DOM-based XPath-injection is, discuss the potential impact of this kind of vulnerability, and suggest ways to reduce your exposure to them.

What is DOM-based XPath injection?

DOM-based XPath-injection vulnerabilities arise when a script incorporates attacker-controllable data into an XPath query. An attacker may be able to use this behavior to construct a URL that, if visited by another application user, will trigger the execution of an arbitrary XPath query, which could cause different data to be retrieved and processed by the website.

What is the impact of DOM-based XPath injection?

Depending on the purpose for which the query results are used, it may be possible for the attacker to subvert the website's logic or cause unintended actions on behalf of the user.

Which sinks can lead to XPath-injection vulnerabilities?

The following are some of the main sinks that can lead to DOM-based XPath-injection vulnerabilities:

document.evaluate()

element.evaluate()

How to prevent DOM-based XPath-injection vulnerabilities

In addition to the general measures described on the DOM-based vulnerabilities page, you should avoid allowing data from any untrusted source to be incorporated into XPath queries.

Find DOM-based vulnerabilities using Burp Suite

Try for free
