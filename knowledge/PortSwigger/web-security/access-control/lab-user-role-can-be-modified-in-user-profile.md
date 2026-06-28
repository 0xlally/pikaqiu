# Lab: User role can be modified in user profile

Source: https://portswigger.net/web-security/access-control/lab-user-role-can-be-modified-in-user-profile
Fetched: 2026-06-28T09:17:39.172171+00:00

Web Security Academy

Access control

Lab

Lab: User role can be modified in user profile

This lab has an admin panel at /admin. It's only accessible to logged-in users with a roleid of 2.

Solve the lab by accessing the admin panel and using it to delete the user carlos.

You can log in to your own account using the following credentials: wiener:peter

Solution

Log in using the supplied credentials and access your account page.

Use the provided feature to update the email address associated with your account.

Observe that the response contains your role ID.

Send the email submission request to Burp Repeater, add "roleid":2 into the JSON in the request body, and resend it.

Observe that the response shows your roleid has changed to 2.

Browse to /admin and delete carlos.

Community solutions

Rana Khalil

Michael Sommer (no audio)

Find access control vulnerabilities using Burp Suite

Try for free
