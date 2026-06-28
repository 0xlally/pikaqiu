# Lab: JWT authentication bypass via kid header path traversal

Source: https://portswigger.net/web-security/jwt/lab-jwt-authentication-bypass-via-kid-header-path-traversal
Fetched: 2026-06-28T09:17:53.127038+00:00

Web Security Academy

JWT attacks

Lab

Lab: JWT authentication bypass via kid header path traversal

This lab uses a JWT-based mechanism for handling sessions. In order to verify the signature, the server uses the kid parameter in JWT header to fetch the relevant key from its filesystem.

To solve the lab, forge a JWT that gives you access to the admin panel at /admin, then delete the user carlos.

You can log in to your own account using the following credentials: wiener:peter

Tip

We recommend familiarizing yourself with how to work with JWTs in Burp Suite before attempting this lab.

Solution

Note

In this solution, we'll point the kid parameter to the standard file /dev/null. In practice, you can point the kid parameter to any file with predictable contents.

Generate a suitable signing key

In Burp, load the JWT Editor extension from the BApp store.

In the lab, log in to your own account and send the post-login GET /my-account request to Burp Repeater.

In Burp Repeater, change the path to /admin and send the request. Observe that the admin panel is only accessible when logged in as the administrator user.

Go to the JWT Editor Keys tab in Burp's main tab bar.

Click New Symmetric Key.

In the dialog, click Generate to generate a new key in JWK format. Note that you don't need to select a key size as this will automatically be updated later.

Replace the generated value for the k property with an empty string.

Click OK to save the key.

Modify and sign the JWT

Go back to the GET /admin request in Burp Repeater and switch to the extension-generated JSON Web Token message editor tab.

In the header of the JWT, change the value of the kid parameter to a path traversal sequence pointing to the /dev/null file:

../../../../../../../dev/null

In the JWT payload, change the value of the sub claim to administrator.

At the bottom of the tab, click Sign, then select the symmetric key that you generated in the previous section.

Make sure that the Don't modify header option is selected, then click OK. The modified token is now signed using a null byte as the secret key.

Send the request and observe that you have successfully accessed the admin panel.

In the response, find the URL for deleting carlos (/admin/delete?username=carlos). Send the request to this endpoint to solve the lab.

Community solutions

Emanuele Picariello

Michael Sommer

Intigriti

Find JWT vulnerabilities using Burp Suite

Try for free
