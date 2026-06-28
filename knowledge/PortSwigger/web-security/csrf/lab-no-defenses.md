# Lab: CSRF vulnerability with no defenses

Source: https://portswigger.net/web-security/csrf/lab-no-defenses
Fetched: 2026-06-28T09:17:46.665472+00:00

Web Security Academy

CSRF

Lab

Lab: CSRF vulnerability with no defenses

This lab's email change functionality is vulnerable to CSRF.

To solve the lab, craft some HTML that uses a CSRF attack to change the viewer's email address and upload it to your exploit server.

You can log in to your own account using the following credentials: wiener:peter

Hint

You cannot register an email address that is already taken by another user. If you change your own email address while testing your exploit, make sure you use a different email address for the final exploit you deliver to the victim.

Solution

Open Burp's browser and log in to your account. Submit the "Update email" form, and find the resulting request in your Proxy history.

If you're using Burp Suite Professional, right-click on the request and select Engagement tools / Generate CSRF PoC. Enable the option to include an auto-submit script and click "Regenerate".

Alternatively, if you're using Burp Suite Community Edition, use the following HTML template. You can get the request URL by right-clicking and selecting "Copy URL".

<form method="POST" action="https://YOUR-LAB-ID.web-security-academy.net/my-account/change-email">

<input type="hidden" name="email" value="anything@web-security-academy.net">

</form>

<script>

document.forms[0].submit();

</script>

Go to the exploit server, paste your exploit HTML into the "Body" section, and click "Store".

To verify that the exploit works, try it on yourself by clicking "View exploit" and then check the resulting HTTP request and response.

Change the email address in your exploit so that it doesn't match your own.

Click "Deliver to victim" to solve the lab.

Community solutions

Intigriti

Rana Khalil

z3nsh3ll

Michael Sommer

Find CSRF vulnerabilities using Burp Suite

Try for free
