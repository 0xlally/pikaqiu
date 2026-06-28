# Professional 1.2.10

Source: https://portswigger.net/burp/releases/professional-1-2-10
Fetched: 2026-06-28T09:16:22.562635+00:00

Implements a workaround for a JRE bug which causes a "bad record mac" error in the SSL handshake when the server implements a certain combination of SSL protocols.

Fixes a bug introduced in v1.2.09 which prevented saving of state from the UI.

Provides an alert on startup and on restoration of state if live active scanning is enabled, to reduce the likelihood of inadvertently attacking websites that have been added to the target scope during previous work.

In the params view of HTTP requests, allows copying (via the context menu) of multiple rows as tab/newline delimited data, for pasting into spreadsheets, etc.
