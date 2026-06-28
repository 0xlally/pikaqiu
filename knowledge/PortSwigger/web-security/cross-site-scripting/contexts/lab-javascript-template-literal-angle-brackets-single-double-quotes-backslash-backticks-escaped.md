# Lab: Reflected XSS into a template literal with angle brackets, single, double quotes, backslash and backticks Unicode-escaped

Source: https://portswigger.net/web-security/cross-site-scripting/contexts/lab-javascript-template-literal-angle-brackets-single-double-quotes-backslash-backticks-escaped
Fetched: 2026-06-28T09:17:44.490491+00:00

Web Security Academy

Cross-site scripting

Contexts

Lab

Lab: Reflected XSS into a template literal with angle brackets, single, double quotes, backslash and backticks Unicode-escaped

This lab contains a reflected cross-site scripting vulnerability in the search blog functionality. The reflection occurs inside a template string with angle brackets, single, and double quotes HTML encoded, and backticks escaped. To solve this lab, perform a cross-site scripting attack that calls the alert function inside the template string.

Solution

Submit a random alphanumeric string in the search box, then use Burp Suite to intercept the search request and send it to Burp Repeater.

Observe that the random string has been reflected inside a JavaScript template string.

Replace your input with the following payload to execute JavaScript inside the template string: ${alert(1)}

Verify the technique worked by right clicking, selecting "Copy URL", and pasting the URL in the browser. When you load the page it should trigger an alert.

Community solutions

z3nsh3ll

Michael Sommer

Find XSS vulnerabilities using Burp Suite

Try for free
