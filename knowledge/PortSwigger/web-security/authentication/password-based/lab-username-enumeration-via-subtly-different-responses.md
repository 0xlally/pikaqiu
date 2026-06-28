# Lab: Username enumeration via subtly different responses

Source: https://portswigger.net/web-security/authentication/password-based/lab-username-enumeration-via-subtly-different-responses
Fetched: 2026-06-28T09:17:41.873791+00:00

Web Security Academy

Authentication vulnerabilities

Password-based

Lab

Lab: Username enumeration via subtly different responses

This lab is subtly vulnerable to username enumeration and password brute-force attacks. It has an account with a predictable username and password, which can be found in the following wordlists:

Candidate usernames

Candidate passwords

To solve the lab, enumerate a valid username, brute-force this user's password, then access their account page.

Solution

With Burp running, submit an invalid username and password. Highlight the username parameter in the POST /login request and send it to Burp Intruder.

Go to Intruder. Notice that the username parameter is automatically marked as a payload position.

In the Payloads side panel, make sure that the Simple list payload type is selected and add the list of candidate usernames.

Click on the Settings tab to open the Settings side panel. Under Grep - Extract, click Add. In the dialog that appears, scroll down through the response until you find the error message Invalid username or password.. Use the mouse to highlight the text content of the message. The other settings will be automatically adjusted. Click OK and then start the attack.

When the attack is finished, notice that there is an additional column containing the error message you extracted. Sort the results using this column to notice that one of them is subtly different.

Look closer at this response and notice that it contains a typo in the error message - instead of a full stop/period, there is a trailing space. Make a note of this username.

Close the results window and go back to the Intruder tab. Insert the username you just identified and add a payload position to the password parameter:

username=identified-user&password=§invalid-password§

In the Payloads side panel, clear the list of usernames and replace it with the list of passwords. Start the attack.

When the attack is finished, notice that one of the requests received a 302 response. Make a note of this password.

Log in using the username and password that you identified and access the user account page to solve the lab.

Note

It's also possible to brute-force the login using a single cluster bomb attack. However, it's generally much more efficient to enumerate a valid username first if possible.

Community solutions

Rana Khalil

Michael Sommer

Find vulnerabilities in your authentication using Burp Suite

Try for free
