# Lab: Stored XSS into onclick event with angle brackets and double quotes HTML-encoded and single quotes and backslash escaped

Source: https://portswigger.net/web-security/cross-site-scripting/contexts/lab-onclick-event-angle-brackets-double-quotes-html-encoded-single-quotes-backslash-escaped
Fetched: 2026-06-28T09:17:44.722678+00:00

Web Security Academy

Cross-site scripting

Contexts

Lab

Lab: Stored XSS into onclick event with angle brackets and double quotes HTML-encoded and single quotes and backslash escaped

This lab contains a stored cross-site scripting vulnerability in the comment functionality.

To solve this lab, submit a comment that calls the alert function when the comment author name is clicked.

Solution

Post a comment with a random alphanumeric string in the "Website" input, then use Burp Suite to intercept the request and send it to Burp Repeater.

Make a second request in the browser to view the post and use Burp Suite to intercept the request and send it to Burp Repeater.

Observe that the random string in the second Repeater tab has been reflected inside an onclick event handler attribute.

Repeat the process again but this time modify your input to inject a JavaScript URL that calls alert, using the following payload:

http://foo?&apos;-alert(1)-&apos;

Verify the technique worked by right-clicking, selecting "Copy URL", and pasting the URL in the browser. Clicking the name above your comment should trigger an alert.

Community solutions

z3nsh3ll

Michael Sommer

Find XSS vulnerabilities using Burp Suite

Try for free
