# Enterprise Edition 2023.12

Source: https://portswigger.net/burp/releases/enterprise-edition-2023-12
Fetched: 2026-06-28T09:16:19.003601+00:00

This release introduces BChecks, custom extensions that enable you to extend and tailor your scans in Burp Suite Enterprise Edition, as well as some other improvements and bug fixes.

BChecks

We're introducing BChecks to Burp Suite Enterprise Edition. These custom scan checks enable you to extend Burp Scanner in a quick and simple way, to tailor your scans to your own applications' framework and provide targeted coverage for new and novel vulnerabilities.

You can find these specific custom scan checks in the BChecks GitHub repository, then Administrators can then import them to Burp Suite Enterprise Edition to make them available for users to apply to sites and folders.

Other improvements

We've made some other improvements, including:

SAML metadata files can now be downloaded by system administrators. In Settings > Integrations > SAML, click Export metadata to download these as an XML file.

Burp Suite Enterprise Edition has been updated to the latest version of Azul Zulu Java (17.0.9+8).

Older versions of the built-in browser are now automatically deleted when Burp Suite Enterprise Edition updates.

Bug fixes

We've fixed some bugs, including:

A bug causing CI-driven scans that had headers and/or cookies specified in the config file to fail.

A bug causing the UI to remain stuck in edit mode and fail to display the correct site when switching between sites from edit mode.

A bug preventing the scanner from running extensions in the order that they were applied to the site or folder. This fix enables you to arrange your extensions to run in a specific order, for example, authentication extensions first, and logging extensions last.
