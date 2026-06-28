# Lab: 2FA broken logic

Source: https://portswigger.net/web-security/authentication/multi-factor/lab-2fa-broken-logic
Fetched: 2026-06-28T09:17:40.974637+00:00

Web Security Academy

Authentication vulnerabilities

Multi-factor

Lab

Lab: 2FA broken logic

This lab's two-factor authentication is vulnerable due to its flawed logic. To solve the lab, access Carlos's account page.

Your credentials: wiener:peter

Victim's username: carlos

You also have access to the email server to receive your 2FA verification code.

Hint

Carlos will not attempt to log in to the website himself.

Solution

With Burp running, log in to your own account and investigate the 2FA verification process. Notice that in the POST /login2 request, the verify parameter is used to determine which user's account is being accessed.

Log out of your account.

Send the GET /login2 request to Burp Repeater. Change the value of the verify parameter to carlos and send the request. This ensures that a temporary 2FA code is generated for Carlos.

Go to the login page and enter your username and password. Then, submit an invalid 2FA code.

Send the POST /login2 request to Burp Intruder.

In Burp Intruder, set the verify parameter to carlos and add a payload position to the mfa-code parameter. Brute-force the verification code.

Load the 302 response in the browser.

Click My account to solve the lab.

Community solutions

Rana Khalil

Michael Sommer

Find vulnerabilities in your authentication using Burp Suite

Try for free
