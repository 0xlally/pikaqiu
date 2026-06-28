# Lab: Stored XSS into anchor href attribute with double quotes HTML-encoded

Source: https://portswigger.net/web-security/cross-site-scripting/contexts/lab-href-attribute-double-quotes-html-encoded
Fetched: 2026-06-28T09:17:44.217971+00:00

Web Security Academy

Cross-site scripting

Contexts

Lab

Lab: Stored XSS into anchor href attribute with double quotes HTML-encoded

This lab contains a stored cross-site scripting vulnerability in the comment functionality. To solve this lab, submit a comment that calls the alert function when the comment author name is clicked.

Solution

Post a comment with a random alphanumeric string in the "Website" input, then use Burp Suite to intercept the request and send it to Burp Repeater.

Make a second request in the browser to view the post and use Burp Suite to intercept the request and send it to Burp Repeater.

Observe that the random string in the second Repeater tab has been reflected inside an anchor href attribute.

Repeat the process again but this time replace your input with the following payload to inject a JavaScript URL that calls alert:

javascript:alert(1)

Verify the technique worked by right-clicking, selecting "Copy URL", and pasting the URL in the browser. Clicking the name above your comment should trigger an alert.

Community solutions

z3nsh3ll

Michael Sommer

Find XSS vulnerabilities using Burp Suite

Try for free
