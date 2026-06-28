# Configuring the Burp Logger capture filter

Source: https://portswigger.net/burp/documentation/desktop/tools/logger/filter/capture
Fetched: 2026-06-28T09:16:05.867469+00:00

Support Center

Documentation

Desktop editions

Tools

Logger

Filtering Logger

Capture filter

ProfessionalCommunity Edition

Configuring the Burp Logger capture filter

Last updated:

June 18, 2026

Read time:

2 Minutes

You can use the capture filter settings to control which types of items are captured in Burp Logger.

You can configure the Logger capture filter in two different ways:

Settings mode - Configure a capture filter using checkboxes and drop-downs.

Script mode - Apply a powerful custom capture filter using Burp's Java-based scripts.

Note

Items that are not captured will be discarded from Logger. Burp can't retrieve these items even if the capture filter is removed.

To filter the items that Logger captures, click on the Capture filter bar in the Logger tab.

This opens the Logger capture filter window.

Settings mode

On the Settings mode tab, you can apply a capture filter using the following options:

Capture limit

You can specify a limit to the memory used by Logger.

Once the limit is reached, Logger discards the oldest entries as new entries are created.

The default limit is 50MB (or 100MB, if you give Burp Suite access to at least 1GB of memory).

To change the capture limit, select a preset option from the drop-down, or type a specific value.

Note

Allocating a large amount of memory to Logger can cause performance issues.

We recommend that you only increase the amount of memory when you have a specific issue that requires a large number of entries.

Capture by request type

Choose which request types Logger captures. You can select from:

Capture only in-scope items. For more information on how to set your scope, see Target scope.

Discard items without responses.

Capture only parameterized requests.

Capture by MIME type

Choose which MIME type Logger captures, such as HTML or XML.

Capture by status code

Choose which status codes Logger captures.

Capture by tool

Choose which other Burp tools Logger captures items from.

This enables you to discard traffic from a noisy tool, or direct Logger to capture traffic from one tool only.

By default, all tools are selected.

Capture by search term

Professional Choose to capture only records that contain a specific search term:

Regex. Specify whether the search term is a literal string or a regular expression.

Case sensitive. Specify whether the search term is case-sensitive.

Negative search. Capture only items that do not match the search term.

Session handling

Choose whether or not to discard session handling requests.

Limit request/response size

Limit the size of requests or responses that Logger captures. The default maximum size for items is 1MB.

To change the maximum size of items Logger captures, select a preset option from the drop-down.

Script mode

On the Script mode tab, you can apply Java-based scripts to create custom capture filters for Logger. For more information, see

Configuring the Logger capture filter with scripts.
