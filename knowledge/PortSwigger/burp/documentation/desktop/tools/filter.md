# Filter settings

Source: https://portswigger.net/burp/documentation/desktop/tools/filter
Fetched: 2026-06-28T09:16:04.239097+00:00

Support Center

Documentation

Desktop editions

Tools

Filter settings

ProfessionalCommunity Edition

Filter settings

Last updated:

June 18, 2026

Read time:

2 Minutes

You can filter the messages that are shown in various Burp Suite tools. This makes it easier for you to analyze a large number of messages.

The filter bar above the table describes the current display filter. Click the filter bar to view and edit the filter settings. If the filter has a Settings mode and a Script mode, make sure that you've selected Settings mode. For more information about Script mode, see Bambdas.

Note

Most filters only control what is displayed. Items hidden by the filter aren't deleted and reappear if you reset the filter. The exception is the Burp Logger capture filter, which controls the messages that are captured in Burp Logger.

Filter settings

The table below shows common filter settings that can be found in many Burp tools:

Setting

Description

Filter by request type

Use the following options to filter requests:

Only the items that are in scope.

Only items with responses.

Only requests with parameters.

Filter by MIME type

Filter responses by their MIME type.

Filter by status code

Filter responses by their HTTP status code.

Filter by search term

Use a search term to filter responses. You have the following options:

Regex - Use a literal string or a regular expression.

Case sensitive - Make your search case-sensitive.

Negative search - Only show items that don't match the search term.

Filter by file extension

Filter items by their file extension.

Filter by annotation

Only show items with notes or highlights.

Managing the filter settings

Many filter windows include options to manage filter settings, making it easier to quickly refine and reset your changes. Where applicable, the available options are:

Click in the filter window to:

Restore defaults - Restore Burp's default filter settings.

Load settings - Load filter settings.

Save settings - Save your current filter settings.

Click to restore Burp's default filter settings.

Show all - Show all items.

Hide all - Hide all items.

Revert changes - Undo any changes you made since last applying the filter.
