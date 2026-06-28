# Working with WebSocket messages in Burp Repeater

Source: https://portswigger.net/burp/documentation/desktop/tools/repeater/websocket-messages
Fetched: 2026-06-28T09:16:08.082741+00:00

Support Center

Documentation

Desktop editions

Tools

Repeater

Working with WebSocket messages

ProfessionalCommunity Edition

Working with WebSocket messages in Burp Repeater

Last updated:

June 18, 2026

Read time:

2 Minutes

You can use Burp Repeater to manipulate and resend individual WebSocket messages, and analyze the application's responses.

To send WebSocket requests with Burp Repeater:

Go to Proxy > WebSockets history.

Right-click on a WebSocket message, and click Send to Repeater. A new tab is added to Repeater containing the request.

Go to Repeater and view the WebSocket message details in the new tab.

Modify the message.

Select whether the message should be sent to the server or client.

Click Send to send the message to the target server or client, and view the response.

To resend the message, right-click on it and click Edit and resend. Do this as many times as you like to see how modifying the message in different ways changes the response.

Note

The option to send a message to the client is only available in connections that are still open via Burp Proxy.

WebSocket Repeater tab

For WebSocket messages, each Repeater tab contains the following items:

A message editor which contains the WebSocket message to be sent. You can use the message editor functions to analyze and edit the message.

The WebSocket connection via which the message is sent. This is set automatically when you send a message to Repeater.

To disconnect or reconnect to a WebSocket connection, use the toggle in the WebSocket ID header.

To edit a connection click on the edit icon in the WebSocket ID header. You can clone or attach to any open connection, create a new connection, or reconnect a closed connection. You can then manipulate the negotiation request used to create the WebSocket.

A history table that shows all messages that have been sent and received. Manually generated messages are indicated in the table.

To automatically select the next message that is received in the history table, check Select next message received.

A message viewer for the message that is currently selected in the history table.

You can customize and sort the table contents. For more information, see Customizing Burp's tables.
