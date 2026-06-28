# Brute-forcing passwords with Burp Suite

Source: https://portswigger.net/burp/documentation/desktop/testing-workflow/vulnerabilities/authentication-mechanisms/brute-forcing-passwords
Fetched: 2026-06-28T09:15:59.305049+00:00

Support Center

Documentation

Desktop editions

Testing workflow

Testing for vulnerabilities

Testing authentication mechanisms

Brute-forcing passwords

ProfessionalCommunity Edition

Brute-forcing passwords with Burp Suite

Last updated:

June 18, 2026

Read time:

4 Minutes

Burp Suite provides a number of features that can help you brute-force the password of a given user, gaining access to their account and additional attack surface. For example, you can:

Use a list of common passwords. This is commonly known as a dictionary attack. For details on how to do this, see Running a dictionary attack.

Try every permutation of a character set. For details on how to do this, see Running an exhaustive brute-force attack.

Note

The examples below are simplified to demonstrate how to use the relevant features of Burp Suite. To run these attacks on real websites, you usually need to also bypass defenses such as rate limiting. For some ideas on how to do this, see the Authentication topic on the Web Security Academy.

Before you start

Identify one or more valid usernames for the target website. For example, you can potentially enumerate a list of usernames using Burp. For the examples below, you can assume that the username wiener is valid.

For details on how to brute-force both the username and password in a single attack, see Brute-forcing a login with Burp Suite.

Running a dictionary attack

One approach for brute-forcing passwords is to use a list of potential passwords, usually collated from previous data breaches. This is far more efficient than an exhaustive brute-force attack, but relies on the user's password being present in your list, which may not always be the case.

You can follow along with the process below using the User role controlled by request parameter lab from our Web Security Academy.

Send the request for submitting the login form to Burp Intruder.

Go to Intruder. Make sure that Sniper attack is selected.

Highlight the password value and click Add § to mark it as a payload position. Make sure that you're using a valid username. If you're following along with the lab, set the username to wiener.

In the Payloads side panel, under Payload configuration, add a list of passwords that you want to test. Ideally, sort the list in order of how likely you think the password is to be correct. This could be based on prior knowledge of the user in question or just how common the password is in general.

If you're using Burp Suite Professional, you can open the Add from list dropdown menu and select the Passwords list.

If you're using Burp Suite Community Edition, manually add a list of potential passwords.

Click Start attack. The attack starts running in the new dialog. Intruder sends a request for each password in the list.

When the attack is finished, study the responses to look for any behavior that may indicate a valid password. For example, look for any anomalous error messages, response times, or status codes. In the example below, one of the requests has received a 302 response.

To investigate the contents of a response in detail, right-click and select Send to Comparer (response). Do the same for the original response.

Go to the Comparer tab. Select the two responses and click Words or Bytes to compare the responses. Any differences are highlighted.

Running an exhaustive brute-force attack

Another approach is to attempt every possible permutation of a character set. This enables you to brute-force passwords that don't necessarily appear in a wordlist. However, for longer passwords and larger character sets, this type of attack is often impractical due to the number of requests needed. For example, an alphabetical password with five characters has over 11 million possible combinations. It's often better to try running a dictionary attack first.

Send the request for submitting the login form to Burp Intruder.

In the request, highlight the password value and click Add § to mark it as a payload position. Make sure that you're using a valid username.

In the Payloads side panel, change the Payload type to Brute forcer.

Under Payload configuration, enter the full character set and set the minimum and maximum password length that you want to test. If you're able to create your own account on the site, you can potentially get clues about the password requirements to help you determine the appropriate values.

Click Start attack. The attack starts running in the new dialog. Intruder sends a request for every possible password based on your settings.

When the attack is finished, study the responses to look for any behavior that may indicate a valid password. For example, look for any anomalous error messages, response times, or status codes. In the example below, one of the requests has received a 302 response.

To investigate the contents of a response in detail, right-click and select Send to Comparer (response). Do the same for the original response.

Go to the Comparer tab. Select the two responses and click Words or Bytes to compare the responses. Any differences are highlighted.

Related pages

Burp Intruder

Predefined payload lists

Burp Comparer

Academy: Vulnerabilities in password-based login mechanisms
