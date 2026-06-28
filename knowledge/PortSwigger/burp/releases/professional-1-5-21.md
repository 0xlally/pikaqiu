# Professional 1.5.21

Source: https://portswigger.net/burp/releases/professional-1-5-21
Fetched: 2026-06-28T09:16:26.199814+00:00

This release adds support for WebSockets to the Proxy tool. You can now view, intercept and modify WebSockets messages in the same way as regular HTTP messages:

There is a new Proxy history tab for WebSockets messages, with the same capabilities as the HTTP history (filter, sort, search, etc.):

You can configure whether incoming and outgoing WebSockets messages are intercepted at Proxy / Options / Intercept WebSockets Messages.

The Scanner's support for nested insertion points, which was introduced in the previous release, has been updated:

Nested data in URL-encoded query string format is now recognized, and insertion points are created for each parameter value within the nested data. This is only done if the nested query string contains at least two parameters, so as to avoid false positive in common cases where a parameter value happens to contain the = character.

Highlighting of relevant syntax in reported Scanner issues is now fully precise within nested insertion points, and picks out the exact item of input that Burp modified in order to identify the issue.

The Scanner reporting function now has an option to embed report images inline within the generated HTML. This works on all recent browsers, but you can revert to the old behavior (of images stored in a subdirectory) if you prefer.

There is a new function to report anonymous feedback about Burp's performance. This will help us improve Burp by obtaining technical information about problems within Burp. The feedback does not identify the user, but you can turn this function off at Options / Misc / Performance Feedback.

Various bugs have been fixed.
