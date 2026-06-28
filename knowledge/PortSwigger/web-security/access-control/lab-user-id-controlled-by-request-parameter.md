# Lab: User ID controlled by request parameter

Source: https://portswigger.net/web-security/access-control/lab-user-id-controlled-by-request-parameter
Fetched: 2026-06-28T09:17:38.721094+00:00

Web Security Academy

Access control

Lab

Lab: User ID controlled by request parameter

This lab has a horizontal privilege escalation vulnerability on the user account page.

To solve the lab, obtain the API key for the user carlos and submit it as the solution.

You can log in to your own account using the following credentials: wiener:peter

Solution

Log in using the supplied credentials and go to your account page.

Note that the URL contains your username in the "id" parameter.

Send the request to Burp Repeater.

Change the "id" parameter to carlos.

Retrieve and submit the API key for carlos.

Community solutions

Rana Khalil

Michael Sommer (no audio)

Find access control vulnerabilities using Burp Suite

Try for free
