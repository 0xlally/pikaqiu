# Lab: File path traversal, validation of file extension with null byte bypass

Source: https://portswigger.net/web-security/file-path-traversal/lab-validate-file-extension-null-byte-bypass
Fetched: 2026-06-28T09:17:49.650014+00:00

Web Security Academy

Path traversal

Lab

Lab: File path traversal, validation of file extension with null byte bypass

This lab contains a path traversal vulnerability in the display of product images.

The application validates that the supplied filename ends with the expected file extension.

To solve the lab, retrieve the contents of the /etc/passwd file.

Solution

Use Burp Suite to intercept and modify a request that fetches a product image.

Modify the filename parameter, giving it the value:

../../../etc/passwd%00.png

Observe that the response contains the contents of the /etc/passwd file.

Community solutions

Rana Khalil

z3nsh3ll

Intigriti

Michael Sommer

Find path traversal vulnerabilities using Burp Suite

Try for free
