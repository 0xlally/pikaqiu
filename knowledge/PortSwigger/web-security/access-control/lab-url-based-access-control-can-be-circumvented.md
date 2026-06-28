# Lab: URL-based access control can be circumvented

Source: https://portswigger.net/web-security/access-control/lab-url-based-access-control-can-be-circumvented
Fetched: 2026-06-28T09:17:38.690106+00:00

Web Security Academy

Access control

Lab

Lab: URL-based access control can be circumvented

This website has an unauthenticated admin panel at /admin, but a front-end system has been configured to block external access to that path. However, the back-end application is built on a framework that supports the X-Original-URL header.

To solve the lab, access the admin panel and delete the user carlos.

Solution

Try to load /admin and observe that you get blocked. Notice that the response is very plain, suggesting it may originate from a front-end system.

Send the request to Burp Repeater. Change the URL in the request line to / and add the HTTP header X-Original-URL: /invalid. Observe that the application returns a "not found" response. This indicates that the back-end system is processing the URL from the X-Original-URL header.

Change the value of the X-Original-URL header to /admin. Observe that you can now access the admin page.

To delete carlos, add ?username=carlos to the real query string, and change the X-Original-URL path to /admin/delete.

Community solutions

Rana Khalil

Michael Sommer (no audio)

Find access control vulnerabilities using Burp Suite

Try for free
