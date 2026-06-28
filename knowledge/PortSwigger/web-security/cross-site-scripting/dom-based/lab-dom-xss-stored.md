# Lab: Stored DOM XSS

Source: https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-dom-xss-stored
Fetched: 2026-06-28T09:17:44.984961+00:00

Web Security Academy

Cross-site scripting

DOM-based

Lab

Lab: Stored DOM XSS

This lab demonstrates a stored DOM vulnerability in the blog comment functionality. To solve this lab, exploit this vulnerability to call the alert() function.

Solution

Post a comment containing the following vector:

<><img src=1 onerror=alert(1)>

In an attempt to prevent XSS, the website uses the JavaScript replace() function to encode angle brackets. However, when the first argument is a string, the function only replaces the first occurrence. We exploit this vulnerability by simply including an extra set of angle brackets at the beginning of the comment. These angle brackets will be encoded, but any subsequent angle brackets will be unaffected, enabling us to effectively bypass the filter and inject HTML.

Community solutions

z3nsh3ll

Michael Sommer

Find XSS vulnerabilities using Burp Suite

Try for free
