# Lab: CSRF where token is duplicated in cookie

Source: https://portswigger.net/web-security/csrf/bypassing-token-validation/lab-token-duplicated-in-cookie
Fetched: 2026-06-28T09:17:46.795759+00:00

Web Security Academy

CSRF

Bypassing CSRF token validation

Lab

Lab: CSRF where token is duplicated in cookie

This lab's email change functionality is vulnerable to CSRF. It attempts to use the insecure "double submit" CSRF prevention technique.

To solve the lab, use your exploit server to host an HTML page that uses a CSRF attack to change the viewer's email address.

You can log in to your own account using the following credentials: wiener:peter

Hint

You cannot register an email address that is already taken by another user. If you change your own email address while testing your exploit, make sure you use a different email address for the final exploit you deliver to the victim.

Solution

Open Burp's browser and log in to your account. Submit the "Update email" form, and find the resulting request in your Proxy history.

Send the request to Burp Repeater and observe that the value of the csrf body parameter is simply being validated by comparing it with the csrf cookie.

Perform a search, send the resulting request to Burp Repeater, and observe that the search term gets reflected in the Set-Cookie header. Since the search function has no CSRF protection, you can use this to inject cookies into the victim user's browser.

Create a URL that uses this vulnerability to inject a fake csrf cookie into the victim's browser:

/?search=test%0d%0aSet-Cookie:%20csrf=fake%3b%20SameSite=None

Create and host a proof of concept exploit as described in the solution to the CSRF vulnerability with no defenses lab, ensuring that your CSRF token is set to "fake". The exploit should be created from the email change request.

Remove the auto-submit <script> block and instead add the following code to inject the cookie and submit the form:

<img src="https://YOUR-LAB-ID.web-security-academy.net/?search=test%0d%0aSet-Cookie:%20csrf=fake%3b%20SameSite=None" onerror="document.forms[0].submit();"/>

Change the email address in your exploit so that it doesn't match your own.

Store the exploit, then click "Deliver to victim" to solve the lab.

Community solutions

Rana Khalil

Michael Sommer

Find CSRF vulnerabilities using Burp Suite

Try for free
