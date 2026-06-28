# Burp Organizer

Source: https://portswigger.net/burp/documentation/desktop/tools/organizer
Fetched: 2026-06-28T09:16:06.256753+00:00

Support Center

Documentation

Desktop editions

Tools

Organizer

ProfessionalCommunity Edition

Burp Organizer

Last updated:

June 18, 2026

Read time:

3 Minutes

Burp Organizer is a workspace for collecting and managing HTTP messages during application testing.

It provides a way to store and annotate interesting requests and responses without interrupting your testing workflow.

Sending messages to Organizer

You can send HTTP messages to Burp Organizer from other Burp tools by right-clicking one or more selected messages and selecting Send to Organizer. Alternatively, you can use the default hotkey

Ctrl + O

Messages appear in the Organizer inbox as read-only copies of the original request and response, including any notes and highlights.

Related pages

Annotating Organizer items.

Collections

As your testing progresses, you may want to organize messages into collections. Collections are groups of HTTP messages that you create based on how you want to organize your testing.

Messages can be moved or copied between collections (including back into the inbox), enabling you to group related messages in a way that works for you. Learn more about Collections.

Browsing messages in Organizer

Organizer displays messages from the selected collection in a table with the following columns:

# - The request index number.

Time - When the request was made.

Status - The status applied to the message.

Tool - The Burp tool that originally generated the request. This always reflects the request's origin, even if the message is later sent from Burp Logger or from within Organizer.

Method - The HTTP method.

Host - The server hostname.

Path - The URL path.

Query - The URL query string.

Param count - The number of parameters in the request.

Status code - The HTTP status code of the response.

Length - The length of the response in bytes.

Notes - Any notes added to the message.

Right-click any message in the table to access additional actions, such as adding notes, assigning workflow status, and highlighting messages. For more information, see Annotating Organizer items.

You can filter the table to narrow down which messages are shown. For more information, see Filtering Burp Organizer.

You can also sort and customize the table to suit the way you work. For more information, see Customizing Burp's tables.

Inspecting a message in Organizer

Select a message to inspect its request and response in the lower pane. Both are shown as read-only snapshots.

To search within the request or response, use the search bar below the message. For more information, see Text editor - Quick search.

Use the tabs beside the message to switch between the Inspector and Notes panels.

Exporting results

You can export Organizer items as a CSV file to easily share with others or include in your reports.

Notes

Professional You can generate a link to quickly and easily share collections with other Burp Suite Professional users. For more information, see Sharing collections.

To export all items:

Right-click the table then select Export as CSV.

If necessary, choose a directory.

Enter a filename and click Save.

To export specific items:

Select the items that you want to export.

Right-click and select Export as CSV.

If necessary, choose a directory.

Enter a filename and click Save.

When exporting items in CSV format, Burp represents data as follows:

Date times are formatted as: yyyy-MMM-dd HH:mm:ss.SSS.

DNS queries and HTTP interactions (including requests and responses) are represented as Base64 encoded strings.

Any data that contains a comma is escaped by wrapping the data in double quotes. For example, a,b will become "a,b".

Any data containing double quotes is escaped by an additional double quote. For example, "a" will become """a""".

Any data starting with -, +, = or @ is escaped for Excel by prefixing a single quote (').

You can also export and import Organizer items as part of a project file. For more information, see Project

files.
