# Lab: DOM XSS in innerHTML sink using source location.search

Source: https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-innerhtml-sink
Fetched: 2026-06-28T09:17:45.323688+00:00

Web Security Academy

Cross-site scripting

DOM-based

Lab

Lab: DOM XSS in innerHTML sink using source location.search

This lab contains a DOM-based cross-site scripting vulnerability in the search blog functionality. It uses an innerHTML assignment, which changes the HTML contents of a div element, using data from location.search.

To solve this lab, perform a cross-site scripting attack that calls the alert function.

Solution

Enter the following into the into the search box:

<img src=1 onerror=alert(1)>

Click "Search".

The value of the src attribute is invalid and throws an error. This triggers the onerror event handler, which then calls the alert() function. As a result, the payload is executed whenever the user's browser attempts to load the page containing your malicious post.

Community solutions

z3nsh3ll

Michael Sommer

Find XSS vulnerabilities using Burp Suite

Try for free
