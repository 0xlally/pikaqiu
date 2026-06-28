# Report settings

Source: https://portswigger.net/burp/documentation/desktop/running-scans/reporting/report-settings
Fetched: 2026-06-28T09:15:52.981012+00:00

Support Center

Documentation

Desktop editions

Running scans

Reporting scan results

Report settings

Professional

Report settings

Last updated:

June 18, 2026

Read time:

3 Minutes

You can use the reporting wizard to customize the format and content of your report.

Report format

You can generate a report in HTML format. This is the best choice if you want to print your report, or view it in a browser. You can also export issue data in XML format. This is useful if you want to import information about issues into other tools or reporting frameworks.

If you export issue data, you can choose to Base64-encode HTTP requests and responses within the XML output. This is useful because HTTP messages may contain nonprinting characters that are not permitted in XML documents, even in CDATA blocks. If you Base64-encode HTTP requests, you can make sure that your report is compatible with strict XML parsers.

Note

The XML file includes an internal Document Type Definition (DTD), which defines its structure and attributes. If you are an author of interoperability code, you can export issue data for any chosen issue, and view the XML file to see the DTD.

XML elements

The report uses the following XML elements:

The serialNumber element contains a long integer that is unique to that individual issue instance. If you export a list of current issues several times from the same instance of Burp, you can use the serial number to identify incrementally new issues.

The type element contains an integer that uniquely identifies the issue type, such as SQL injection, or XSS. This value is constant across different instances of Burp. See the list of scan issue types for a list of all numeric type identifiers.

The name element contains the descriptive name for the issue type. See the list of scan issue types for a list of all issue names.

The path element contains the URL for the issue. It excludes the query string.

If relevant, the location element includes the URL and a description of the entry point for the attack. For example, it may contain a specific URL parameter, or a request header.

The request and response elements contain a base64 attribute. It contains a Boolean value that indicates if the messages are Base64-encoded.

Issue details

You can choose the types of details to include in the report:

Issue background - The standard description of the issue. This is the same for all issues of the same type.

Remediation background - The standard remediation advice. This is the same for all issues of the same type.

Issue detail - Specific information about the issue, if relevant.

Remediation detail - Specific remediation advice for the issue, if relevant.

Vulnerability classifications - Mappings to the Common Weakness Enumeration (CWE) list.

HTTP messages

You can choose how HTTP messages appear in the report. Select the following options for requests and responses:

Do not include - The report excludes messages of the selected type.

Include relevant extract - The report includes the parts of the message that are highlighted in the in-tool results. It also includes some of the surrounding message, to give context.

Include in full - The report includes the full messages, which may include content that doesn't directly help to understand or reproduce the issue. You can limit each message to a maximum length, so that the report doesn't become too large.

Selecting issue types

The wizard lists the different types of issues in your selection, and a count of the number of instances of each type. You can deselect issues by type. This is useful if you select a large number of issues, and want to remove less interesting issues from the report.

Report details

For HTML reports, you can specify the following details:

Report title.

How issues should be organized within the report:

By type.

By severity.

By URL.

The number of levels of detail to include in the table of contents.

The severities of issue to include in the summary table and bar chart.
