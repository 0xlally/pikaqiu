# Lab: Unprotected admin functionality

Source: https://portswigger.net/web-security/access-control/lab-unprotected-admin-functionality
Fetched: 2026-06-28T09:17:38.320652+00:00

Web Security Academy

Access control

Lab

Lab: Unprotected admin functionality

This lab has an unprotected admin panel.

Solve the lab by deleting the user carlos.

Solution

Go to the lab and view robots.txt by appending /robots.txt to the lab URL. Notice that the Disallow line discloses the path to the admin panel.

In the URL bar, replace /robots.txt with /administrator-panel to load the admin panel.

Delete carlos.

Community solutions

Rana Khalil

Popo Hack

Find access control vulnerabilities using Burp Suite

Try for free
