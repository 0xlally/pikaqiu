# Lab: Broken brute-force protection, IP block

Source: https://portswigger.net/web-security/authentication/password-based/lab-broken-bruteforce-protection-ip-block
Fetched: 2026-06-28T09:17:41.310606+00:00

Web Security Academy

Authentication vulnerabilities

Password-based

Lab

Lab: Broken brute-force protection, IP block

This lab is vulnerable due to a logic flaw in its password brute-force protection. To solve the lab, brute-force the victim's password, then log in and access their account page.

Your credentials: wiener:peter

Victim's username: carlos

Candidate passwords

Hint

Advanced users may want to solve this lab by using a macro or the Turbo Intruder extension. However, it is possible to solve the lab without using these advanced features.

Solution

With Burp running, investigate the login page. Observe that your IP is temporarily blocked if you submit 3 incorrect logins in a row. However, notice that you can reset the counter for the number of failed login attempts by logging in to your own account before this limit is reached.

Enter an invalid username and password, then send the POST /login request to Burp Intruder. Create a pitchfork attack with payload positions in both the username and password parameters.

Click Resource pool to open the Resource

pool side panel, then add the attack to a resource pool with Maximum concurrent requests set to 1. By only sending one request at a time, you can ensure that your login attempts are sent to the server in the correct order.

Click Payloads to open the Payloads side panel, then select position 1 from the Payload position drop-down list. Add a list of payloads that alternates between your username and carlos. Make sure that your username is first and that carlos is repeated at least 100 times.

Edit the list of candidate passwords and add your own password before each one. Make sure that your password is aligned with your username in the other list.

Select position 2 from the Payload position drop-down list, then add the password list. Start the attack.

When the attack finishes, filter the results to hide responses with a 200 status code. Sort the remaining results by username. There should only be a single 302 response for requests with the username carlos. Make a note of the password from the Payload 2 column.

Log in to Carlos's account using the password that you identified and access his account page to solve the lab.

Community solutions

Rana Khalil

Find vulnerabilities in your authentication using Burp Suite

Try for free
