# Brute-forcing logins with Burp Suite

Source: https://portswigger.net/burp/documentation/desktop/testing-workflow/vulnerabilities/authentication-mechanisms/brute-forcing-logins
Fetched: 2026-06-28T09:15:59.527260+00:00

Support Center

Documentation

Desktop editions

Testing workflow

Testing for vulnerabilities

Testing authentication mechanisms

Brute-forcing logins

ProfessionalCommunity Edition

Brute-forcing logins with Burp Suite

Last updated:

June 18, 2026

Read time:

2 Minutes

Although it's far more efficient to first enumerate a valid username and then attempt to guess the matching password, this may not always be possible. Using Burp Intruder, you can attempt to brute-force both usernames and passwords in a single attack.

Note

The example below is simplified to demonstrate how to use the relevant features of Burp Suite. To run this kind of attack on real websites, you usually need to also bypass defenses such as rate limiting. For some ideas on how to do this, see the Authentication topic on the Web Security Academy.

Before you start

Obtain lists of potential usernames and passwords. For the example below, you can use the following lists:

Usernames

Passwords

In practice, we recommend sorting the list in order of how likely you think the username or password is to be correct.

Steps

You can follow along with the process below using the Username enumeration via subtly different responses lab from our Web Security Academy.

Send the request for submitting the login form to Burp Intruder.

Go to Intruder and select Cluster bomb attack from the attack type drop-down menu.

In the request, highlight the username value and click Add § to mark it as a payload position. Do the same for the password.

In the Payloads side panel, select position 1 from the Payload position drop-down list.

Under Payload configuration, paste the list of usernames.

Select position 2 from the Payload position drop-down list, and paste the list of passwords.

Click Start attack. The attack starts running in the new dialog. Intruder sends a request for every possible combination of the provided usernames and passwords.

When the attack is finished, study the responses to look for any behavior that may indicate a valid login. For example, look for any anomalous error messages, response times, or status codes. In the example below, one of the requests has received a 302 response.

To investigate the contents of a response in detail, right-click and select Send to Comparer (response). Do the same for the original response.

Go to the Comparer tab. Select the two responses and click Words or Bytes to compare the responses. Any differences are highlighted.

Related pages

Burp Intruder

Predefined payload lists

Grep - match

Grep - extract

Burp Comparer

Academy: Vulnerabilities in password-based login mechanisms
