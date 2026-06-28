# Professional 1.6.38

Source: https://portswigger.net/burp/releases/professional-1-6-38
Fetched: 2026-06-28T09:16:28.057713+00:00

This release adds the capability to report reflected DOM-based and stored DOM-based vulnerabilities.

Burp already reports reflected XSS (where reflection of input allows direct execution of supplied JavaScript) and DOM-based XSS (where data is read from a controllable DOM location and processed in a way that allows execution of JavaScript). Burp now joins these steps together, to handle cases where:

The server returns reflected or stored input in the value of a JavaScript string.

That string is processed in a way that allows execution of JavaScript code from within the string.

The new capability applies to all of the DOM-based vulnerability types that Burp can report, such as JavaScript injection, WebSocket hijacking and open redirection.
