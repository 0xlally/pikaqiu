# Professional 1.6.12

Source: https://portswigger.net/burp/releases/professional-1-6-12
Fetched: 2026-06-28T09:16:26.720904+00:00

This release contains various bugfixes and minor enhancements:

In the site map table, the "Method" column previously always showed GET for requests without a body, and POST for requests with a body, even if the actual method was different, such as HEAD or PUT. This bug has now been fixed and the table shows the correct method.

A bug which prevented client SSL certificates from being used when an upstream proxy is configured has been fixed.

A bug which caused Decoder to fail to decode hex number HTML entities containing an upper-case X has been fixed.

A bug in which the Intruder payload options UI sometimes fails to repaint properly when switching between payload sets has been fixed.

The function to Ctrl+click on a column header in the Intruder attack results to copy the contents of the column previously had two problems. Firstly, as well as copying the contents, the default action of sorting by the selected column was also being carried out. Secondly, the column contents were being copied in the ordering of the underlying data model, not the ordering of the currently sorted view. Both these issues have been fixed.

A bug which prevented the sending of items to Intruder from the active scan queue table has been fixed.

The Scanner HTML report now includes the Burp version in the report footer.

Burp now attempts to explicitly prevent SSL session reuse, as this can cause connection failures with some misconfigured or buggy target servers.

The Intruder results table now truncates long payloads to 200 characters, rather than the previous 50.
