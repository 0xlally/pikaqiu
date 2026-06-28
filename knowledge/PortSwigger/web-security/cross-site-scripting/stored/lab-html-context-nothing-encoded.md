# Lab: Stored XSS into HTML context with nothing encoded

Source: https://portswigger.net/web-security/cross-site-scripting/stored/lab-html-context-nothing-encoded
Fetched: 2026-06-28T09:17:45.923108+00:00

Web Security Academy

Cross-site scripting

Stored

Lab

Lab: Stored XSS into HTML context with nothing encoded

This lab contains a stored cross-site scripting vulnerability in the comment functionality.

To solve this lab, submit a comment that calls the alert function when the blog post is viewed.

Solution

Enter the following into the comment box:

<script>alert(1)</script>

Enter a name, email and website.

Click "Post comment".

Go back to the blog.

Community solutions

z3nsh3ll

Michael Sommer

Find XSS vulnerabilities using Burp Suite

Try for free
