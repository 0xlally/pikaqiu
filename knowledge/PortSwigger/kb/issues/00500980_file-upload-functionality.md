# File upload functionality

Source: https://portswigger.net/kb/issues/00500980_file-upload-functionality
Fetched: 2026-06-28T09:17:13.449015+00:00

Support Center

Issue Definitions

File upload functionality

File upload functionality

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: File upload functionality

File upload functionality is commonly associated with a number of vulnerabilities, including:

File path traversal

Persistent cross-site scripting

Placing of other client-executable code into the domain

Transmission of viruses and other malware

Denial of service

You should review file upload functionality to understand its purpose, and establish whether uploaded content is ever returned to other application users, either through their normal usage of the application or by being fed a specific link by an attacker.

Some factors to consider when evaluating the security impact of this functionality include:

Whether uploaded content can subsequently be downloaded via a URL within the application.

What Content-type and Content-disposition headers the application returns when the file's content is downloaded.

Whether it is possible to place executable HTML/JavaScript into the file, which executes when the file's contents are viewed.

Whether the application performs any filtering on the file extension or MIME type of the uploaded file.

Whether it is possible to construct a hybrid file containing both executable and non-executable content, to bypass any content filters - for example, a file containing both a GIF image and a Java archive (known as a GIFAR file).

What location is used to store uploaded content, and whether it is possible to supply a crafted filename to escape from this location.

Whether archive formats such as ZIP are unpacked by the application.

How the application handles attempts to upload very large files, or decompression bomb files.

Remediation: File upload functionality

File upload functionality is not straightforward to implement securely. Some recommendations to consider in the design of this functionality include:

Use a server-generated filename if storing uploaded files on disk.

Inspect the content of uploaded files, and enforce a whitelist of accepted, non-executable content types. Additionally, enforce a blacklist of common executable formats, to hinder hybrid file attacks.

Enforce a whitelist of accepted, non-executable file extensions.

If uploaded files are downloaded by users, supply an accurate non-generic Content-Type header, the X-Content-Type-Options: nosniff header, and also a Content-Disposition header that specifies that browsers should handle the file as an attachment.

Enforce a size limit on uploaded files (for defense-in-depth, this can be implemented both within application code and in the web server's configuration).

Reject attempts to upload archive formats such as ZIP.

References

Various proof-of-concept files

An XSS polyglot attack

Vulnerability classifications

CWE-434: Unrestricted Upload of File with Dangerous Type

CAPEC-17: Using Malicious Files

Typical severity

Information

Type index (hex)

0x00500980

Type index (decimal)

5245312

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
