# Lab: Reflected XSS in canonical link tag

Source: https://portswigger.net/web-security/cross-site-scripting/contexts/lab-canonical-link-tag
Fetched: 2026-06-28T09:17:43.965407+00:00

Web Security Academy

Cross-site scripting

Contexts

Lab

Lab: Reflected XSS in canonical link tag

This lab reflects user input in a canonical link tag and escapes angle brackets.

To solve the lab, perform a cross-site scripting attack on the home page that injects an attribute that calls the alert function.

To assist with your exploit, you can assume that the simulated user will press the following key combinations:

ALT+SHIFT+X

CTRL+ALT+X

Alt+X

Please note that the intended solution to this lab is only possible in Chrome.

Solution

Visit the following URL, replacing YOUR-LAB-ID with your lab ID:

https://YOUR-LAB-ID.web-security-academy.net/?%27accesskey=%27x%27onclick=%27alert(1)

This sets the X key as an access key for the whole page. When a user presses the access key, the alert function is called.

To trigger the exploit on yourself, press one of the following key combinations:

On Windows: ALT+SHIFT+X

On MacOS: CTRL+ALT+X

On Linux: Alt+X

Community solutions

z3nsh3ll

Michael Sommer

Find XSS vulnerabilities using Burp Suite

Try for free
