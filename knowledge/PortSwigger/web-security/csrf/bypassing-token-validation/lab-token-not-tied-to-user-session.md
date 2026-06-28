# Lab: CSRF where token is not tied to user session

Source: https://portswigger.net/web-security/csrf/bypassing-token-validation/lab-token-not-tied-to-user-session
Fetched: 2026-06-28T09:17:46.929584+00:00

Web Security Academy

CSRF

Bypassing CSRF token validation

Lab

Lab: CSRF where token is not tied to user session

This lab's email change functionality is vulnerable to CSRF. It uses tokens to try to prevent CSRF attacks, but they aren't integrated into the site's session handling system.

To solve the lab, use your exploit server to host an HTML page that uses a CSRF attack to change the viewer's email address.

You have two accounts on the application that you can use to help design your attack. The credentials are as follows:

wiener:peter

carlos:montoya

Hint

You cannot register an email address that is already taken by another user. If you change your own email address while testing your exploit, make sure you use a different email address for the final exploit you deliver to the victim.

Solution

Open Burp's browser and log in to your account. Submit the "Update email" form, and intercept the resulting request.

Make a note of the value of the CSRF token, then drop the request.

Open a private/incognito browser window, log in to your other account, and send the update email request into Burp Repeater.

Observe that if you swap the CSRF token with the value from the other account, then the request is accepted.

Create and host a proof of concept exploit as described in the solution to the CSRF vulnerability with no defenses lab. Note that the CSRF tokens are single-use, so you'll need to include a fresh one.

Change the email address in your exploit so that it doesn't match your own.

Store the exploit, then click "Deliver to victim" to solve the lab.

Community solutions

Intigriti

Rana Khalil

Michael Sommer

Find CSRF vulnerabilities using Burp Suite

Try for free
