# Lab: Reflected XSS into HTML context with nothing encoded

Source: https://portswigger.net/web-security/cross-site-scripting/reflected/lab-html-context-nothing-encoded
Fetched: 2026-06-28T09:17:45.914545+00:00

Web Security Academy

Cross-site scripting

Reflected

Lab

Lab: Reflected XSS into HTML context with nothing encoded

This lab contains a simple reflected cross-site scripting vulnerability in the search functionality.

To solve the lab, perform a cross-site scripting attack that calls the alert function.

Solution

Copy and paste the following into the search box:

<script>alert(1)</script>

Click "Search".

Community solutions

z3nsh3ll

Michael Sommer

Find XSS vulnerabilities using Burp Suite

Try for free
