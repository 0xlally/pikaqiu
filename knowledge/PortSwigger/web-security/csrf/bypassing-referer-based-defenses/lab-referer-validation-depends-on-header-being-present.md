# Lab: CSRF where Referer validation depends on header being present

Source: https://portswigger.net/web-security/csrf/bypassing-referer-based-defenses/lab-referer-validation-depends-on-header-being-present
Fetched: 2026-06-28T09:17:46.124537+00:00

Web Security Academy

CSRF

Bypassing Referer-based CSRF defenses

Lab

Lab: CSRF where Referer validation depends on header being present

This lab's email change functionality is vulnerable to CSRF. It attempts to block cross domain requests but has an insecure fallback.

To solve the lab, use your exploit server to host an HTML page that uses a CSRF attack to change the viewer's email address.

You can log in to your own account using the following credentials: wiener:peter

Hint

You cannot register an email address that is already taken by another user. If you change your own email address while testing your exploit, make sure you use a different email address for the final exploit you deliver to the victim.

Solution

Open Burp's browser and log in to your account. Submit the "Update email" form, and find the resulting request in your Proxy history.

Send the request to Burp Repeater and observe that if you change the domain in the Referer HTTP header then the request is rejected.

Delete the Referer header entirely and observe that the request is now accepted.

Create and host a proof of concept exploit as described in the solution to the CSRF vulnerability with no defenses lab. Include the following HTML to suppress the Referer header:

<meta name="referrer" content="no-referrer">

Change the email address in your exploit so that it doesn't match your own.

Store the exploit, then click "Deliver to victim" to solve the lab.

Community solutions

Rana Khalil

Michael Sommer

Find CSRF vulnerabilities using Burp Suite

Try for free
