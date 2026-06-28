# Working with Burp Logger entries

Source: https://portswigger.net/burp/documentation/desktop/tools/logger/entries
Fetched: 2026-06-28T09:16:05.523577+00:00

Support Center

Documentation

Desktop editions

Tools

Logger

Working with Logger entries

ProfessionalCommunity Edition

Working with Burp Logger entries

Last updated:

June 18, 2026

Read time:

2 Minutes

All HTTP traffic is recorded in the Logger tab, up to a specified limit of allocated memory.

To disable or enable the logging of all items, click the Logging: On/Off button. You can also clear the log: click the Clear log trash icon . Once cleared, the log cannot be retrieved.

Burp Logger has a range of functions to help you view and analyze a large number of results.

Managing log entries

You can sort and customize the table, and copy column data to your clipboard. For more information, see Customizing

Burp's tables.

Adding custom columns

Professional You can create your own custom columns using scripts.

Custom columns enable you to see more detail about the items that have been logged for a more focused analysis. For more information, see Adding custom columns in Burp Logger.

Viewing requests and responses

You can view the request and response for each entry in the message editor and Inspector. Click on an entry to view these. They are read-only.

You can customize and sort the table contents. For more information, see Customizing Burp's tables.

Filtering log entries

You can choose which types of items Logger captures and displays. This enables you to focus your work on interesting messages, and control how much memory Logger uses.

You can set filters using predefined options, or create advanced filters using scripts.

For more information, see Filtering Burp Logger.

Annotating log entries

You can annotate log entries for later attention:

To highlight an entry, click in the # column and choose a color from the drop-down menu.

To leave a comment on an entry, double-click on the Comment column.

Logger workflow tools

You can use the context menu to perform further actions on any log entry as part of your workflow. For example, you can send requests to other Burp tools, such as

Organizer and Intruder. For more information on the available options, see

Context menu.

Export log entries as CSV

To export log entries as a CSV file, select the relevant entries in the table, right-click and select Export as CSV. The whole table is exported if you select zero entries or one entry.

When exporting entries in CSV format, Logger encodes certain data as follows:

Date times are represented in ISO 8601 format with UTC offset: yyyy-MM-dd'T'HH:mm:ss.SSS'Z'.

Binary data (for example, HTTP/2 requests and responses) are represented as Base64 encoded strings.

Any data that contains a comma is escaped by wrapping the data in double quotes. For example, a,b will become "a,b".

Any data containing double quotes is escaped by an additional double quote. For example, "a" will become """a""".

Any data starting with -, +, = or @ is escaped for Excel by prefixing a single quote (').
