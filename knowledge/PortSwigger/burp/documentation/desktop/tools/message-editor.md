# Burp Suite message editor

Source: https://portswigger.net/burp/documentation/desktop/tools/message-editor
Fetched: 2026-06-28T09:16:05.897780+00:00

Support Center

Documentation

Desktop editions

Tools

Message editor

ProfessionalCommunity Edition

Burp Suite message editor

Last updated:

June 18, 2026

Read time:

10 Minutes

You can view HTTP and WebSocket messages in various places throughout Burp Suite. Wherever you can see messages, Burp provides a number of functions to help you quickly analyze them. This drives Burp's core workflow, and helps you to carry out other useful tasks.

In some of Burp's tools, such as Burp Repeater and Burp Intruder, you can also edit the HTTP and WebSocket messages and resend them.

The message editor primarily consists of the following panels:

The text editor, which contains the messages. This is read-only in certain tools.

The side panel, including the Inspector. The Inspector provides quick access to key details of HTTP messages and WebSockets, and allows you to perform some basic operations without having to switch to the Decoder tab. In Burp Organizer, the side panel includes an Inspector and Notes tab. You can switch between them as required.

For an introduction to the Inspector, refer to Getting started with the Inspector.

In the upper-right corner of the message editor, there are three icons that adjust the screen layout. You can choose from the following options:

Horizontal layout - The request and response are arranged side-by-side.

Vertical layout - The request and response are stacked one on top of the other.

Combined view - Either the request or response fills the message editor pane. You can use the tabs to alternate between the two.

Message analysis toolbar

At the top of each request or response is the message analysis toolbar. This provides different tabs that show alternative views of the message content and provide some additional features for performing common operations.

By default, the Pretty, Raw, Hex, and Render tabs are displayed, but you can remove or reorder the tabs, and add some extra ones from the settings menu.

Raw tab

In this tab, the text editor displays the full message in its raw form. The text editor includes various useful functions including syntax analysis, hotkeys, and text search. You can use the \n button to toggle whether non-printing characters are displayed

In some of Burp's tools, such as Burp Repeater, you can also make changes to requests directly in the text editor.

You can access a wide range of context-specific actions for both requests and responses either from the Actions menu or by right-clicking anywhere on the relevant message. By selecting one or more characters in a message, you can also work with specific values in the Inspector.

Pretty tab

In this tab, you can access all the same functionality as in the Raw tab. The key difference is that the text editor's pretty printing feature is enabled. This improves the readability of data, markup, and code in HTTP messages by displaying them with standardized indentation and line breaks.

In editable messages, supported text formats are dynamically prettified as you type wherever possible. Otherwise, the text is prettified when you send the request.

Note

This tab is only available if the message contains content in one of the supported formats.

Hex tab

This tab displays messages in raw form in a hexadecimal editor. It shows messages arranged into lines of 16 bytes, and displays the hex value of each byte. You can edit messages in the hex tab. Any values that you insert can be given as characters or in two-digit hexadecimal form, from 00 through FF.

Any selected bytes appear in the Inspector. You can edit individual bytes directly in the Inspector or by double-clicking values in the table. You can select rows of bytes by clicking the row number, and view the selection in the Inspector.

The hex tab is useful when you want to:

View or edit the code point for individual characters.

View or insert non-printing characters.

Insert or delete individual bytes or strings.

The context menu for this tab has the following items:

Insert byte: This inserts a single new byte before the selected byte.

Insert bytes: This inserts the requested number of new bytes before the selected byte.

Insert string: This inserts the specified string before the selected byte.

Delete selected byte: This deletes the selected byte.

Delete selected bytes: This deletes the selected bytes.

Render tab

This tab applies to HTTP responses containing HTML or image content. It attempts to render the contents of the message body in the form it would appear when displayed in a browser.

GraphQL tab

This tab appears when Burp detects a GraphQL query. It separates the GraphQL query from the rest of the request, and formats it in a way that makes

it easy to view and edit the query structure (displayed in the Query panel) and its associated variables (displayed in the Variables panel).

Additional tabs

You can also choose to add the following tabs to the message editor:

Headers.

Query params.

Body params.

Cookies.

Attributes.

These tabs provide the same functionality as the widgets in the Inspector. For more information, see Inspector.

To add tabs to the message editor, click the settings icon in the upper-right corner of the side panel. For more information, see

Message editor settings.

Extension-specific tabs

Some Burp extensions provide additional tabs for the message editor.

Actions menu

The Actions menu provides quick access to the full range of context-specific actions that are available for the current request.

Other ways of using the message editor

You can do the following things with the message editor:

Toggle whether non-printing characters are displayed directly in the normal HTTP message editor tabs. To do this, press the \n button in the message editor toolbar.

To view the code point for a character, select a character, either printing or non-printing, in the HTTP message. An entry will appear in the Inspector that indicates the decimal and hex code points for the character. In editable contexts, such as a request in Burp Repeater, you can edit this value to overwrite the selected character.

Insert a non-printing character, such as a null byte, carriage return, or newline character, by editing the code point of an existing byte using the Inspector.

Insert a CLRF by placing the cursor in the appropriate position in the request and press the Enter / Return key.

To insert a byte, place the cursor in the desired position in the request and enter an arbitrary placeholder character. Edit its code point accordingly using the Inspector.

To delete a byte, delete the corresponding character directly in the request. To delete non-printing characters, we recommend using the \n button to display them first.

Note

Instead of using the Inspector to edit code points for a character, some users may find it quicker to URL-encode a selection and edit the relevant hex codes in-line before decoding the selection back to its original form. This is particularly effective if you use the corresponding hotkeys.

HTTP/2 messages in the message editor

