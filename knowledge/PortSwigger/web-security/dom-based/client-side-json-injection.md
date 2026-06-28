# DOM-based client-side JSON injection

Source: https://portswigger.net/web-security/dom-based/client-side-json-injection
Fetched: 2026-06-28T09:17:47.935573+00:00

Web Security Academy

DOM-based

Client-side JSON injection

DOM-based client-side JSON injection

In this section, we'll describe client-side JSON injection as related to the DOM, look at how damaging such an attack could be, and suggest ways to reduce your exposure to this kind of vulnerability.

What is DOM-based JSON injection?

DOM-based JSON-injection vulnerabilities arise when a script incorporates attacker-controllable data into a string that is parsed as a JSON data structure and then processed by the application. An attacker may be able to use this behavior to construct a URL that, if visited by another user, will cause arbitrary JSON data to be processed.

What is the impact of a DOM-based JSON-injection attack?

Depending on the purpose for which this data is used, it may be possible for an attacker to subvert the website's logic, or cause unintended actions on behalf of another user.

Which sinks can lead to DOM-based JSON-injection vulnerabilities?

JSON.parse()

jQuery.parseJSON()

$.parseJSON()

How to prevent client-side JSON-injection vulnerabilities?

In addition to the general measures described on the DOM-based vulnerabilities page, you should avoid allowing strings containing data from any untrusted source to be parsed as JSON.

Find DOM-based vulnerabilities using Burp Suite

Try for free
