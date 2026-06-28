# Lab: Password reset poisoning via middleware

Source: https://portswigger.net/web-security/authentication/other-mechanisms/lab-password-reset-poisoning-via-middleware
Fetched: 2026-06-28T09:17:41.190751+00:00

Web Security Academy

Authentication vulnerabilities

Other mechanisms

Lab

Lab: Password reset poisoning via middleware

This lab is vulnerable to password reset poisoning. The user carlos will carelessly click on any links in emails that he receives. To solve the lab, log in to Carlos's account.

You can log in to your own account using the following credentials: wiener:peter. Any emails sent to this account can be read via the email client on the exploit server.

Solution

With Burp running, investigate the password reset functionality. Observe that a link containing a unique reset token is sent via email.

Send the POST /forgot-password request to Burp Repeater. Notice that the X-Forwarded-Host header is supported and you can use it to point the dynamically generated reset link to an arbitrary domain.

Go to the exploit server and make a note of your exploit server URL.

Go back to the request in Burp Repeater and add the X-Forwarded-Host header with your exploit server URL:

X-Forwarded-Host: YOUR-EXPLOIT-SERVER-ID.exploit-server.net

Change the username parameter to carlos and send the request.

Go to the exploit server and open the access log. You should see a GET /forgot-password request, which contains the victim's token as a query parameter. Make a note of this token.

Go back to your email client and copy the valid password reset link (not the one that points to the exploit server). Paste this into the browser and change the value of the temp-forgot-password-token parameter to the value that you stole from the victim.

Load this URL and set a new password for Carlos's account.

Log in to Carlos's account using the new password to solve the lab.

Community solutions

Rana Khalil

Michael Sommer

Find vulnerabilities in your authentication using Burp Suite

Try for free
