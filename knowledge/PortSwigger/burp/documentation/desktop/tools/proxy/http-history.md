# HTTP history

Source: https://portswigger.net/burp/documentation/desktop/tools/proxy/http-history
Fetched: 2026-06-28T09:16:06.630595+00:00

Support Center

Documentation

Desktop editions

Tools

Burp Proxy

HTTP history

ProfessionalCommunity Edition

HTTP history

Last updated:

June 18, 2026

Read time:

3 Minutes

You can use the HTTP history to see a record of the HTTP traffic that has passed through Burp Proxy. You can also see any modifications that you made to intercepted messages.

The HTTP history contains the following information:

# - The request index number.

Host - The protocol and server hostname.

Method - The HTTP method.

URL - The URL file path and query string.

Params - Flag whether the request contains any parameters.

Edited - Flag whether the request or response were modified by the user.

Status code - The HTTP status code of the response.

Length - The length of the response in bytes.

MIME type - The MIME type of the response.

Extension - The URL file extension.

Title - The page title (for HTML responses).

Notes - Any user-applied note.

TLS - Flag whether TLS is used.

IP - The IP address of the destination server.

Cookies - Any cookies that were set in the response.

Time - The time the request was made.

Listener port - The listener port on which the request was received.

Start response timer - The time in milliseconds from when the request was sent until the first byte of the response is received.

End response timer - The time in milliseconds from when the request was sent until the complete response was received.

The HTTP history is always updated, even if Intercept is off. This enables you to browse without interruption while you monitor key details about application traffic.

Right-click any item in the table to access further options, such as sending requests to other Burp tools. For more information on the available options, see

Context menu.

Managing the HTTP history

You can manage the HTTP history in the following ways:

Manage the table - Sort and customize the table, and copy column data to your clipboard. For more information, see Customizing Burp's tables.

Filter the data - Click the Filter settings bar, then choose from the following:

Settings mode - Use predefined checkboxes and fields to set your criteria. For more information, see Filtering the HTTP history.

Script mode - Apply a Java-based script to define your custom filter. For more information, see Filtering the HTTP history with scripts.

Search the data - Enter a search term in the Search box to find matching items across all columns. The search applies to the underlying data, regardless of any filters you have applied.

Toggle the filter - Click Filter on or Filter off to enable or disable both the filter and the search bar. This enables you to compare filtered and unfiltered traffic without resetting your filter or search term.

Professional Add custom columns - Click the options menu > Add custom column to create a personalized column that displays the data you want to see. For more information, see Adding custom columns to the HTTP history.

Viewing a request

If you select an item from the HTTP history, the lower pane shows the request and response messages for the item. Any modified messages are shown separately. The message may have been modified through:

User interception.

Automatic response modification.

Match and replace rules.

In addition to the main history view, you can also:

Double-click an item to open it in a pop-up window.

Right-click a request and select Show new history window to open a new history window with its own display filter.

Access the Inspector, to easily view and edit interesting items.

View and edit your notes. To do this, click Notes.

Related pages

Filtering the HTTP history

Filtering the HTTP history with scripts
