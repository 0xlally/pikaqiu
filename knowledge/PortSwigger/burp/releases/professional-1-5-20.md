# Professional 1.5.20

Source: https://portswigger.net/burp/releases/professional-1-5-20
Fetched: 2026-06-28T09:16:25.678357+00:00

This release adds support for nested insertion points to the Scanner.

Nested insertion points are used when an insertion point's base value contains data in a recognized format. For example, a URL parameter might contain Base64-encoded data, and the decoded value might in turn contain JSON or XML data. With the option to use nested insertion points enabled, Burp will create suitable insertion points for each separate item of input at each level of nesting.

Below are some examples of Burp's new capabilities in scanning nested insertion points, running against some targets in our lab.

SQL injection into a Base64-encoded value within a JSON value within a URL parameter:

SQL injection into a JSON value within XML within a URL parameter:

SQL injection into XML within a JSON value within a URL parameter:

XSS in a JSON value within a Base64-encoded URL parameter:

XSS in a JSON value within XML within a URL parameter:

XSS in an XML value within JSON within a URL parameter

You get the idea. There is no limit to how deep Burp can go. If it recognizes the data format of the base value of any insertion point, Burp will look inside that data for nested values that should be tested.

The option to include nested insertion points is on by default, and using this option imposes no overhead when scanning requests containing only conventional parameters. However, it enables Burp to reach much more of the attack surface of today's complex applications where data is encapsulated within different formats.
