# Proxy intercept

Source: https://portswigger.net/burp/documentation/desktop/tools/proxy/intercept-messages
Fetched: 2026-06-28T09:16:06.994299+00:00

Support Center

Documentation

Desktop editions

Tools

Burp Proxy

Proxy intercept

ProfessionalCommunity Edition

Proxy intercept

Last updated:

June 18, 2026

Read time:

3 Minutes

From the Proxy > Intercept tab, you can intercept HTTP requests and responses sent between the browser and the target server. This enables you to study how the website behaves when you interact with it.

The intercept feature enables you to perform the following useful actions:

Intercept requests and modify them before forwarding them to the server.

Release a selection of requests at once.

Send interesting requests to Burp's other tools, such as Repeater or Intruder, for further testing.

Drop one or more requests to prevent them from reaching the server.

Getting started

If you want a quick introduction to intercepting messages, you can follow the tutorials in the Getting started section:

Intercepting HTTP traffic.

Modifying HTTP traffic.

Controls

When you intercept messages, the request details are populated in the Proxy > Intercept tab. You can see details of the target server at the top of the panel. For HTTP requests you can manually edit the target server. Select the Edit target menu .

The panel contains the following controls:

Forward - After you review or edit the message, click Forward to send all the selected messages to the target.

Forward all - To send all the intercepted messages, click the Forward dropdown menu, select Forward all to update the button, then click Forward all again.

Drop - To cancel the selected requests so that they never reach the target server, click Drop.

Drop all - To drop all the intercepted messages, click the Drop dropdown menu, select Drop all to update the button, then click Drop all again.

Intercept on/off - Use this button to toggle all interception on and off:

If the button shows Intercept on, messages are intercepted. You can also configure messages to be forwarded automatically using the settings for interception of HTTP and WebSocket messages.

If the button shows Intercept off, Burp forwards all messages automatically.

You can also right-click to access different context menus in the message editor, or the list of intercepted messages.

Note

You can use hotkeys to forward or drop intercepted messages. By default, Ctrl+F forwards the selected messages. You can also set a hotkey to forward all intercepted messages.

For more information, see hotkey settings.

Intercepted messages table

The table in the top half of the panel shows you the intercepted messages. Right-click the table to access the

context menu. The available options if you only have one message selected, or multiple messages.

You can select multiple messages from the table:

Click a message to select it.

Hold Shift to select a block of messages.

Hold Command (Mac) or Ctrl (Windows or Linux) to select multiple messages one at a time.

Adding annotations

You can add notes and highlights to intercepted messages. This enables you to describe the purpose of different messages, and to flag interesting messages for further investigation.

Any annotations that you make also appear against the item in the HTTP history. If you apply an annotation to an HTTP request, the annotation appears again if the corresponding response is also intercepted.

To highlight an intercepted message, right-click the message in the table and selection Highlight. Then select a color from the list.

To add a note, right-click the message in the table and select Add Notes. Enter your comment in the Notes panel.

Message display

The message editor in the main panel shows the most recently selected intercepted message. From here you can analyze the message and perform actions on it.

Right-click the message editor to see the context menu and access the standard functions. You can also perform the following actions for HTTP messages:

Don't intercept requests/responses - You can add an interception rule so that Burp automatically forwards messages that share a specific feature, such as host, file extension, or HTTP status code. Use this feature if you're seeing a lot of uninteresting requests or responses of a particular type.

Do intercept - Select this function to intercept the response to the currently displayed request. This is only available for requests.

Protocol

You can use the Inspector to edit the protocol for the request. For more information, see the HTTP/2 documentation.
