# Cross-site WebSocket hijacking

Source: https://portswigger.net/web-security/websockets/cross-site-websocket-hijacking
Fetched: 2026-06-28T09:18:06.289103+00:00

Web Security Academy

WebSockets

CSWSH

Cross-site WebSocket hijacking

In this section, we'll explain cross-site WebSocket hijacking (CSWSH), describe the impact of a compromise, and spell out how to perform a cross-site WebSocket hijacking attack.

What is cross-site WebSocket hijacking?

Cross-site WebSocket hijacking (also known as cross-origin WebSocket hijacking) involves a cross-site request forgery (CSRF) vulnerability on a WebSocket handshake. It arises when the WebSocket handshake request relies solely on HTTP cookies for session handling and does not contain any CSRF tokens or other unpredictable values.

An attacker can create a malicious web page on their own domain which establishes a cross-site WebSocket connection to the vulnerable application. The application will handle the connection in the context of the victim user's session with the application.

The attacker's page can then send arbitrary messages to the server via the connection and read the contents of messages that are received back from the server. This means that, unlike regular CSRF, the attacker gains two-way interaction with the compromised application.

What is the impact of cross-site WebSocket hijacking?

A successful cross-site WebSocket hijacking attack will often enable an attacker to:

Perform unauthorized actions masquerading as the victim user. As with regular CSRF, the attacker can send arbitrary messages to the server-side application. If the application uses client-generated WebSocket messages to perform any sensitive actions, then the attacker can generate suitable messages cross-domain and trigger those actions.

Retrieve sensitive data that the user can access. Unlike with regular CSRF, cross-site WebSocket hijacking gives the attacker two-way interaction with the vulnerable application over the hijacked WebSocket. If the application uses server-generated WebSocket messages to return any sensitive data to the user, then the attacker can intercept those messages and capture the victim user's data.

Performing a cross-site WebSocket hijacking attack

Since a cross-site WebSocket hijacking attack is essentially a CSRF vulnerability on a WebSocket handshake, the first step to performing an attack is to review the WebSocket handshakes that the application carries out and determine whether they are protected against CSRF.

In terms of the normal conditions for CSRF attacks, you typically need to find a handshake message that relies solely on HTTP cookies for session handling and doesn't employ any tokens or other unpredictable values in request parameters.

For example, the following WebSocket handshake request is probably vulnerable to CSRF, because the only session token is transmitted in a cookie:

GET /chat HTTP/1.1

Host: normal-website.com

Sec-WebSocket-Version: 13

Sec-WebSocket-Key: wDqumtseNBJdhkihL6PW7w==

Connection: keep-alive, Upgrade

Cookie: session=KOsEJNuflw4Rd9BDNrVmvwBF9rEijeE2

Upgrade: websocket

Note

The Sec-WebSocket-Key header contains a random value to prevent errors from caching proxies, and is not used for authentication or session handling purposes.

If the WebSocket handshake request is vulnerable to CSRF, then an attacker's web page can perform a cross-site request to open a WebSocket on the vulnerable site. What happens next in the attack depends entirely on the application's logic and how it is using WebSockets. The attack might involve:

Sending WebSocket messages to perform unauthorized actions on behalf of the victim user.

Sending WebSocket messages to retrieve sensitive data.

Sometimes, just waiting for incoming messages to arrive containing sensitive data.

Find WebSocket vulnerabilities using Burp Suite

Try for free
