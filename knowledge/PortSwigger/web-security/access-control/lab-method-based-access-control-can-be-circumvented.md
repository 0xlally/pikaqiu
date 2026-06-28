# Lab: Method-based access control can be circumvented

Source: https://portswigger.net/web-security/access-control/lab-method-based-access-control-can-be-circumvented
Fetched: 2026-06-28T09:17:38.268449+00:00

Web Security Academy

Access control

Lab

Lab: Method-based access control can be circumvented

This lab implements access controls based partly on the HTTP method of requests. You can familiarize yourself with the admin panel by logging in using the credentials administrator:admin.

To solve the lab, log in using the credentials wiener:peter and exploit the flawed access controls to promote yourself to become an administrator.

Solution

Log in using the admin credentials.

Browse to the admin panel, promote carlos, and send the HTTP request to Burp Repeater.

Open a private/incognito browser window, and log in with the non-admin credentials.

Attempt to re-promote carlos with the non-admin user by copying that user's session cookie into the existing Burp Repeater request, and observe that the response says "Unauthorized".

Change the method from POST to POSTX and observe that the response changes to "missing parameter".

Convert the request to use the GET method by right-clicking and selecting "Change request method".

Change the username parameter to your username and resend the request.

Community solutions

Rana Khalil

Michael Sommer (no audio)

Find access control vulnerabilities using Burp Suite

Try for free
