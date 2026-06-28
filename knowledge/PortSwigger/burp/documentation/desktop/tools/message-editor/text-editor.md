# Text editor

Source: https://portswigger.net/burp/documentation/desktop/tools/message-editor/text-editor
Fetched: 2026-06-28T09:16:05.892525+00:00

Support Center

Documentation

Desktop editions

Tools

Message editor

Text editor

ProfessionalCommunity Edition

Text editor

Last updated:

June 18, 2026

Read time:

4 Minutes

The HTTP message editor uses the text editor to display the content of requests and responses. The text editor is also used elsewhere within Burp to display any plain text.

It provides a number of useful features to make it easier to read different kinds of text and help you to analyze the content.

Syntax analysis

Syntax in HTTP requests and responses is automatically colorized to highlight interesting items, such as parameters in requests and HTML elements in responses. JavaScript, JSON, and CSS content is also fully colorized. You can configure this behavior, and adjust the font, in the message display settings.

When syntax colorizing is enabled, the editor also displays mouse-over popups that show the decoded values of syntax items where appropriate. For HTTP requests, the popups perform URL-decoding, and for responses they perform HTML-decoding.

Pretty printing

In the Pretty tab, supported text formats are automatically prettified in the text editor. The editor currently supports pretty printing of the following formats:

JSON.

XML (including image/svg+xml content).

HTML.

CSS.

JavaScript.

This improves the readability of data, markup, and code in HTTP messages, which are displayed with standardized indentation and line breaks. In editable messages, such as in Burp Repeater, supported text formats are dynamically prettified as you type. Otherwise, the text is prettified when you send the request.

By default, messages are displayed in the Pretty tab whenever Burp detects a supported format in the content. To manually alternate between the prettified version and the raw content, use the tabs in the message editor.

You can disable pretty printing by default in the Settings dialog. Click on the settings icon to open the dialog. For more information, see Message editor settings.

Hide headers

In the Pretty tab, you have the option to hide HTTP headers that typically don't offer much insight into the target application's behavior, or that contain information that can't be exploited. This enables you to reduce clutter, helping you focus on more valuable information.

Toggle whether these HTTP headers are visible using the eye button above each message. Burp hides the headers specified in the

Hide request headers or Hide response headers list. You can edit these lists in the

Settings dialog, under User interface > Message editor.

Related pages

For more information, see the following pages:

Message editor settings - Hide request headers.

Message editor settings - Hide response headers.

Line-wrapping

In both the Pretty and Raw tabs, lines in requests and responses are automatically wrapped to fit the width of the text editor. This makes it easier to read long, single-line header values, for example.

Line numbers are displayed so that you can still keep track of the original line breaks.

To toggle line-wrapping on and off, use the button above each message.

Non-printing characters

By default, non-printing characters in HTTP requests and responses are hidden. To display them, click . This is supported for any bytes with a hexadecimal code point lower than 20, which includes tabs, line feeds, carriage returns, and null bytes. Characters with code points from 7F to FF are also supported.

This feature can help you to:

Spot subtle differences between byte values in responses.

Experiment with HTTP request smuggling vulnerabilities.

Study line endings to identify potential HTTP header injection vulnerabilities.

Observe how null-byte injections are handled by the server.

Text editor hotkeys

The text editor supports hotkeys for common actions. You can configure the hotkeys in the hotkey settings. The default hotkeys for the text editor are:

Ctrl + A, select all.

Ctrl + X, cut selected text.

Ctrl + C, copy selected text.

Ctrl + V, paste.

Ctrl + S, find and highlight the selected text throughout the message.

Ctrl + Z, undo last edit.

Ctrl + Y, redo last undone edit.

Ctrl + U, URL-encode selected text (hold down Shift to decode).

Ctrl + H, HTML-encode selected text (hold down Shift to decode).

Ctrl + B, Base64-encode selected text (hold down Shift to decode).

Ctrl + left, move to previous word.

Ctrl + right, move to next word.

Ctrl + up, move to previous paragraph.

Ctrl + down, move to next paragraph.

Ctrl + home, go to start of message.

Ctrl + end, go to end of message.

Ctrl + backspace, delete previous word.

Ctrl + del, delete next word.

Quick search

Use the search bar at the bottom of the text editor to quickly find expressions in the text. As you type into the search box, the editor automatically highlights matching items. You can use the arrow buttons and to move the selection to the previous or next match.

You can control the configuration of the search in the Settings dialog. For more information, see Message editor settings.
