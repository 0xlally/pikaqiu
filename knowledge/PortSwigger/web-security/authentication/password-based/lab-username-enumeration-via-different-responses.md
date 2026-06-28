# Lab: Username enumeration via different responses

Source: https://portswigger.net/web-security/authentication/password-based/lab-username-enumeration-via-different-responses
Fetched: 2026-06-28T09:17:41.837347+00:00

Web Security Academy

Authentication vulnerabilities

Password-based

Lab

Lab: Username enumeration via different responses

This lab is vulnerable to username enumeration and password brute-force attacks. It has an account with a predictable username and password, which can be found in the following wordlists:

Candidate usernames

Candidate passwords

To solve the lab, enumerate a valid username, brute-force this user's password, then access their account page.

Solution

With Burp running, investigate the login page and submit an invalid username and password.

In Burp, go to Proxy > HTTP history and find the POST /login request. Highlight the value of the username parameter in the request and send it to Burp Intruder.

In Burp Intruder, notice that the username parameter is automatically set as a payload position. This position is indicated by two § symbols, for example: username=§invalid-username§. Leave the password as any static value for now.

Make sure that Sniper attack is selected.

In the Payloads side panel, make sure that the Simple list payload type is selected.

Under Payload configuration, paste the list of candidate usernames. Finally, click Start attack. The attack will start in a new window.

When the attack is finished, examine the Length column in the results table. You can click on the column header to sort the results. Notice that one of the entries is longer than the others. Compare the response to this payload with the other responses. Notice that other responses contain the message Invalid username, but this response says Incorrect password. Make a note of the username in the Payload column.

Close the attack and go back to the Intruder tab. Click Clear §, then change the username parameter to the username you just identified. Add a payload position to the password parameter. The result should look something like this:

username=identified-user&password=§invalid-password§

In the Payloads side panel, clear the list of usernames and replace it with the list of candidate passwords. Click Start attack.

When the attack is finished, look at the Status column. Notice that each request received a response with a 200 status code except for one, which got a 302 response. This suggests that the login attempt was successful - make a note of the password in the Payload column.

Log in using the username and password that you identified and access the user account page to solve the lab.

Note

It's also possible to brute-force the login using a single cluster bomb attack. However, it's generally much more efficient to enumerate a valid username first if possible.

Community solutions

Rana Khalil

Michael Sommer

Find vulnerabilities in your authentication using Burp Suite

Try for free
