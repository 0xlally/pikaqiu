# Inspector

Source: https://portswigger.net/burp/documentation/desktop/tools/inspector
Fetched: 2026-06-28T09:16:03.911437+00:00

Support Center

Documentation

Desktop editions

Tools

Inspector

ProfessionalCommunity Edition

Inspector

Last updated:

June 18, 2026

Read time:

4 Minutes

The Inspector enables you to quickly view and edit interesting features of HTTP and WebSocket messages without having to switch between different tabs. You can access the Inspector from the side panel, next to the message editor throughout Burp Suite. You can use it to:

View the fully decoded values of parameters or cookies, or a substring that you've selected in the editor.

Add, remove, and reorder items at the click of a button, so you don't have to work with the raw HTTP syntax.

Edit data in its decoded form. When you update the request, the sequence is automatically re-encoded.

Toggle the protocol used to send individual requests. Burp automatically performs the transformations to generate an equivalent request for the new protocol.

Work with HTTP headers and pseudo-headers without being tied to the message editor's HTTP/1-style syntax. This enables you to use a number of advanced techniques for HTTP/2-specific tests.

Some of these features are only available for editable requests. You can find these in Burp Repeater or intercepted requests in Burp Proxy, for example.

Note

You can add tabs to the message editor to display the same information. You can enable these in the Settings dialog. For more information see Message editor settings.

Configuring the Inspector layout

The buttons at the top of the Inspector enable you to adjust the layout of the side panel, including the Inspector:

To dock the side panel on the left or right of the screen, click or .

To expand or collapse all the Inspector widgets simultaneously, click or . The expand button only expands widgets that contain data.

In some Burp tools, you can switch between the Inspector and the Notes tool. To select the Notes tool, click Notes.

Click on the settings icon to open the Settings dialog. This enables you to adjust how widgets are displayed, and set the default layout for the side panel. For more information, see

Side panel settings.

Request attributes

The Request attributes section displays the HTTP method, the path, and the protocol that was used to send the request. For editable messages, it shows the protocol that you want to use when you send the request instead.

When you change the protocol, Burp performs the transformations to generate an equivalent request for the new protocol. This enables you to easily upgrade and downgrade individual requests.

Viewing HTTP message data in the Inspector

The Inspector displays the headers, parameters, and cookies from the request and response as a series of name-value pairs. The items are grouped by category. The number next to each category shows you how many items of each type were found.

Automatic decoding

The values shown in the Inspector are automatically decoded from HTML, URL, and Base64. This enables you to read them more easily without having to manually decode them.

In the main Inspector view, you only see the final result of the decoding. To see each decoding step that the Inspector applied, click the arrow to the right of the item.

You can use the Decoded from drop-down menus to modify the sequence of decoding steps. Use the plus and minus icons to manually add or remove more steps if necessary.

HTTP/2 headers and pseudo-headers

The Inspector displays HTTP/2 pseudo-headers alongside any ordinary headers in the request. To identify them, each pseudo-header is prefixed with a colon.

This provides an alternative way to work with HTTP/2 requests that is completely decoupled from HTTP/1 syntax. This more closely resembles the underlying request that is sent to the server. It enables you to use injections that are not possible via the message editor, to test for a number of HTTP/2-specific vulnerabilities.

For more information, see working with HTTP/2 in Burp.

Selecting a substring

If you highlight a substring in the message editor, you can view it in the Inspector. The Selection widget appears when you select one or more characters. The contents of the widget depends on your selection:

If you select an individual character, you can see its ASCII code point in either decimal or hexadecimal form.

If you select more than one character, the Inspector automatically decodes it. It displays the character count next to the category heading.

Note

The Selection widget also displays any non-printing characters, regardless of whether you've selected to show them in the message editor. If you highlight multiple lines, you'll see the \r\n characters at the end of each line, for example.

Related pages

Getting started with the Inspector.

Modifying requests using the Inspector.

Side panel settings.
