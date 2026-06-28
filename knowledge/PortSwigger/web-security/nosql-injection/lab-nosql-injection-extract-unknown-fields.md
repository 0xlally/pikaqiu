# Lab: Exploiting NoSQL operator injection to extract unknown fields

Source: https://portswigger.net/web-security/nosql-injection/lab-nosql-injection-extract-unknown-fields
Fetched: 2026-06-28T09:17:56.513657+00:00

Web Security Academy

NoSQL injection

Lab

Lab: Exploiting NoSQL operator injection to extract unknown fields

The user lookup functionality for this lab is powered by a MongoDB NoSQL database. It is vulnerable to NoSQL injection.

To solve the lab, log in as carlos.

Tip

To solve the lab, you'll first need to exfiltrate the value of the password reset token for the user

carlos.

Solution

In Burp's browser, attempt to log in to the application with username carlos and password invalid. Notice that you receive an Invalid username or password error message.

In Burp, go to Proxy > HTTP history. Right-click the POST

/login request and select Send to Repeater.

In Repeater, change the value of the password parameter from "invalid" to

{"$ne":"invalid"}, then send the request. Notice that you now receive an

Account locked error message. You can't access Carlos's account, but this response indicates that the $ne operator has been accepted and the application is vulnerable.

In Burp's browser, attempt to reset the password for the carlos account. When you submit the carlos username, observe that the reset mechanism involves email verification, so you can't reset the account yourself.

In Repeater, use the POST /login request to test whether the application is vulnerable to JavaScript injection:

Add "$where": "0" as an additional parameter in the JSON data as follows:

{"username":"carlos","password":{"$ne":"invalid"}, "$where": "0"}

Send the request. Notice that you receive an Invalid username or password error message.

Change "$where": "0" to "$where": "1", then resend the request. Notice that you receive an Account locked error message. This indicates that the JavaScript in the $where clause is being evaluated.

Right-click the request and select Send to Intruder.

In Intruder, construct an attack to identify all the fields on the user object:

Update the $where parameter as follows:

"$where":"Object.keys(this)[1].match('^.{}.*')"

Add two payload positions. The first identifies the character position number, and

the second identifies the character itself:

"$where":"Object.keys(this)[1].match('^.{§§}§§.*')"

Select Cluster bomb attack from the attack type drop-down menu.

In the Payloads side panel, select position 1 from the Payload position drop-down list, then set the

Payload type to

Numbers. Set the number range, for example from 0 to 20.

Select position 2 from the Payload position drop-down list and make sure the Payload type is set to

Simple list. Add all numbers,

lower-case letters and upper-case letters as payloads. If you're using Burp Suite Professional,

you can use the built-in word lists a-z, A-Z, and 0-9.

Click Start attack.

Sort the attack results by Payload 1, then Length, to identify responses with an

Account locked message

instead of the Invalid username or password message. Notice that the characters in the Payload

2 column

spell out the name of the parameter: username.

Repeat the above steps to identify further JSON parameters. You can do this

by incrementing the index of the keys array with each attempt, for example:

"$where":"Object.keys(this)[2].match('^.{}.*')"

Notice that one of the JSON parameters is for a password reset token.

Test the identified password reset field name as a query parameter on different

endpoints:

In Proxy > HTTP history, identify the GET

/forgot-password request as a

potentially interesting endpoint, as it relates to the password reset

functionality. Right-click the request and select Send to Repeater.

In Repeater, submit an invalid field in the URL: GET

/forgot-password?foo=invalid.

Notice that the response is identical to the original response.

Submit the exfiltrated name of the password reset token field in the URL:

GET /forgot-password?YOURTOKENNAME=invalid. Notice that you receive an

Invalid token error message. This confirms that you have the correct token name and endpoint.

In Intruder, use the POST /login request to construct an attack that

extracts the value of Carlos's password reset token:

Keep the settings from your previous attack, but update the $where parameter as follows: "$where":"this.YOURTOKENNAME.match('^.{§§}§§.*')"

Make sure that you replace YOURTOKENNAME with the password reset token name that you exfiltrated in the previous step.

Click Start attack.

Sort the attack results by Payload 1, then Length, to identify responses with an Account locked message instead of the Invalid username or password message. Note the letters from the Payload 2 column down.

In Repeater, submit the value of the password reset token in the URL of the GET /

forgot-password request:

GET /forgot-password?YOURTOKENNAME=TOKENVALUE.

Right-click the response and select Request in browser > Original session. Paste this into Burp's browser.

Change Carlos's password, then log in as carlos to solve the lab.

Community solutions

Popo Hack

Find NoSQL injection vulnerabilities using Burp Suite

Try for free
