# Lab: Username enumeration via response timing

Source: https://portswigger.net/web-security/authentication/password-based/lab-username-enumeration-via-response-timing
Fetched: 2026-06-28T09:17:41.787730+00:00

Web Security Academy

Authentication vulnerabilities

Password-based

Lab

Lab: Username enumeration via response timing

This lab is vulnerable to username enumeration using its response times. To solve the lab, enumerate a valid username, brute-force this user's password, then access their account page.

Your credentials: wiener:peter

Candidate usernames

Candidate passwords

Hint

To add to the challenge, the lab also implements a form of IP-based brute-force protection. However, this can be easily bypassed by manipulating HTTP request headers.

Solution

With Burp running, submit an invalid username and password, then send the POST /login request to Burp Repeater. Experiment with different usernames and passwords. Notice that your IP will be blocked if you make too many invalid login attempts.

Identify that the X-Forwarded-For header is supported, which allows you to spoof your IP address and bypass the IP-based brute-force protection.

Continue experimenting with usernames and passwords. Pay particular attention to the response times. Notice that when the username is invalid, the response time is roughly the same. However, when you enter a valid username (your own), the response time is increased depending on the length of the password you entered.

Send this request to Burp Intruder and select Pitchfork attack from the attack type drop-down menu. Add the X-Forwarded-For header.

Add payload positions for the X-Forwarded-For header and the username parameter. Set the password to a very long string of characters (about 100 characters should do it).

In the Payloads side panel, select position 1 from the Payload position drop-down list. Select the Numbers payload type. Enter the range 1 - 100 and set the step to 1. Set the max fraction digits to 0. This will be used to spoof your IP.

Select position 2 from the Payload position drop-down list, then add the list of usernames. Start the attack.

When the attack finishes, at the top of the dialog, click Columns and select the Response received and Response completed options. These two columns are now displayed in the results table.

Notice that one of the response times was significantly longer than the others. Repeat this request a few times to make sure it consistently takes longer, then make a note of this username.

Create a new Burp Intruder attack for the same request. Add the X-Forwarded-For header again and add a payload position to it. Insert the username that you just identified and add a payload position to the password parameter.

In the Payloads side panel, add the list of numbers to payload position 1 and add the list of passwords to payload position 2. Start the attack.

When the attack is finished, find the response with a 302 status. Make a note of this password.

Log in using the username and password that you identified and access the user account page to solve the lab.

Note

It's also possible to brute-force the login using a single cluster bomb attack. However, it's generally much more efficient to enumerate a valid username first if possible.

Community solutions

Rana Khalil

Michael Sommer

Find vulnerabilities in your authentication using Burp Suite

Try for free
