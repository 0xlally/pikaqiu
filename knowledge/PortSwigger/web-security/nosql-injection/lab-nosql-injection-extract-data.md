# Lab: Exploiting NoSQL injection to extract data

Source: https://portswigger.net/web-security/nosql-injection/lab-nosql-injection-extract-data
Fetched: 2026-06-28T09:17:56.597546+00:00

Web Security Academy

NoSQL injection

Lab

Lab: Exploiting NoSQL injection to extract data

The user lookup functionality for this lab is powered by a MongoDB NoSQL database. It is vulnerable to NoSQL injection.

To solve the lab, extract the password for the administrator user, then log in to their account.

You can log in to your own account using the following credentials: wiener:peter.

Tip

The password only uses lowercase letters.

Solution

In Burp's browser, access the lab and log in to the application using the credentials wiener:peter.

In Burp, go to Proxy > HTTP history. Right-click the GET /user/lookup?user=wiener request and select

Send to Repeater.

In Repeater, submit a ' character in the user parameter. Notice that this causes an error. This may indicate that the user input was not filtered or sanitized correctly.

Submit a valid JavaScript payload in the user parameter. For example, you could use wiener'+'

Make sure to URL-encode the payload by highlighting it and using the hotkey Ctrl-U. Notice that it retrieves the account details for the

wiener user, which indicates that a form of server-side injection may be occurring.

Identify whether you can inject boolean conditions to change the response:

Submit a false condition in the user parameter. For example: wiener' && '1'=='2

Make sure to URL-encode the payload. Notice that it retrieves the message Could not find user.

Submit a true condition in the user parameter. For example: wiener' &&

'1'=='1

Make sure to URL-encode the payload. Notice that it no longer causes an error. Instead, it retrieves the account details for the

wiener user. This demonstrates that you can trigger different responses for true and false conditions.

Identify the password length:

Change the user parameter to administrator' && this.password.length < 30 || 'a'=='b, then send the request.

Make sure to URL-encode the payload. Notice that the response retrieves the account details for the administrator user. This indicates that the condition is true because the password is less than 30 characters.

Reduce the password length in the payload, then resend the request.

Continue to try different lengths.

Notice that when you submit the value 9, you retrieve the account details for the administrator user, but when you submit the value

8, you receive an error message because the condition is false. This indicates that the password is 8 characters long.

Right-click the request and select Send to Intruder.

In Intruder, enumerate the password:

Change the user parameter to administrator' && this.password[§0§]=='§a§. This includes two payload positions. Make sure to URL-encode the payload.

Select Cluster bomb attack from the attack type drop-down menu.

In the Payloads side panel, select position 1 from the Payload position drop-down list. Add numbers from 0 to 7 for each character of the password.

Select position 2 from the Payload position drop-down list, then add lowercase letters from a to

z. If you're using Burp Suite Professional, you can use the built-in a-z list.

Click Start attack.

Sort the attack results by Payload 1, then Length. Notice that one request for each character position (0 to 7) has evaluated to true and retrieved the details for the

administrator user. Note the letters from the Payload 2 column down.

In Burp's browser, log in as the administrator user using the enumerated password. The lab is solved.

Community solutions

Popo Hack

Find NoSQL injection vulnerabilities using Burp Suite

Try for free
