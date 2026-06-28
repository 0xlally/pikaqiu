# Lab: DOM XSS in document.write sink using source location.search

Source: https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-document-write-sink
Fetched: 2026-06-28T09:17:45.090450+00:00

Web Security Academy

Cross-site scripting

DOM-based

Lab

Lab: DOM XSS in document.write sink using source location.search

This lab contains a DOM-based cross-site scripting vulnerability in the search query tracking functionality. It uses the JavaScript document.write function, which writes data out to the page. The document.write function is called with data from location.search, which you can control using the website URL.

To solve this lab, perform a cross-site scripting attack that calls the alert function.

Solution

Enter a random alphanumeric string into the search box.

Right-click and inspect the element, and observe that your random string has been placed inside an img src attribute.

Break out of the img attribute by searching for:

"><svg onload=alert(1)>

Community solutions

z3nsh3ll

Michael Sommer

Find XSS vulnerabilities using Burp Suite

Try for free
