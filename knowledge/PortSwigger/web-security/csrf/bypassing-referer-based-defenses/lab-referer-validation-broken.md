# Lab: CSRF with broken Referer validation

Source: https://portswigger.net/web-security/csrf/bypassing-referer-based-defenses/lab-referer-validation-broken
Fetched: 2026-06-28T09:17:45.882886+00:00

Web Security Academy

CSRF

Bypassing Referer-based CSRF defenses

Lab

Lab: CSRF with broken Referer validation

This lab's email change functionality is vulnerable to CSRF. It attempts to detect and block cross domain requests, but the detection mechanism can be bypassed.

To solve the lab, use your exploit server to host an HTML page that uses a CSRF attack to change the viewer's email address.

You can log in to your own account using the following credentials: wiener:peter

Hint

You cannot register an email address that is already taken by another user. If you change your own email address while testing your exploit, make sure you use a different email address for the final exploit you deliver to the victim.

Solution

Open Burp's browser and log in to your account. Submit the "Update email" form, and find the resulting request in your Proxy history.

Send the request to Burp Repeater. Observe that if you change the domain in the Referer HTTP header, the request is rejected.

Copy the original domain of your lab instance and append it to the Referer header in the form of a query string. The result should look something like this:

Referer: https://arbitrary-incorrect-domain.net?YOUR-LAB-ID.web-security-academy.net

Send the request and observe that it is now accepted. The website seems to accept any Referer header as long as it contains the expected domain somewhere in the string.

Create a CSRF proof of concept exploit as described in the solution to the CSRF vulnerability with no defenses lab and host it on the exploit server. Edit the JavaScript so that the third argument of the history.pushState() function includes a query string with your lab instance URL as follows:

history.pushState("", "", "/?YOUR-LAB-ID.web-security-academy.net")

This will cause the Referer header in the generated request to contain the URL of the target site in the query string, just like we tested earlier.

If you store the exploit and test it by clicking "View exploit", you may encounter the "invalid Referer header" error again. This is because many browsers now strip the query string from the Referer header by default as a security measure. To override this behavior and ensure that the full URL is included in the request, go back to the exploit server and add the following header to the "Head" section:

Referrer-Policy: unsafe-url

Note that unlike the normal Referer header, the word "referrer" must be spelled correctly in this case.

Change the email address in your exploit so that it doesn't match your own.

Store the exploit, then click "Deliver to victim" to solve the lab.

Community solutions

Rana Khalil

Michael Sommer

Find CSRF vulnerabilities using Burp Suite

Try for free
