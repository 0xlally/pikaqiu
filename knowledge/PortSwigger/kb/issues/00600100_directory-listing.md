# Directory listing

Source: https://portswigger.net/kb/issues/00600100_directory-listing
Fetched: 2026-06-28T09:17:16.793174+00:00

Support Center

Issue Definitions

Directory listing

Directory listing

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Directory listing

Web servers can be configured to automatically list the contents of directories that do not have an index page present. This can aid an attacker by enabling them to quickly identify the resources at a given path, and proceed directly to analyzing and attacking those resources. It particularly increases the exposure of sensitive files within the directory that are not intended to be accessible to users, such as temporary files and crash dumps.

Directory listings themselves do not necessarily constitute a security vulnerability. Any sensitive resources within the web root should in any case be properly access-controlled, and should not be accessible by an unauthorized party who happens to know or guess the URL. Even when directory listings are disabled, an attacker may guess the location of sensitive files using automated tools.

Remediation: Directory listing

There is not usually any good reason to provide directory listings, and disabling them may place additional hurdles in the path of an attacker. This can normally be achieved in two ways:

Configure your web server to prevent directory listings for all paths beneath the web root;

Place into each directory a default file (such as index.htm) that the web server will display instead of returning a directory listing.

References

Web Security Academy: Information disclosure via directory listings

Vulnerability classifications

CWE-538: File and Directory Information Exposure

CWE-548: Information Exposure Through Directory Listing

CAPEC-37: Retrieve Embedded Sensitive Data

Typical severity

Information

Type index (hex)

0x00600100

Type index (decimal)

6291712

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Burp Scanner

This issue - and many more like it - can be found using our

web vulnerability scanner

Read more

Get Burp

Scan your web application from just $499.00

Find out more
