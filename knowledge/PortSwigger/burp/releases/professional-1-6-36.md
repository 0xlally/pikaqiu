# Professional 1.6.36

Source: https://portswigger.net/burp/releases/professional-1-6-36
Fetched: 2026-06-28T09:16:27.783920+00:00

This release adds a new scan check for client-side template injection.

It is very common for applications that use AngularJS to incorporate user input into HTML responses within the client-side template. AngularJS has a long history of sandbox escapes that permit execution of arbitrary JavaScript via template expressions. Hence, when user input is echoed within AngularJS templates, it is frequently possible to perform XSS attacks using minimal syntax that is not usually sufficient to perform XSS, and so not blocked by input filters.

See today's blog post for a full description of this issue, and a list of sandbox escapes in recent versions of AngularJS.
