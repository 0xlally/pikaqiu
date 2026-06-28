# Lab: File path traversal, traversal sequences stripped non-recursively

Source: https://portswigger.net/web-security/file-path-traversal/lab-sequences-stripped-non-recursively
Fetched: 2026-06-28T09:17:49.781640+00:00

Web Security Academy

Path traversal

Lab

Lab: File path traversal, traversal sequences stripped non-recursively

This lab contains a path traversal vulnerability in the display of product images.

The application strips path traversal sequences from the user-supplied filename before using it.

To solve the lab, retrieve the contents of the /etc/passwd file.

Solution

Use Burp Suite to intercept and modify a request that fetches a product image.

Modify the filename parameter, giving it the value:

....//....//....//etc/passwd

Observe that the response contains the contents of the /etc/passwd file.

Community solutions

Rana Khalil

Intigriti

z3nsh3ll

Michael Sommer

Find path traversal vulnerabilities using Burp Suite

Try for free
