# Lab: DOM XSS in jQuery anchor href attribute sink using location.search source

Source: https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-jquery-href-attribute-sink
Fetched: 2026-06-28T09:17:45.384458+00:00

Web Security Academy

Cross-site scripting

DOM-based

Lab

Lab: DOM XSS in jQuery anchor href attribute sink using location.search source

This lab contains a DOM-based cross-site scripting vulnerability in the submit feedback page. It uses the jQuery library's $ selector function to find an anchor element, and changes its href attribute using data from location.search.

To solve this lab, make the "back" link alert document.cookie.

Solution

On the Submit feedback page, change the query parameter returnPath to / followed by a random alphanumeric string.

Right-click and inspect the element, and observe that your random string has been placed inside an a href attribute.

Change returnPath to:

javascript:alert(document.cookie)

Hit enter and click "back".

Community solutions

z3nsh3ll

Michael Sommer

Find XSS vulnerabilities using Burp Suite

Try for free
