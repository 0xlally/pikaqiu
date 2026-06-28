# Lab: JWT authentication bypass via flawed signature verification

Source: https://portswigger.net/web-security/jwt/lab-jwt-authentication-bypass-via-flawed-signature-verification
Fetched: 2026-06-28T09:17:53.266509+00:00

Web Security Academy

JWT attacks

Lab

Lab: JWT authentication bypass via flawed signature verification

This lab uses a JWT-based mechanism for handling sessions. The server is insecurely configured to accept unsigned JWTs.

To solve the lab, modify your session token to gain access to the admin panel at /admin, then delete the user carlos.

You can log in to your own account using the following credentials: wiener:peter

Tip

We recommend familiarizing yourself with how to work with JWTs in Burp Suite before attempting this lab.

Solution

In the lab, log in to your own account.

In Burp, go to the Proxy > HTTP history tab and look at the post-login GET /my-account request. Observe that your session cookie is a JWT.

Double-click the payload part of the token to view its decoded JSON form in the Inspector panel. Notice that the sub claim contains your username. Send this request to Burp Repeater.

In Burp Repeater, change the path to /admin and send the request. Observe that the admin panel is only accessible when logged in as the administrator user.

Select the payload of the JWT again. In the Inspector panel, change the value of the sub claim to administrator, then click Apply changes.

Select the header of the JWT, then use the Inspector to change the value of the alg parameter to none. Click Apply changes.

In the message editor, remove the signature from the JWT, but remember to leave the trailing dot after the payload.

Send the request and observe that you have successfully accessed the admin panel.

In the response, find the URL for deleting carlos (/admin/delete?username=carlos). Send the request to this endpoint to solve the lab.

Community solutions

Intigriti

Emanuele Picariello

Michael Sommer

nu11 secur1ty

Find JWT vulnerabilities using Burp Suite

Try for free
