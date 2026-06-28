# Lab: Brute-forcing a stay-logged-in cookie

Source: https://portswigger.net/web-security/authentication/other-mechanisms/lab-brute-forcing-a-stay-logged-in-cookie
Fetched: 2026-06-28T09:17:40.781641+00:00

Web Security Academy

Authentication vulnerabilities

Other mechanisms

Lab

Lab: Brute-forcing a stay-logged-in cookie

This lab allows users to stay logged in even after they close their browser session. The cookie used to provide this functionality is vulnerable to brute-forcing.

To solve the lab, brute-force Carlos's cookie to gain access to his My account page.

Your credentials: wiener:peter

Victim's username: carlos

Candidate passwords

Solution

With Burp running, log in to your own account with the Stay logged in option selected. Notice that this sets a stay-logged-in cookie.

Examine this cookie in the Inspector panel and notice that it is Base64-encoded. Its decoded value is wiener:51dc30ddc473d43a6011e9ebba6ca770. Study the length and character set of this string and notice that it could be an MD5 hash. Given that the plaintext is your username, you can make an educated guess that this may be a hash of your password. Hash your password using MD5 to confirm that this is the case. We now know that the cookie is constructed as follows:

base64(username+':'+md5HashOfPassword)

Log out of your account.

In the most recent GET /my-account?id=wiener request highlight the stay-logged-in cookie parameter and send the request to Burp Intruder.

In Burp Intruder, notice that the stay-logged-in cookie has been automatically added as a payload position. Add your own password as a single payload.

Under Payload processing, add the following rules in order. These rules will be applied sequentially to each payload before the request is submitted.

Hash: MD5

Add prefix: wiener:

Encode: Base64-encode

As the Update email button is only displayed when you access the My

account page in an authenticated state, we can use the presence or absence of this button to determine whether we've successfully brute-forced the cookie. In the Settings side panel, add a grep match rule to flag any responses containing the string Update email. Start the attack.

Notice that the generated payload was used to successfully load your own account page. This confirms that the payload processing rules work as expected and you were able to construct a valid cookie for your own account.

Make the following adjustments and then repeat this attack:

Remove your own password from the payload list and add the list of candidate passwords instead.

Change the id parameter in the request URL to carlos instead of wiener.

Change the Add prefix rule to add carlos: instead of wiener:.

When the attack is finished, the lab will be solved. Notice that only one request returned a response containing Update email. The payload from this request is the valid stay-logged-in cookie for Carlos's account.

Community solutions

Rana Khalil

Find vulnerabilities in your authentication using Burp Suite

Try for free
