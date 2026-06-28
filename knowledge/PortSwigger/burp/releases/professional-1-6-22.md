# Professional 1.6.22

Source: https://portswigger.net/burp/releases/professional-1-6-22
Fetched: 2026-06-28T09:16:27.255699+00:00

This release adds a new scan check for external service interaction and out-of-band resource load via injected XML doctype tags. Burp now sends payloads like:

<!DOCTYPE foo PUBLIC "-//B/A/EN" "http://chx3bggs599lgla2n3wqnj2e35.burpcollaborator.net">

and reports an appropriate issue based on any observed interactions (DNS or HTTP) that reach the Burp Collaborator server.
