# Professional 1.6.06

Source: https://portswigger.net/burp/releases/professional-1-6-06
Fetched: 2026-06-28T09:16:26.393760+00:00

This release includes some major enhancements to the Scanner engine. Burp can now automatically report the following new types of issues:

Perl code injection

PHP code injection

Ruby code injection

Server-side JavaScript code injection

File path manipulation

Serialized object in HTTP message

Client-side JSON injection (DOM-based)

Client-side XPath injection (DOM-based)

Document domain manipulation (DOM-based)

Link manipulation (DOM-based)

DOM data manipulation (DOM-based)

Additionally, the scanning logic for several existing checks has been enhanced to improve accuracy.

A number of bugs have also been fixed, including:

A bug that caused the option "skip server side injection tests for these parameters" to not work in some situations.

A bug that caused session handling rules to fail when using the sessions tracer, in some situations.

A bug affecting the auto-generation of CA-signed per-host SSL certificates, in some situations.

A bug that sometimes caused Burp to hang on startup when reloading certain extensions.
