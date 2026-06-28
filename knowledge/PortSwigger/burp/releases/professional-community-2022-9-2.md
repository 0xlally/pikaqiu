# Professional / Community 2022.9.2

Source: https://portswigger.net/burp/releases/professional-community-2022-9-2
Fetched: 2026-06-28T09:16:38.984827+00:00

This release provides various new features for the Montoya API. It also includes some bug fixes for Burp Scanner and an update for Burp's browser.

New Montoya API features

We have added several new features to the Montoya API. These include:

New methods to create, modify, and delete request / response headers.

The ability for an extension to query which edition of Burp (that is, Professional, Community Edition, or Enterprise Edition) it is currently running in.

The ability to generate collaborator payloads from your own custom data.

The ability to export the secret key that the Collaborator uses for extensions and restore a previous Collaborator client session from it.

New utilities to generate random sequences and manipulate byte arrays.

Browser update

This release updates Burp's browser to Chromium 106.0.5249.61, which fixes a number of high-severity security issues.

Bug fixes

This release also includes a couple of bug fixes for Burp Scanner, including:

We have fixed a bug that prevented the crawler from handling links that are added to a page by JavaScript following a delay.

We have fixed a bug whereby Burp Scanner was failing to find CSRF vulnerabilities on sites that return a 302 response when CSRF is exploited.
