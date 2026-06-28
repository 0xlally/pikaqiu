# Configuring the Burp Logger view filter

Source: https://portswigger.net/burp/documentation/desktop/tools/logger/filter/view
Fetched: 2026-06-28T09:16:05.939349+00:00

Support Center

Documentation

Desktop editions

Tools

Logger

Filtering Logger

View filter

ProfessionalCommunity Edition

Configuring the Burp Logger view filter

Last updated:

June 18, 2026

Read time:

2 Minutes

You can use the view filter to control which captured items Burp Logger displays.

For more information on which items Logger captures, see Configuring the Burp Logger capture filter.

Items that are not displayed because of view filter settings can be accessed by removing the view filter.

You can configure the Logger view filter in two different ways:

Settings mode - Configure a view filter using checkboxes and drop-downs.

Script mode - Apply a powerful custom view filter using Burp's Java-based scripts.

To filter which of the captured items are displayed, click on the View filter bar. This opens the Logger view filter window.

The View filter bar only appears when there is one or more items recorded in Logger.

Settings mode

On the Settings mode tab, you can apply a view filter using the following options:

Filter by request type

Choose which request types Logger displays. You can select from:

Show only in-scope items. For more information on how to set your scope, see Target scope.

Hide items without responses.

Show only parameterized requests.

Filter by MIME type

Choose which MIME type Logger displays, such as HTML or XML.

Filter by status code

Choose which status codes Logger displays.

Filter by tool

Choose which Burp tools Logger displays items from. This enables you to ignore traffic from a noisy tool, or direct Logger to display traffic from one tool only.

By default, all tools are selected.

Filter by search term

Professional

Choose to display only records that contain a specific search term:

Regex. Specify whether the search term is a literal string or a regular expression.

Case sensitive. Specify whether the search term is case-sensitive.

Negative search. Display only items that do not match the search term.

Filter by file extension

Choose which types of file Logger displays, such as PHP or CSS.

Filter by annotation

Choose whether to show only items that have been annotated, either by a comment or highlight. To learn how to annotate items, see Working with Burp Logger entries.

Script mode

On the Script mode tab, you can apply Java-based scripts to create custom view filters for Logger. For more information, see

Configuring the Logger view filter with scripts.
