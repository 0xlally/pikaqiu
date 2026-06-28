# Lab: JWT authentication bypass via jku header injection

Source: https://portswigger.net/web-security/jwt/lab-jwt-authentication-bypass-via-jku-header-injection
Fetched: 2026-06-28T09:17:53.118611+00:00

Web Security Academy

JWT attacks

Lab

Lab: JWT authentication bypass via jku header injection

This lab uses a JWT-based mechanism for handling sessions. The server supports the jku parameter in the JWT header. However, it fails to check whether the provided URL belongs to a trusted domain before fetching the key.

To solve the lab, forge a JWT that gives you access to the admin panel at /admin, then delete the user carlos.

You can log in to your own account using the following credentials: wiener:peter

Tip

We recommend familiarizing yourself with how to work with JWTs in Burp Suite before attempting this lab.

Solution

Part 1 - Upload a malicious JWK Set

In Burp, load the JWT Editor extension from the BApp store.

In the lab, log in to your own account and send the post-login GET /my-account request to Burp Repeater.

In Burp Repeater, change the path to /admin and send the request. Observe that the admin panel is only accessible when logged in as the administrator user.

Go to the JWT Editor Keys tab in Burp's main tab bar.

Click New RSA Key.

In the dialog, click Generate to automatically generate a new key pair, then click OK to save the key. Note that you don't need to select a key size as this will automatically be updated later.

In the browser, go to the exploit server.

Replace the contents of the Body section with an empty JWK Set as follows:

{

"keys": [

]

}

Back on the JWT Editor Keys tab, right-click on the entry for the key that you just generated, then select Copy Public Key as JWK.

Paste the JWK into the keys array on the exploit server, then store the exploit. The result should look something like this:

{

"keys": [

{

"kty": "RSA",

"e": "AQAB",

"kid": "893d8f0b-061f-42c2-a4aa-5056e12b8ae7",

"n": "yy1wpYmffgXBxhAUJzHHocCuJolwDqql75ZWuCQ_cb33K2vh9mk6GPM9gNN4Y_qTVX67WhsN3JvaFYw"

}

]

}

Part 2 - Modify and sign the JWT

Go back to the GET /admin request in Burp Repeater and switch to the extension-generated JSON Web Token message editor tab.

In the header of the JWT, replace the current value of the kid parameter with the kid of the JWK that you uploaded to the exploit server.

Add a new jku parameter to the header of the JWT. Set its value to the URL of your JWK Set on the exploit server.

In the payload, change the value of the sub claim to administrator.

At the bottom of the tab, click Sign, then select the RSA key that you generated in the previous section.

Make sure that the Don't modify header option is selected, then click OK. The modified token is now signed with the correct signature.

Send the request. Observe that you have successfully accessed the admin panel.

In the response, find the URL for deleting carlos (/admin/delete?username=carlos). Send the request to this endpoint to solve the lab.

Community solutions

Intigriti

Emanuele Picariello

Michael Sommer

nu11 secur1ty

Find JWT vulnerabilities using Burp Suite

Try for free
