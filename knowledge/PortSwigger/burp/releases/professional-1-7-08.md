# Professional 1.7.08

Source: https://portswigger.net/burp/releases/professional-1-7-08
Fetched: 2026-06-28T09:16:28.697795+00:00

This release considerably enhances Burp Scanner's logic for reporting issues with cross-origin resource sharing (CORS) and introduces three new issues:

CORS: arbitrary origin trusted

CORS: all subdomains trusted

CORS: unencrypted origin trusted

There are many subtleties with CORS configuration that are not widely understood but can lead to catastrophic vulnerabilities, as described in today's blog post. This update puts all of the knowledge from this research into Burp so that it can accurately report all of the different problems that can arise with CORS.
