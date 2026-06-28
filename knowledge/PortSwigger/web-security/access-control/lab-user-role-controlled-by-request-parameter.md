# Lab: User role controlled by request parameter

Source: https://portswigger.net/web-security/access-control/lab-user-role-controlled-by-request-parameter
Fetched: 2026-06-28T09:17:39.075486+00:00

Web Security Academy

Access control

Lab

Lab: User role controlled by request parameter

This lab has an admin panel at /admin, which identifies administrators using a forgeable cookie.

Solve the lab by accessing the admin panel and using it to delete the user carlos.

You can log in to your own account using the following credentials: wiener:peter

Solution

Browse to /admin and observe that you can't access the admin panel.

Browse to the login page.

In Burp Proxy, turn interception on and enable response interception.

Complete and submit the login page, and forward the resulting request in Burp.

Observe that the response sets the cookie Admin=false. Change it to Admin=true.

Load the admin panel and delete carlos.

Community solutions

Rana Khalil

Find access control vulnerabilities using Burp Suite

Try for free
