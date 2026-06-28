# Lab: 2FA simple bypass

Source: https://portswigger.net/web-security/authentication/multi-factor/lab-2fa-simple-bypass
Fetched: 2026-06-28T09:17:40.604869+00:00

Web Security Academy

Authentication vulnerabilities

Multi-factor

Lab

Lab: 2FA simple bypass

This lab's two-factor authentication can be bypassed. You have already obtained a valid username and password, but do not have access to the user's 2FA verification code. To solve the lab, access Carlos's account page.

Your credentials: wiener:peter

Victim's credentials carlos:montoya

Solution

Log in to your own account. Your 2FA verification code will be sent to you by email. Click the Email client button to access your emails.

Go to your account page and make a note of the URL.

Log out of your account.

Log in using the victim's credentials.

When prompted for the verification code, manually change the URL to navigate to /my-account. The lab is solved when the page loads.

Community solutions

Rana Khalil

Michael Sommer

Find vulnerabilities in your authentication using Burp Suite

Try for free
