# DOM-based denial of service

Source: https://portswigger.net/web-security/dom-based/denial-of-service
Fetched: 2026-06-28T09:17:48.374604+00:00

Web Security Academy

DOM-based

Denial of service

DOM-based denial of service

In this section, we'll describe DOM-based denial-of-service vulnerabilities, look at which sinks can lead to this kind of vulnerability, and discuss ways to reduce your exposure to DOM-based DOS attacks.

What is DOM-based denial of service?

DOM-based denial-of-service vulnerabilities arise when a script passes attacker-controllable data in an unsafe way to a problematic platform API, such as an API whose invocation can cause the user's computer to consume excessive amounts of CPU or disk space. This may result in side effects if the browser restricts the functionality of the website, for example, by rejecting attempts to store data in localStorage or killing busy scripts.

Which sinks can lead to DOM-based denial-of-service vulnerabilities?

The following are some of the main sinks can lead to DOM-based denial-of-service vulnerabilities:

requestFileSystem()

RegExp()

How to prevent DOM-based denial-of-service vulnerabilities

In addition to the general measures described on the DOM-based vulnerabilities page, you should avoid allowing data from any untrusted source to dynamically pass data into problematic platform APIs.

Find DOM-based vulnerabilities using Burp Suite

Try for free
