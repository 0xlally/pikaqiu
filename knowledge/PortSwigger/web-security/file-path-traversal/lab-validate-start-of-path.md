# Lab: File path traversal, validation of start of path

Source: https://portswigger.net/web-security/file-path-traversal/lab-validate-start-of-path
Fetched: 2026-06-28T09:17:49.990153+00:00

Web Security Academy

Path traversal

Lab

Lab: File path traversal, validation of start of path

This lab contains a path traversal vulnerability in the display of product images.

The application transmits the full file path via a request parameter, and validates that the supplied path starts with the expected folder.

To solve the lab, retrieve the contents of the /etc/passwd file.

Solution

Use Burp Suite to intercept and modify a request that fetches a product image.

Modify the filename parameter, giving it the value:

/var/www/images/../../../etc/passwd

Observe that the response contains the contents of the /etc/passwd file.

Community solutions

Rana Khalil

z3nsh3ll

Intigriti

Michael Sommer

Find path traversal vulnerabilities using Burp Suite

Try for free
