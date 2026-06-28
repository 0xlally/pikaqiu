# Lab: JWT authentication bypass via algorithm confusion

Source: https://portswigger.net/web-security/jwt/algorithm-confusion/lab-jwt-authentication-bypass-via-algorithm-confusion
Fetched: 2026-06-28T09:17:53.007973+00:00

Web Security Academy

JWT attacks

Algorithm confusion attacks

Lab

Lab: JWT authentication bypass via algorithm confusion

This lab uses a JWT-based mechanism for handling sessions. It uses a robust RSA key pair to sign and verify tokens. However, due to implementation flaws, this mechanism is vulnerable to algorithm confusion attacks.

To solve the lab, first obtain the server's public key. This is exposed via a standard endpoint. Use this key to sign a modified session token that gives you access to the admin panel at /admin, then delete the user carlos.

You can log in to your own account using the following credentials: wiener:peter

Tip

We recommend familiarizing yourself with how to work with JWTs in Burp Suite before attempting this lab.

Hint

You can assume that the server stores its public key as an X.509 PEM file.

Solution

Part 1 - Obtain the server's public key

In Burp, load the JWT Editor extension from the BApp store.

In the lab, log in to your own account and send the post-login GET /my-account request to Burp Repeater.

In Burp Repeater, change the path to /admin and send the request. Observe that the admin panel is only accessible when logged in as the administrator user.

In the browser, go to the standard endpoint /jwks.json and observe that the server exposes a JWK Set containing a single public key.

Copy the JWK object from inside the keys array. Make sure that you don't accidentally copy any characters from the surrounding array.

Part 2 - Generate a malicious signing key

In Burp, go to the JWT Editor Keys tab in Burp's main tab bar.

Click New RSA Key.

In the dialog, make sure that the JWK option is selected, then paste the JWK that you just copied. Click OK to save the key.

Right-click on the entry for the key that you just created, then select Copy Public Key as PEM.

Use the Decoder tab to Base64 encode this PEM key, then copy the resulting string.

Go back to the JWT Editor Keys tab in Burp's main tab bar.

Click New Symmetric Key. In the dialog, click Generate to generate a new key in JWK format. Note that you don't need to select a key size as this will automatically be updated later.

Replace the generated value for the k property with a Base64-encoded PEM that you just created.

Save the key.

Part 3 - Modify and sign the token

Go back to the GET /admin request in Burp Repeater and switch to the extension-generated JSON Web Token tab.

In the header of the JWT, change the value of the alg parameter to HS256.

In the payload, change the value of the sub claim to administrator.

At the bottom of the tab, click Sign, then select the symmetric key that you generated in the previous section.

Make sure that the Don't modify header option is selected, then click OK. The modified token is now signed using the server's public key as the secret key.

Send the request and observe that you have successfully accessed the admin panel.

In the response, find the URL for deleting carlos (/admin/delete?username=carlos). Send the request to this endpoint to solve the lab.

Community solutions

Intigriti

Emanuele Picariello

Michael Sommer

Find JWT vulnerabilities using Burp Suite

Try for free
