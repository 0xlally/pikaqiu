# Response queue poisoning

Source: https://portswigger.net/web-security/request-smuggling/advanced/response-queue-poisoning
Fetched: 2026-06-28T09:18:01.001608+00:00

Web Security Academy

Request smuggling

Advanced

Response queue poisoning

Response queue poisoning

Response queue poisoning is a powerful form of request smuggling attack that causes a front-end server to start mapping responses from the back-end to the wrong requests. In practice, this means that all users of the same front-end/back-end connection are persistently served responses that were intended for someone else.

This is achieved by smuggling a complete request, thereby eliciting two responses from the back-end when the front-end server is only expecting one.

What is the impact of response queue poisoning?

The impact of response queue poisoning is normally catastrophic. Once the queue is poisoned, an attacker can capture other users' responses simply by issuing arbitrary follow-up requests. These responses may contain sensitive personal or business data, as well as session tokens and the like, which effectively grant the attacker full access to the victim's account.

Response queue poisoning also causes significant collateral damage, effectively breaking the site for any other users whose traffic is being sent to the back-end over the same TCP connection. While attempting to browse the site as normal, users will receive seemingly random responses from the server, which will prevent most functions from working correctly.

How to construct a response queue poisoning attack

For a successful response queue poisoning attack, the following criteria must be met:

The TCP connection between the front-end server and back-end server is reused for multiple request/response cycles.

The attacker is able to successfully smuggle a complete, standalone request that receives its own distinct response from the back-end server.

The attack does not result in either server closing the TCP connection. Servers generally close incoming connections when they receive an invalid request because they can't determine where the request is supposed to end.

Understanding the aftermath of request smuggling

Request smuggling attacks usually involve smuggling a partial request, which the server adds as a prefix to the start of the next request on the connection. It's important to note that the content of the smuggled request influences what happens to the connection following the initial attack.

If you just smuggle a request line with some headers, assuming that another request is sent on the connection shortly afterwards, the back-end ultimately still sees two complete requests.

If you instead smuggle a request that also contains a body, the next request on the connection will be appended to the body of the smuggled request. This often has the side-effect of truncating the final request based on the apparent Content-Length. As a result, the back-end effectively sees three requests, where the third "request" is just a series of leftover bytes:

Front-end (CL)

POST / HTTP/1.1

Host: vulnerable-website.com

Content-Type: x-www-form-urlencoded

Content-Length: 120

Transfer-Encoding: chunked

0

POST /example HTTP/1.1

Host: vulnerable-website.com

Content-Type: x-www-form-urlencoded

Content-Length: 25

x=GET / HTTP/1.1

Host: vulnerable-website.com

Back-end (TE)

POST / HTTP/1.1

Host: vulnerable-website.com

Content-Type: x-www-form-urlencoded

Content-Length: 120

Transfer-Encoding: chunked

0

POST /example HTTP/1.1

Host: vulnerable-website.com

Content-Type: x-www-form-urlencoded

Content-Length: 25

x=GET / HTTP/1.1

Host: vulnerable-website.com

As these leftover bytes don't form a valid request, this typically results in an error, causing the server to close the connection.

Smuggling a complete request

With a bit of care, you can smuggle a complete request instead of just a prefix. As long as you send exactly two requests in one, any subsequent requests on the connection will remain unchanged:

Front-end (CL)

POST / HTTP/1.1\r\n

Host: vulnerable-website.com\r\n

Content-Type: x-www-form-urlencoded\r\n

Content-Length: 61\r\n

Transfer-Encoding: chunked\r\n

\r\n

0\r\n

\r\n

GET /anything HTTP/1.1\r\n

Host: vulnerable-website.com\r\n

\r\n

GET / HTTP/1.1\r\n

Host: vulnerable-website.com\r\n

\r\n

Back-end (TE)

POST / HTTP/1.1\r\n

Host: vulnerable-website.com\r\n

Content-Type: x-www-form-urlencoded\r\n

Content-Length: 61\r\n

Transfer-Encoding: chunked\r\n

\r\n

0\r\n

\r\n

GET /anything HTTP/1.1\r\n

Host: vulnerable-website.com\r\n

\r\n

GET / HTTP/1.1\r\n

Host: vulnerable-website.com\r\n

\r\n

Notice that no invalid requests are hitting the back-end, so the connection should remain open following the attack.

Desynchronizing the response queue

When you smuggle a complete request, the front-end server still thinks it only forwarded a single request. On the other hand, the back-end sees two distinct requests, and will send two responses accordingly:

The front-end correctly maps the first response to the initial "wrapper" request and forwards this on to the client. As there are no further requests awaiting a response, the unexpected second response is held in a queue on the connection between the front-end and back-end.

When the front-end receives another request, it forwards this to the back-end as normal. However, when issuing the response, it will send the first one in the queue, that is, the leftover response to the smuggled request.

The correct response from the back-end is then left without a matching request. This cycle is repeated every time a new request is forwarded down the same connection to the back-end.

Stealing other users' responses

Once the response queue is poisoned, the attacker can just send an arbitrary request to capture another user's response.

They have no control over which responses they receive as they will always be sent the next response in the queue i.e. the response to the previous user's request. In some cases, this will be of limited interest. However, using tools like Burp Intruder, an attacker can easily automate the process of reissuing the request. By doing so, they can quickly grab an assortment of responses intended for different users, at least some of which are likely to contain useful data.

An attacker can continue to steal responses like this for as long as the front-end/back-end connection remains open. Exactly when a connection is closed differs from server to server, but a common default is to terminate a connection after it has handled 100 requests. It's also trivial to repoison a new connection once the current one is closed.

Tip

To make it easier to differentiate stolen responses from responses to your own requests, try using a non-existent path in both of the requests that you send. That way, your own requests should consistently receive a 404 response, for example.

Notes

This attack is possible both via classic HTTP/1 request smuggling and by exploiting HTTP/2 downgrading.

Find HTTP request smuggling vulnerabilities using Burp Suite

Try for free
