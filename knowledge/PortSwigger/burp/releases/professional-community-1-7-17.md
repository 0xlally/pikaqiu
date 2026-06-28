# Professional / Community 1.7.17

Source: https://portswigger.net/burp/releases/professional-community-1-7-17
Fetched: 2026-06-28T09:16:31.519379+00:00

This release adds various new features and addresses some issues.

There is a new Scanner check for suspicious input transformation. This issue arises when an application receives user input, transforms it in some way, and then performs further processing on the result. Burp reports reflected and stored input that has been transformed in the following ways:

Overlong UTF-8 sequences are decoded.

Invalid UTF-8 sequences containing illegal continuation bytes are decoded.

Superfluous (or "double") URL-encoded sequences are decoded.

HTML-encoded sequences are decoded.

Backslash escape sequences are unescaped.

Unexpected transformations resulting from submitting any of the above payloads.

Performing these input transformations does not constitute a vulnerability in its own right, but might lead to problems in conjunction with other application behaviors. An attacker might be able to bypass input filters by suitably encoding their payloads, if the input is decoded after the input filters have been applied. Or an attacker might be able to interfere with other data that is concatenated onto their input, by finishing their input with the start of a multi-character encoding or escape sequence, the transformation of which will consume the start of the following data.

Various enhancements have been made to Burp Infiltrator, in response to feedback from real-world usage:

A bug affecting the patcher when running on Java 6 or earlier has been fixed.

A bug that caused the manifest files of some nested JAR files to be lost has been fixed.

A bug that left invalid signatures in place after the relevant bytecode was modified has been fixed

Burp Scanner's issues are now mapped to CWE vulnerabilities.

There is a new command-line option to prevent Burp from pausing the Spider and Scanner when reopening existing projects. To prevent this, add the following argument to the command to launch Burp:

--unpause-spider-and-scanner

Various other enhancements and bugfixes have been made.
