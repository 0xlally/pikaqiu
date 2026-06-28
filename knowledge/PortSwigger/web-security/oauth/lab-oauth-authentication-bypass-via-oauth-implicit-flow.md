# Lab: Authentication bypass via OAuth implicit flow

Source: https://portswigger.net/web-security/oauth/lab-oauth-authentication-bypass-via-oauth-implicit-flow
Fetched: 2026-06-28T09:17:57.280108+00:00

Web Security Academy

OAuth authentication

Lab

Lab: Authentication bypass via OAuth implicit flow

This lab uses an OAuth service to allow users to log in with their social media account. Flawed validation by the client application makes it possible for an attacker to log in to other users' accounts without knowing their password.

To solve the lab, log in to Carlos's account. His email address is carlos@carlos-montoya.net.

You can log in with your own social media account using the following credentials: wiener:peter.

Solution

While proxying traffic through Burp, click "My account" and complete the OAuth login process. Afterwards, you will be redirected back to the blog website.

In Burp, go to "Proxy" > "HTTP history" and study the requests and responses that make up the OAuth flow. This starts from the authorization request GET /auth?client_id=[...].

Notice that the client application (the blog website) receives some basic information about the user from the OAuth service. It then logs the user in by sending a POST request containing this information to its own /authenticate endpoint, along with the access token.

Send the POST /authenticate request to Burp Repeater. In Repeater, change the email address to carlos@carlos-montoya.net and send the request. Observe that you do not encounter an error.

Right-click on the POST request and select "Request in browser" > "In original session". Copy this URL and visit it in the browser. You are logged in as Carlos and the lab is solved.

Community solutions

Michael Sommer

Find OAuth 2.0 authentication vulnerabilities using Burp Suite

Try for free
