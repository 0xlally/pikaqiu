# Lab: Multi-step process with no access control on one step

Source: https://portswigger.net/web-security/access-control/lab-multi-step-process-with-no-access-control-on-one-step
Fetched: 2026-06-28T09:17:38.337817+00:00

Web Security Academy

Access control

Lab

Lab: Multi-step process with no access control on one step

This lab has an admin panel with a flawed multi-step process for changing a user's role. You can familiarize yourself with the admin panel by logging in using the credentials administrator:admin.

To solve the lab, log in using the credentials wiener:peter and exploit the flawed access controls to promote yourself to become an administrator.

Solution

Log in using the admin credentials.

Browse to the admin panel, promote carlos, and send the confirmation HTTP request to Burp Repeater.

Open a private/incognito browser window, and log in with the non-admin credentials.

Copy the non-admin user's session cookie into the existing Repeater request, change the username to yours, and replay it.

Community solutions

Rana Khalil

Michael Sommer (no audio)

Find access control vulnerabilities using Burp Suite

Try for free
