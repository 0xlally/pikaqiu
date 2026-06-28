# Lab: Reflected XSS into a JavaScript string with single quote and backslash escaped

Source: https://portswigger.net/web-security/cross-site-scripting/contexts/lab-javascript-string-single-quote-backslash-escaped
Fetched: 2026-06-28T09:17:44.382519+00:00

Web Security Academy

Cross-site scripting

Contexts

Lab

Lab: Reflected XSS into a JavaScript string with single quote and backslash escaped

This lab contains a reflected cross-site scripting vulnerability in the search query tracking functionality. The reflection occurs inside a JavaScript string with single quotes and backslashes escaped.

To solve this lab, perform a cross-site scripting attack that breaks out of the JavaScript string and calls the alert function.

Solution

Submit a random alphanumeric string in the search box, then use Burp Suite to intercept the search request and send it to Burp Repeater.

Observe that the random string has been reflected inside a JavaScript string.

Try sending the payload test'payload and observe that your single quote gets backslash-escaped, preventing you from breaking out of the string.

Replace your input with the following payload to break out of the script block and inject a new script:

</script><script>alert(1)</script>

Verify the technique worked by right clicking, selecting "Copy URL", and pasting the URL in the browser. When you load the page it should trigger an alert.

Community solutions

z3nsh3ll

Michael Sommer

Find XSS vulnerabilities using Burp Suite

Try for free
