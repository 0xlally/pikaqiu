# Lab: CSRF where token validation depends on request method

Source: https://portswigger.net/web-security/csrf/bypassing-token-validation/lab-token-validation-depends-on-request-method
Fetched: 2026-06-28T09:17:46.706813+00:00

Web Security Academy

CSRF

Bypassing CSRF token validation

Lab

Lab: CSRF where token validation depends on request method

This lab's email change functionality is vulnerable to CSRF. It attempts to block CSRF attacks, but only applies defenses to certain types of requests.

To solve the lab, use your exploit server to host an HTML page that uses a CSRF attack to change the viewer's email address.

You can log in to your own account using the following credentials: wiener:peter

Hint

You cannot register an email address that is already taken by another user. If you change your own email address while testing your exploit, make sure you use a different email address for the final exploit you deliver to the victim.

Solution

Open Burp's browser and log in to your account. Submit the "Update email" form, and find the resulting request in your Proxy history.

Send the request to Burp Repeater and observe that if you change the value of the csrf parameter then the request is rejected.

Use "Change request method" on the context menu to convert it into a GET request and observe that the CSRF token is no longer verified.

If you're using Burp Suite Professional, right-click on the request, and from the context menu select Engagement tools / Generate CSRF PoC. Enable the option to include an auto-submit script and click "Regenerate".

Alternatively, if you're using Burp Suite Community Edition, use the following HTML template. You can get the request URL by right-clicking and selecting "Copy URL".

<form action="https://YOUR-LAB-ID.web-security-academy.net/my-account/change-email">

<input type="hidden" name="email" value="anything@web-security-academy.net">

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
