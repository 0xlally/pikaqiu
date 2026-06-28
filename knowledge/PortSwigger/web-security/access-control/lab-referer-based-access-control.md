# Lab: Referer-based access control

Source: https://portswigger.net/web-security/access-control/lab-referer-based-access-control
Fetched: 2026-06-28T09:17:38.492671+00:00

Web Security Academy

Access control

Lab

Lab: Referer-based access control

This lab controls access to certain admin functionality based on the Referer header. You can familiarize yourself with the admin panel by logging in using the credentials administrator:admin.

To solve the lab, log in using the credentials wiener:peter and exploit the flawed access controls to promote yourself to become an administrator.

Solution

Log in using the admin credentials.

Browse to the admin panel, promote carlos, and send the HTTP request to Burp Repeater.

Open a private/incognito browser window, and log in with the non-admin credentials.

Browse to /admin-roles?username=carlos&action=upgrade and observe that the request is treated as unauthorized due to the absent Referer header.

Copy the non-admin user's session cookie into the existing Burp Repeater request, change the username to yours, and replay it.

Community solutions

Rana Khalil

Find access control vulnerabilities using Burp Suite

Try for free
