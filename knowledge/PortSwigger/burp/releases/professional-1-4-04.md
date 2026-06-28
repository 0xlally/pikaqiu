# Professional 1.4.04

Source: https://portswigger.net/burp/releases/professional-1-4-04
Fetched: 2026-06-28T09:16:23.705359+00:00

This release contains a large number of new features, usability tweaks and bug fixes. The more interesting items are listed below.

HTTP message viewer

The inline text conversion operations that are accessible via the context menu now also work on non-editable HTTP messages. The result of the conversion is shown in a pop-up dialog.

The HTTP params view now automatically URL-decodes relevant parameter names and values when these are displayed in the table. If you edit a URL-encoded value, this reverts to the raw encoded value while you are editing. Further, if you enter any parameter delimiters in raw form (space, ampersand or equals), these are automatically URL-encoded when you complete your edit.

Cut / copy / paste operations within the message editor are now integrated with the Linux selection buffer, as well as the system clipboard. Selecting text within a message automatically copies this to the selection buffer, and clicking the middle mouse button pastes from the selection buffer.

The lower search bar now has an option (accessible via the + button at the bottom left) to automatically scroll to the first search match when a new message is displayed. This feature is useful when you are stepping through a series of responses (e.g. in the proxy history) and need to view the matched expression within each response.

Clicking on the "N matches" caption on the lower search bar now selects the next matched item, in the same way as the > button does.

The maximum size of the mouse-over pop-ups for decoded syntax has been reduced, to avoid huge popups when the mouse is hovered over large encoded items (e.g. ViewStates).

Search / filters

A "negative" search option has been added to the suite-wide and in-filter search functions. This causes the search to return all items that do not match the specified expression. This can be useful to filter out responses containing a common error message, etc.

The filter bars on the Proxy history etc. now have buttons to show all items, show no items, and restore defaults.

Regex expressions in the search functions and elsewhere now allow the dot to match line terminator characters. So, for example, you can search for expressions spanning two lines using "foo.*?bar".

Proxy

There are new options to disable the web interface (at http://burp) and to suppress Burp error messages in responses. These options can be useful to mask the presence of Burp from users who connect via it.

Scanner

The active scan queue context menu now has new options to delete selected items, delete finished items, and automatically delete items as they finish.

The active scan wizard window is now resizable, to make it easier to select which items you wish to scan from a long list.

Double-clicking the active scan queue status bar now toggles the scanner between the paused/running state.

The passive check on SSL certificates now correctly handles the x.509v3 extension for alternative subject names.

Intruder

When using null payloads, you can now start an attack without needing to define a payload position.

When saving or copying the table of attack results, Burp now provides an alert if it was not possible to include full payload values. You can use the "store full payloads" option to ensure these are available in the results.

Spider

There is a new option to limit the number of parameterised requests that are made to each unique URL. This option is useful, for example, when crawling calendar applications, where each page links to the next using a different parameter value, creating an unlimited crawling space.

Repeater

The context menu now has a "paste URL as request" item. This configures Repeater to make a GET request using the URL on the clipboard. The headers included within this request are taken from the request headers defined in the Spider options.

The context menu now has an "add to site map" item, to facilitate manual content mapping.

Misc

The function to automatically save Burp's state now shows an alert on startup if the configured backup directory is not available. If backup on exit fails, Burp now shows a blocking dialog, allowing the user to cancel and not exit.

When exporting HTTP items and scanner issues in XML format, there is a default-on option to Base64-encode all request and response data. This avoids problems with binary characters within XML. If this option is used, Burp reverts to v1.0 of XML, which is more widely supported by parsers. The XML DTD now includes a "base64" attribute on the request and response elements, indicating whether the contents of those elements is Base64-encoded.

There is a new option to drop all out-of-scope requests. Using this option prevents Burp from issuing any requests to out-of-scope URLs, even if they are requested via the Proxy, Repeater etc. You can use this option based on the defined suite-wide scope or on a custom scope. You can find the new feature at options / connections / drop all out-of-scope requests.

There is a new wizard (accessed from the about menu) to clean up Burp's footprint on the local computer. Optionally, you can remove temporary files, saved preferences, your license key, and the Burp program executable.

Multi-row deletion now works on the lists of scope rules and comparer items.

Extender

There is a new method in IBurpExtenderCallbacks to send an HTTP request to Intruder with custom payload positions defined.

There are new methods in IHttpRequestResponse to get/set highlights on relevant items.

The IHttpRequestResponse object passed to IBurpExtender.processHttpMessage() by the Proxy now properly handles comments (and highlights) and links these to the corresponding item in the Proxy history.

The APIs for the new Burp Extender methods are shown below.

In IBurpExtenderCallbacks:

/**

* This method can be used to send an HTTP request to the Burp Intruder

* tool. The request will be displayed in the user interface, and markers

* for attack payloads will be placed into the specified locations within

* the request.

*

* @param host The hostname of the remote HTTP server.

* @param port The port of the remote HTTP server.

* @param useHttps Flags whether the protocol is HTTPS or HTTP.

* @param request The full HTTP request.

* @param payloadPositionOffsets A list of index pairs representing the

* payload positions to be used. Each item in the list must be an int[2]

* array containing the start and end offset for the payload position.

* @throws java.lang.Exception

*/

public void sendToIntruder(

String host,

int port,

boolean useHttps,

byte[] request,

List payloadPositionOffsets) throws Exception;

In IHttpRequestResponse:

/**

* Returns the user-annotated highlight for this item, if applicable.

*

* @return The highlight color for this item, or null if none is set.

*/

String getHighlight() throws Exception;

/**

* Sets the user-annotated highlight for this item.

*

* @param color The highlight color to be assigned to this item. Accepted

* values are: red, orange, yellow, green, cyan, blue, pink, magenta, gray.

* @throws Exception

*/

void setHighlight(String color) throws Exception;
