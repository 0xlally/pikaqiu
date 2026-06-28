# Lab: Reflected XSS into a JavaScript string with angle brackets HTML encoded

Source: https://portswigger.net/web-security/cross-site-scripting/contexts/lab-javascript-string-angle-brackets-html-encoded
Fetched: 2026-06-28T09:17:44.461689+00:00

Web Security Academy

Cross-site scripting

Contexts

Lab

Lab: Reflected XSS into a JavaScript string with angle brackets HTML encoded

This lab contains a reflected cross-site scripting vulnerability in the search query tracking functionality where angle brackets are encoded. The reflection occurs inside a JavaScript string. To solve this lab, perform a cross-site scripting attack that breaks out of the JavaScript string and calls the alert function.

Solution

Submit a random alphanumeric string in the search box, then use Burp Suite to intercept the search request and send it to Burp Repeater.

Observe that the random string has been reflected inside a JavaScript string.

Replace your input with the following payload to break out of the JavaScript string and inject an alert:

'-alert(1)-'

Verify the technique worked by right clicking, selecting "Copy URL", and pasting the URL in the browser. When you load the page it should trigger an alert.

Community solutions

z3nsh3ll

Michael Sommer

Find XSS vulnerabilities using Burp Suite

Try for free
