# Lab: User ID controlled by request parameter with data leakage in redirect

Source: https://portswigger.net/web-security/access-control/lab-user-id-controlled-by-request-parameter-with-data-leakage-in-redirect
Fetched: 2026-06-28T09:17:38.978253+00:00

Web Security Academy

Access control

Lab

Lab: User ID controlled by request parameter with data leakage in redirect

This lab contains an access control vulnerability where sensitive information is leaked in the body of a redirect response.

To solve the lab, obtain the API key for the user carlos and submit it as the solution.

You can log in to your own account using the following credentials: wiener:peter

Solution

Log in using the supplied credentials and access your account page.

Send the request to Burp Repeater.

Change the "id" parameter to carlos.

Observe that although the response is now redirecting you to the home page, it has a body containing the API key belonging to carlos.

Submit the API key.

Community solutions

Rana Khalil

Michael Sommer (no audio)

Find access control vulnerabilities using Burp Suite

Try for free
