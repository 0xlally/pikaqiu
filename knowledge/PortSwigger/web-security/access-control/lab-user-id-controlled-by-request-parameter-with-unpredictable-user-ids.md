# Lab: User ID controlled by request parameter, with unpredictable user IDs

Source: https://portswigger.net/web-security/access-control/lab-user-id-controlled-by-request-parameter-with-unpredictable-user-ids
Fetched: 2026-06-28T09:17:38.775345+00:00

Web Security Academy

Access control

Lab

Lab: User ID controlled by request parameter, with unpredictable user IDs

This lab has a horizontal privilege escalation vulnerability on the user account page, but identifies users with GUIDs.

To solve the lab, find the GUID for carlos, then submit his API key as the solution.

You can log in to your own account using the following credentials: wiener:peter

Solution

Find a blog post by carlos.

Click on carlos and observe that the URL contains his user ID. Make a note of this ID.

Log in using the supplied credentials and access your account page.

Change the "id" parameter to the saved user ID.

Retrieve and submit the API key.

Community solutions

Rana Khalil

Michael Sommer (no audio)

Find access control vulnerabilities using Burp Suite

Try for free
