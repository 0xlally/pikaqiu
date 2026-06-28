# Lab: CSRF where token validation depends on token being present

Source: https://portswigger.net/web-security/csrf/bypassing-token-validation/lab-token-validation-depends-on-token-being-present
Fetched: 2026-06-28T09:17:47.628770+00:00

Web Security Academy

CSRF

Bypassing CSRF token validation

Lab

Lab: CSRF where token validation depends on token being present

This lab's email change functionality is vulnerable to CSRF.

To solve the lab, use your exploit server to host an HTML page that uses a CSRF attack to change the viewer's email address.

You can log in to your own account using the following credentials: wiener:peter

Hint

You cannot register an email address that is already taken by another user. If you change your own email address while testing your exploit, make sure you use a different email address for the final exploit you deliver to the victim.

Solution

Open Burp's browser and log in to your account. Submit the "Update email" form, and find the resulting request in your Proxy history.

Send the request to Burp Repeater and observe that if you change the value of the csrf parameter then the request is rejected.

Delete the csrf parameter entirely and observe that the request is now accepted.

If you're using Burp Suite Professional, right-click on the request, and from the context menu select Engagement tools / Generate CSRF PoC. Enable the option to include an auto-submit script and click "Regenerate".

Alternatively, if you're using Burp Suite Community Edition, use the following HTML template. You can get the request URL by right-clicking and selecting "Copy URL".

<form method="POST" action="https://YOUR-LAB-ID.web-security-academy.net/my-account/change-email">

<input type="hidden" name="$param1name" value="$param1value">

</form>

<script>

document.forms[0].submit();

</script>

Go to the exploit server, paste your exploit HTML into the "Body" section, and click "Store".

To verify if the exploit will work, try it on yourself by clicking "View exploit" and checking the resulting HTTP request and response.

Change the email address in your exploit so that it doesn't match your own.

Store the exploit, then click "Deliver to victim" to solve the lab.

Community solutions

Rana Khalil

Michael Sommer

Find CSRF vulnerabilities using Burp Suite

Try for free
