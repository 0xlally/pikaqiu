# Search

Source: https://portswigger.net/burp/documentation/desktop/tools/search
Fetched: 2026-06-28T09:16:07.995846+00:00

Support Center

Documentation

Desktop editions

Tools

Search

Professional

Search

Last updated:

June 18, 2026

Read time:

3 Minutes

In this section

Simple text search

Find comments

Find scripts

Find references (links) to a particular URL

Text search

You can perform suite-wide searches in the search dialog. To access the search dialog, click Search on the tab bar.

You can also search within selected branches in the Target site map, by selecting Search within Engagement tools in the context menu.

The search dialog lets you configure the following options:

The expression to search for

Whether the search is case sensitive

Whether the search term is a literal string or a regular expression

Whether the search should show negative matches (i.e. items that do not contain the search expression)

Whether the search is restricted to in-scope items only

Whether the search results should dynamically update as new HTTP messages are processed by Burp tools

Which locations to search within HTTP messages (requests versus responses, headers versus body)

Which tools to search in. You can choose from Target, Repeater, Proxy, or Organizer.

When you click Go, Burp searches in all issued requests, using the options you configured. The search results are shown in a table containing the following columns:

Source - The tool the search result is located in. If the search result is in Repeater, Burp displays the

relevant Repeater tab number and history item number.

Host - The protocol and server hostname.

URL - The URL file path and query string.

Status code - The HTTP status code of the response.

Length - The length of the response in bytes.

Time requested - The time the request was made.

Note

If the search result is found in Repeater, you can quickly switch to the relevant request / response pair using the context menu. Right-click the search result in the table and select

Go to Repeater tab. Burp takes you directly to the correct history item in the tab.

You can customize and sort the table, and copy column data to your clipboard. For more information, see Customizing Burp's tables.

The preview pane shows the full request and response for the selected item, including highlighted matches for your search expression.

The context menu can be used to send requests to Burp tools and carry out other actions. For more information on the available options, see

Context menu.

Find comments and scripts

You can use these functions to search part or all of the Target site map for comments and scripts. You can start the search by selecting part or all of the site map tree, and choosing Find comments or Find scripts within Engagement tools in the site map context menu.

In the search dialog, use the Search button to perform the search (or re-perform it later). Details of the discovered items are shown in a sortable table. The preview pane shows the full request and response for the selected item, with relevant items automatically highlighted, and also extracted into their own tab.

Selecting the Dynamic update option will cause Burp to dynamically update the results as new HTTP messages are processed by Burp tools. You can use the Export button to save all of the scripts or comments to file or to the clipboard, optionally consolidating duplicated items.

Find references

You can use this function to search all of Burp's tools for HTTP responses that link to a particular item. To access the function, select an HTTP request anywhere within Burp, or any part of the Target site map, and choose Find references within Engagement tools in the context menu.

The search results window shows responses (from all Burp tools) that link to the selected item. When you view an individual search result, the response is automatically highlighted to show where the linking reference occurs.

Note that this feature treats the original URL as a prefix when searching for links, so if you select a host, you will find all references to that host; if you select a folder, you will find all references to items within that folder or deeper.
