# Professional / Community 1.7.26

Source: https://portswigger.net/burp/releases/professional-community-1-7-26
Fetched: 2026-06-28T09:16:32.041662+00:00

This release adds a number of new scan checks relating to file upload functionality.

Burp Scanner has always treated the contents of a file upload (within a multipart POST request) as a regular insertion point where payloads can be placed. In the new release, various additional checks are performed on the file upload:

Some new payloads are used to upload files in various formats, such as PDF, SVG, HTML, PHP, and SSI.

Where relevant, Burp now modifies the file extension and content-type fields in the upload request to reflect the type of file that is being uploaded, so as to maximize the chance that the application will handle the file in the desired way.

Both in-band and out-of-band techniques are used to detect vulnerabilities in the application's handling of uploaded files.

For example, Burp can now detect server-side rendering of uploaded PDF documents, by using some embedded PDF JavaScript to trigger a Burp Collaborator interaction when the document is rendered:

The new detection techniques all lead to new versions of existing issues, notably PHP code injection, SSI injection, reflected XSS, stored XSS, and external service interaction.

Note: Some updates have been made to Burp Collaborator server to support the new scan checks. People running private Collaborator servers should update these now. As usual, Burp will show an alert on startup if the configured Collaborator server is out of date, and you can use the Collaborator health check to determine this at any time.

A number of bugs are also fixed, including a recently introduced bug affecting NTLM authentication.
