# Lab: Password reset broken logic

Source: https://portswigger.net/web-security/authentication/other-mechanisms/lab-password-reset-broken-logic
Fetched: 2026-06-28T09:17:41.174033+00:00

Web Security Academy

Authentication vulnerabilities

Other mechanisms

Lab

Lab: Password reset broken logic

This lab's password reset functionality is vulnerable. To solve the lab, reset Carlos's password then log in and access his "My account" page.

Your credentials: wiener:peter

Victim's username: carlos

Solution

With Burp running, click the Forgot your password? link and enter your own username.

Click the Email client button to view the password reset email that was sent. Click the link in the email and reset your password to whatever you want.

In Burp, go to Proxy > HTTP history and study the requests and responses for the password reset functionality. Observe that the reset token is provided as a URL query parameter in the reset email. Notice that when you submit your new password, the POST /forgot-password?temp-forgot-password-token request contains the username as hidden input. Send this request to Burp Repeater.

In Burp Repeater, observe that the password reset functionality still works even if you delete the value of the temp-forgot-password-token parameter in both the URL and request body. This confirms that the token is not being checked when you submit the new password.

In the browser, request a new password reset and change your password again. Send the POST /forgot-password?temp-forgot-password-token request to Burp Repeater again.

In Burp Repeater, delete the value of the temp-forgot-password-token parameter in both the URL and request body. Change the username parameter to carlos. Set the new password to whatever you want and send the request.

In the browser, log in to Carlos's account using the new password you just set. Click My account to solve the lab.

Community solutions

Rana Khalil

Michael Sommer

Find vulnerabilities in your authentication using Burp Suite

Try for free
