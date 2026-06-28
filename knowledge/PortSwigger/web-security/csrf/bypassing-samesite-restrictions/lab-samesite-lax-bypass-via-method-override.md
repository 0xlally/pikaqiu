# Lab: SameSite Lax bypass via method override

Source: https://portswigger.net/web-security/csrf/bypassing-samesite-restrictions/lab-samesite-lax-bypass-via-method-override
Fetched: 2026-06-28T09:17:46.479318+00:00

Web Security Academy

CSRF

Bypassing SameSite cookie restrictions

Lab

Lab: SameSite Lax bypass via method override

This lab's change email function is vulnerable to CSRF. To solve the lab, perform a CSRF attack that changes the victim's email address. You should use the provided exploit server to host your attack.

You can log in to your own account using the following credentials: wiener:peter

Note

The default SameSite restrictions differ between browsers. As the victim uses Chrome, we recommend also using Chrome (or Burp's built-in Chromium browser) to test your exploit.

Hint

You cannot register an email address that is already taken by another user. If you change your own email address while testing your exploit, make sure you use a different email address for the final exploit you deliver to the victim.

Solution

Study the change email function

In Burp's browser, log in to your own account and change your email address.

In Burp, go to the Proxy > HTTP history tab.

Study the POST /my-account/change-email request and notice that this doesn't contain any unpredictable tokens, so may be vulnerable to CSRF if you can bypass the SameSite cookie restrictions.

Look at the response to your POST /login request. Notice that the website doesn't explicitly specify any SameSite restrictions when setting session cookies. As a result, the browser will use the default Lax restriction level.

Recognize that this means the session cookie will be sent in cross-site GET requests, as long as they involve a top-level navigation.

Bypass the SameSite restrictions

Send the POST /my-account/change-email request to Burp Repeater.

In Burp Repeater, right-click on the request and select Change request method. Burp automatically generates an equivalent GET request.

Send the request. Observe that the endpoint only allows POST requests.

Try overriding the method by adding the _method parameter to the query string:

GET /my-account/change-email?email=foo%40web-security-academy.net&_method=POST HTTP/1.1

Send the request. Observe that this seems to have been accepted by the server.

In the browser, go to your account page and confirm that your email address has changed.

Craft an exploit

In the browser, go to the exploit server.

In the Body section, create an HTML/JavaScript payload that induces the viewer's browser to issue the malicious GET request. Remember that this must cause a top-level navigation in order for the session cookie to be included. The following is one possible approach:

<script>

document.location = "https://YOUR-LAB-ID.web-security-academy.net/my-account/change-email?email=pwned@web-security-academy.net&_method=POST";

</script>

Store and view the exploit yourself. Confirm that this has successfully changed your email address on the target site.

Change the email address in your exploit so that it doesn't match your own.

Deliver the exploit to the victim to solve the lab.

Community solutions

Jarno Timmermans

nu11 secur1ty

Find CSRF vulnerabilities using Burp Suite

Try for free
