# Professional / Community 1.6.30

Source: https://portswigger.net/burp/releases/professional-community-1-6-30
Fetched: 2026-06-28T09:16:30.384213+00:00

This release fixes a bug that was introduced in 1.6.29 in the handling of cookies in session handling rules. When a session handling rule attempts to update the values of multiple cookies within a single request, the bug caused this operation to fail in some situations, with the result that the request might be made out of session.
