# Message editor settings

Source: https://portswigger.net/burp/documentation/desktop/settings/ui/message-editor
Fetched: 2026-06-28T09:15:57.415287+00:00

Support Center

Documentation

Desktop editions

Settings

UI

Message editor

ProfessionalCommunity Edition

Message editor settings

Last updated:

June 18, 2026

Read time:

4 Minutes

The Message editor settings page is located under User interface in the Settings dialog.

You can edit how the message editor is displayed:

Message editor request views.

Message editor response views.

HTTP message display.

Character sets.

HTML rendering.

HTTP message search.

Hide request headers.

Hide response headers.

The Message editor settings are user settings. They apply to all installations of Burp on your machine.

Message editor request and response views

The Message editor request views and Message editor response views settings enable you to adjust the views of the message content in the message editor. Each view is displayed in an individual tab, and provides the same functionality as the widgets in the Inspector.

For each view option, you can:

Show - Enable this setting to display the view in a message editor tab. By default the Pretty, Raw, Hex, and Render view tabs are displayed.

Wrap text - Enable this setting to wrap the text inside the message editor.

To reorder the list of views, use the Up and Down buttons.

Note

In read-only contexts, such as the proxy history, the message editor only displays the selected views if the message contains appropriate content. For example, you won't see the Cookies tab unless the request contains one or more cookies.

In editable contexts, such as in Burp Repeater, the message editor displays all views. This gives you the option to add items even if none were included in the original request.

HTTP message display

These settings enable you to control how HTTP messages are displayed within the HTTP message editor. You can configure the following:

Font - Select the font style and size you want to use. You can also enable font smoothing.

Highlight request syntax - Enable this setting to color-code request syntax. This includes any JavaScript, JSON, and CSS content.

Highlight response syntax - Enable this setting to color-code response syntax. This includes any JavaScript, JSON, and CSS content.

Pretty print by default - Enable this setting to automatically prettify data, markup, and code. Burp adds standardized line breaks and indentation to unformatted text. Pretty printing is supported for JSON, XML, HTML, CSS, and JavaScript.

Hide decoded text on hover - Select this setting to disable the tooltips that display decoded text when you hover over encoded values in the message editor.

Related pages

For more information on pretty printing, see Text editor.

For more information on the message editor, see Burp Suite message editor.

Character sets

These settings control how Burp handles character sets when it displays raw HTTP messages. The available settings are:

Recognize automatically based on message headers - By default, Burp automatically recognizes the character set of each message, based on the message headers. This enables you to work concurrently on messages that use different character sets.

Use the platform default - Select this option to use the default UTF-8 character set for all messages.

Display as raw bytes - Select this option to display the messages as raw bytes (using ASCII encoding), without processing any extended characters.

Use a specific character set - Choose a character set from the drop-down list. This character set is used with all messages.

HTTP headers are always displayed in raw form. The charset encoding options only apply to the message body.

Note

Some of the glyphs required for certain character sets are not supported by all fonts. If you need to use an extended or unusual character set, you should first try a system font such as Courier New or Dialog.

HTML rendering

The Render view within the HTTP message editor displays HTML content approximately as it would appear in your browser. This setting controls whether Burp can make additional HTTP requests to fully render HTML content (for example, to display embedded images).

Select this setting to increase the quality of Burp's HTML rendering at the expense of some speed. This setting increases the overall number of requests that Burp makes to the target application.

Related pages

Burp Suite message editor.

HTTP message search

The HTTP Message search settings control the search bar at the bottom of the message editor window. By default, none of these settings are enabled:

Case sensitive - Choose whether the search is case-sensitive.

Regex - Specify whether the search term is a regular expression or a literal string.

Auto-scroll to match when text changes - Specify whether the text editor automatically scrolls to the first highlighted match when new text is displayed. This is useful if you want to step through items in the Proxy history, to look for a particular expression in the responses.

Hide request headers

Use this setting to hide specified request HTTP headers in the Pretty tab of the message editor by default. This enables you to reduce clutter, helping you focus on more valuable information.

To automatically hide request HTTP headers across Burp, select Hide the following headers by default. Burp hides the defined list of headers. You can customize this list in the following ways:

Add - Enter a new HTTP header name.

Remove - Delete the selected HTTP header.

Clear - Delete all HTTP headers from the list.

Hide response headers

Use this setting to hide specified response HTTP headers in the Pretty tab of the message editor by default. This enables you to reduce clutter, helping you focus on more valuable information.

To automatically hide response HTTP headers across Burp, select Hide the following headers by default. Burp hides the defined list of headers. You can customize this list in the following ways:

Add - Enter a new HTTP header name.

Remove - Delete the selected HTTP header.

Clear - Delete all HTTP headers from the list.
