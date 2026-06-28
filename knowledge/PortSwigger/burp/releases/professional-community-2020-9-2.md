# Professional / Community 2020.9.2

Source: https://portswigger.net/burp/releases/professional-community-2020-9-2
Fetched: 2026-06-28T09:16:34.355791+00:00

This release enables support for recorded login sequences in Burp Scanner and provides several other minor improvements. It also includes a security fix for Burp Collaborator.

Recorded login sequences

Instead of entering basic sets of login credentials for Burp Scanner to use, you can now provide the full sequence of actions required to log in. This enables Burp Scanner to handle more complex login processes, including:

Single sign-on

Multi-step login where the username and password are not entered in the same form

Login forms that contain extra fields, checkboxes, and so on

Our dedicated Chrome extension captures your actions while you perform the login sequence and generates a JSON-based "script". You can then import this script in the Application Logins section of the scan launcher. When the crawler begins an authenticated crawl, it will open a new browser session and use the script to replicate your actions, performing the full login sequence from scratch.

For more details on how to use recorded login sequences, please refer to the scan launcher documentation.

Other improvements

You can now clear the interaction history in Burp Collaborator client.

Bug fixes

This release also implements several minor bug fixes, most notably:

The TLS handshake no longer fails when the target site's hostname contains an underscore.

All bytes are now preserved correctly when pasting data from a file into an HTTP message

Auto-modified responses resulting from match-and-replace rules are now paired with the correct request in the proxy history.

Security fix

This release resolves a security issue in the Collaborator server. Previously, an attacker in a position to perform an active, server-side MITM attack could obtain the contents of emails delivered using STARTTLS. If you are running your own Collaborator server, we recommend updating it.

This vulnerability was reported to us privately via our bug bounty program.
