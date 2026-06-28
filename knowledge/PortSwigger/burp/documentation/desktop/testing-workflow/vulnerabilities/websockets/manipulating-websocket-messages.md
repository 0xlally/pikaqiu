# Manipulating WebSocket messages with Burp Suite

Source: https://portswigger.net/burp/documentation/desktop/testing-workflow/vulnerabilities/websockets/manipulating-websocket-messages
Fetched: 2026-06-28T09:16:01.536880+00:00

Support Center

Documentation

Desktop editions

Testing workflow

Testing for vulnerabilities

Testing for WebSocket vulnerabilities

Manipulating WebSocket messages

ProfessionalCommunity Edition

Manipulating WebSocket messages with Burp Suite

Last updated:

June 18, 2026

Read time:

1 Minute

Finding vulnerabilities in WebSockets generally involves manipulating messages in ways that the application doesn't expect. For example, if you can modify existing messages or create new ones you may be able to deliver SQL injection or cross-site scripting exploits.

This tutorial explains how to modify and resend WebSocket messages in Repeater. You can follow along with the steps below using the Manipulating WebSocket messages to exploit vulnerabilities Web Security Academy lab.

Steps

To modify and re-send WebSocket messages:

Browse around your target application to map its attack surface.

Go to Proxy > WebSockets history. This tab displays a table of any WebSocket messages that Burp's browser has exchanged with the target host.

Right-click a message that you want to re-send or modify (for example, an outbound chat message) and select Send to Repeater. Burp creates a new WebSocket tab in Repeater.

Go to Repeater, select the new tab, and click Send.

Check the History panel to confirm that the message was re-sent.

In the Send WebSocket message panel, modify the message. For example, you could send a proof-of-concept XSS attack at this point.

Click Send again.

Confirm that the modified message appears in the History panel as sent.

Related pages

Web Security Academy: Testing for WebSockets security vulnerabilities

Working with WebSocket messages in Burp Repeater

WebSockets history

Proxy settings: WebSocket interception rules
