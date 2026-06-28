# Lab: CSRF where token is tied to non-session cookie

Source: https://portswigger.net/web-security/csrf/bypassing-token-validation/lab-token-tied-to-non-session-cookie
Fetched: 2026-06-28T09:17:46.632379+00:00

Web Security Academy

CSRF

Bypassing CSRF token validation

Lab

Lab: CSRF where token is tied to non-session cookie

This lab's email change functionality is vulnerable to CSRF. It uses tokens to try to prevent CSRF attacks, but they aren't fully integrated into the site's session handling system.

To solve the lab, use your exploit server to host an HTML page that uses a CSRF attack to change the viewer's email address.

You have two accounts on the application that you can use to help design your attack. The credentials are as follows:

wiener:peter

carlos:montoya

Hint

You cannot register an email address that is already taken by another user. If you change your own email address while testing your exploit, make sure you use a different email address for the final exploit you deliver to the victim.

Solution

Open Burp's browser and log in to your account. Submit the "Update email" form, and find the resulting request in your Proxy history.

Send the request to Burp Repeater and observe that changing the session cookie logs you out, but changing the csrfKey cookie merely results in the CSRF token being rejected. This suggests that the csrfKey cookie may not be strictly tied to the session.

Open a private/incognito browser window, log in to your other account, and send a fresh update email request into Burp Repeater.

Observe that if you swap the csrfKey cookie and csrf parameter from the first account to the second account, the request is accepted.

Close the Repeater tab and incognito browser.

Back in the original browser, perform a search, send the resulting request to Burp Repeater, and observe that the search term gets reflected in the Set-Cookie header. Since the search function has no CSRF protection, you can use this to inject cookies into the victim user's browser.

Create a URL that uses this vulnerability to inject your csrfKey cookie into the victim's browser:

/?search=test%0d%0aSet-Cookie:%20csrfKey=YOUR-KEY%3b%20SameSite=None

Create and host a proof of concept exploit as described in the solution to the CSRF vulnerability with no defenses lab, ensuring that you include your CSRF token. The exploit should be created from the email change request.

Remove the auto-submit <script> block, and instead add the following code to inject the cookie:

<img src="https://YOUR-LAB-ID.web-security-academy.net/?search=test%0d%0aSet-Cookie:%20csrfKey=YOUR-KEY%3b%20SameSite=None" onerror="document.forms[0].submit()">

Change the email address in your exploit so that it doesn't match your own.

Store the exploit, then click "Deliver to victim" to solve the lab.

Community solutions

Rana Khalil

Michael Sommer

Find CSRF vulnerabilities using Burp Suite

Try for free
