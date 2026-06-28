# Manipulating WebSocket handshakes with Burp Suite

Source: https://portswigger.net/burp/documentation/desktop/testing-workflow/vulnerabilities/websockets/manipulating-websocket-handshakes
Fetched: 2026-06-28T09:16:01.762127+00:00

Support Center

Documentation

Desktop editions

Testing workflow

Testing for vulnerabilities

Testing for WebSocket vulnerabilities

Manipulating WebSocket handshakes

ProfessionalCommunity Edition

Manipulating WebSocket handshakes with Burp Suite

Last updated:

June 18, 2026

Read time:

2 Minutes

A WebSocket handshake is an HTTP message that establishes a WebSocket connection. You can often access additional attack surface by manipulating these messages.

This tutorial explains how to clone, modify, and resend WebSocket handshakes in Burp Repeater. You can follow along with the steps below using the Manipulating WebSocket messages to exploit vulnerabilities Web Security Academy lab.

Steps

To manipulate WebSocket handshakes:

Browse around your target application to map its attack surface.

Go to Proxy > WebSockets history. This tab displays a table of any WebSocket messages that Burp's browser has exchanged with the target host.

Right-click on a message and select Send to Repeater. Burp opens a new WebSockets tab in Repeater.

Click the edit icon to view a list of WebSocket connections that have been used in your current Burp session.

Select the connection you want to base your new connection on and click Clone.

If required, amend the Host, Port, and Use HTTPS settings.

In the Request panel, amend the body of the message.

There are a wide range of exploits you could perform here, depending on the application's logic and how it uses WebSockets. For example, you could add an X-Forwarded-For header to spoof your IP address, enabling you to get around restrictions on your actual IP.

Click Connect to create the modified connection.

Click the edit icon to view the list of WebSocket connections.

Select the new connection from the list and click Attach. Repeater will now use the new connection for all messages sent from the open tab.

Related pages

Web Security Academy: Testing for WebSockets security vulnerabilities

Working with WebSocket messages in Burp Repeater

WebSockets history