The message editor displays a representation of HTTP/2 messages using HTTP/1 syntax, essentially showing you what the equivalent HTTP/1 request would look like. Whenever you make changes, Burp automatically converts these to their HTTP/2 equivalent behind the scenes and updates the underlying HTTP/2 request. In many cases the protocol you use is irrelevant, this enables you to use the message editor with HTTP/2 as normal.

As this HTTP/1-style view is bound by the limitations of HTTP/1 syntax and requires some lightweight normalization to ensure that a valid HTTP/2 request is produced, it may not be suitable to test for protocol-level issues that are exclusive to HTTP/2. In this case, we recommend you use the Inspector to work with HTTP/2.

For more detailed information, please refer to the HTTP/2 documentation.

HTTP/0.9 responses in the message editor

HTTP/0.9 responses consist only of a body with no headers. Because the message editor expects a standard header block, Burp adds the following status line:

HTTP/0.9 1337 No response headers received

This makes the response visible in the message editor, while indicating that no headers were returned by the server. You can use the string 1337 to help filter these responses.

Context-specific actions

Right-click a request or response to access the context menu. The available actions depend on the message type. These are described below.

Note

The menu may also include additional items that are specific to the tool in which the editor appears. For example, in Repeater, the context menu has options to paste a URL as a request and add the current item to the site map.

Scan / send to ...

You can send any message, or a selected portion of the message, to other Burp tools. The ability to send requests between tools forms the core of Burp's user-driven workflow.

Show response in browser

You can render the selected response in Burp's browser, to avoid the limitations of Burp's built-in HTML renderer. When you select this option, Burp gives you a unique URL that you can paste into Burp's browser, to render the response. The resulting browser request is served by Burp with the exact response that you selected (the request is not forwarded to the original web server), and yet the response is processed by the browser in the context of the originally requested URL. This means that relative links within the response are handled properly by the browser. As a result, the browser may make additional requests in the course of rendering the response, for images or CSS, for example. These are handled by Burp in the usual way.

Record an issue

Professional Manually record an issue for the selected request / response pair:

Create an issue - Add a new issue.

Add to manually created issue - Add a request / response pair to a pre-existing manually created issue.

The issue is saved to your project and can be included when you generate a report.

For more information, see Manually creating issues for reports.

Request in browser

You can re-issue the selected request in Burp's browser. The following sub-options are available:

In original session - Burp issues the request using the exact Cookie header that appeared in the original request.

In current browser session - Burp issues the request using the cookies supplied by Burp's browser.

You can use the In current browser session option to test access controls:

Select requests within Burp that were generated within one user context. An administrator, for example.

Log in with a different user context. An ordinary user, for example.

Reissue the requests.

When you work with complex, multi-stage processes, this method is normally a lot easier than repeating a multi-stage process over and over, and modifying cookies manually using the Proxy.

Save OpenAPI requests to site map

If Burp identifies an OpenAPI definition in a response, you can save the derived requests to the site map.

GraphQL

If Burp identifies any GraphQL queries, you will see the GraphQL context menu. For more information, see Working

with GraphQL in Burp Suite.

Engagement tools

Professional

This submenu contains useful functions to perform engagement-related tasks. For more information, see the Engagement tools section.

Change request method

For requests, you can automatically switch the request method between GET and POST, with all relevant request parameters suitably relocated within the request. Use this option to quickly test the application's tolerance of parameter location. For example, to bypass input filters, or fine-tune a cross-site scripting attack.

Change body encoding

You can change the encoding of any request body. Choose from the following options:

Toggle body encoding - Switch between the two most recently used encodings in the current Repeater

tab.

Form URL-encoded

Multipart

JSON

Copy URL

This function copies the full current URL to the clipboard.

Copy as curl command

This function copies to the clipboard a curl command that can be used to generate the current request.

Copy to file

This function allows you to select a file and copy the contents of the current message to the file. This is handy for binary content, when copying via the clipboard may cause problems. Copying operates on the selected text or, if nothing is selected, the whole message.

Paste from file

This function allows you to select a file and paste the contents of the file into the message. This is handy for binary content, when pasting via the clipboard may cause problems. Pasting replaces the selected text or, if nothing is selected, inserts at the cursor position.

Save item

This function lets you specify a file to save the selected request and response in XML format, including all relevant metadata such as response length, HTTP status code and MIME type.

Convert selection

This applies to the Raw view only. The submenu items enable you to perform quick encoding or decoding of the selected text in a variety of schemes. If the message is editable, then the conversion is performed in-place to the selected text. If the message is not editable, then the result of the conversion is shown in a dialog. The following types of conversion are available:

URL - These options perform URL encoding or decoding. You can optionally encode just key HTTP metacharacters, or all characters, or all characters using 2-byte Unicode-encoding (e.g. %u0041 for A).

HTML - These options perform HTML encoding or decoding. You can optionally encode just key HTML metacharacters, or all characters, or all characters using numeric entities (e.g. &#65; for A), or all characters using hex entities (e.g. &#x41; for A).

Base64 - These options perform Base64 encoding or decoding.

Base64 URL - These options perform Base64 URL encoding or decoding.

Construct string - These options generate code in various interpreted languages to dynamically construct the selected string. It can be useful for delivering certain attacks like SQL injection, where it is necessary to dynamically build a string to evade input filters. The available options are JavaScript, and SQL on the Microsoft, Oracle and MySQL platforms.

URL-encode as you type

This applies to the Raw view only. If this option is turned on then characters like & and = are automatically replaced with their URL-encoded equivalents as you type.

Sharing messages in collections

Professional

You can share requests and responses from the message editor by adding them to a collection in Burp Organizer. Collections let you group related messages together and share them securely with other Burp users.

Related pages

Burp Organizer

Collections
