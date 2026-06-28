# Lab: Forced OAuth profile linking

Source: https://portswigger.net/web-security/oauth/lab-oauth-forced-oauth-profile-linking
Fetched: 2026-06-28T09:17:57.424670+00:00

Web Security Academy

OAuth authentication

Lab

Lab: Forced OAuth profile linking

This lab gives you the option to attach a social media profile to your account so that you can log in via OAuth instead of using the normal username and password. Due to the insecure implementation of the OAuth flow by the client application, an attacker can manipulate this functionality to obtain access to other users' accounts.

To solve the lab, use a CSRF attack to attach your own social media profile to the admin user's account on the blog website, then access the admin panel and delete carlos.

The admin user will open anything you send from the exploit server and they always have an active session on the blog website.

You can log in to your own accounts using the following credentials:

Blog website account: wiener:peter

Social media profile: peter.wiener:hotdog

Solution

While proxying traffic through Burp, click "My account". You are taken to a normal login page, but notice that there is an option to log in using your social media profile instead. For now, just log in to the blog website directly using the classic login form.

Notice that you have the option to attach your social media profile to your existing account.

Click "Attach a social profile". You are redirected to the social media website, where you should log in using your social media credentials to complete the OAuth flow. Afterwards, you will be redirected back to the blog website.

Log out and then click "My account" to go back to the login page. This time, choose the "Log in with social media" option. Observe that you are logged in instantly via your newly linked social media account.

In the proxy history, study the series of requests for attaching a social profile. In the GET /auth?client_id[...] request, observe that the redirect_uri for this functionality sends the authorization code to /oauth-linking. Importantly, notice that the request does not include a state parameter to protect against CSRF attacks.

Turn on proxy interception and select the "Attach a social profile" option again.

Go to Burp Proxy and forward any requests until you have intercepted the one for GET /oauth-linking?code=[...]. Right-click on this request and select "Copy URL".

Drop the request. This is important to ensure that the code is not used and, therefore, remains valid.

Turn off proxy interception and log out of the blog website.

Go to the exploit server and create an iframe in which the src attribute points to the URL you just copied. The result should look something like this:

<iframe src="https://YOUR-LAB-ID.web-security-academy.net/oauth-linking?code=STOLEN-CODE"></iframe>

Deliver the exploit to the victim. When their browser loads the iframe, it will complete the OAuth flow using your social media profile, attaching it to the admin account on the blog website.

Go back to the blog website and select the "Log in with social media" option again. Observe that you are instantly logged in as the admin user. Go to the admin panel and delete carlos to solve the lab.

Community solutions

Michael Sommer

Find OAuth 2.0 authentication vulnerabilities using Burp Suite

Try for free
