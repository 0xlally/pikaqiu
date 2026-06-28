# Lab: Unprotected admin functionality with unpredictable URL

Source: https://portswigger.net/web-security/access-control/lab-unprotected-admin-functionality-with-unpredictable-url
Fetched: 2026-06-28T09:17:38.616416+00:00

Web Security Academy

Access control

Lab

Lab: Unprotected admin functionality with unpredictable URL

This lab has an unprotected admin panel. It's located at an unpredictable location, but the location is disclosed somewhere in the application.

Solve the lab by accessing the admin panel, and using it to delete the user carlos.

Solution

Review the lab home page's source using Burp Suite or your web browser's developer tools.

Observe that it contains some JavaScript that discloses the URL of the admin panel.

Load the admin panel and delete carlos.

Community solutions

Rana Khalil

Michael Sommer (no audio)

Find access control vulnerabilities using Burp Suite

Try for free
