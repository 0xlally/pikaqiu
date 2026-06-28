# Enterprise Edition 2024.3

Source: https://portswigger.net/burp/releases/enterprise-edition-2024-3
Fetched: 2026-06-28T09:16:20.419601+00:00

This release makes some improvements for CI-driven scans. We've also fixed some bugs.

Improvements for CI-driven scans

You can now set any value in the configuration file using an environment variable. This means that you don’t have to create a new configuration file in your CI/CD pipeline.

We've also improved the error messages if there's a problem communicating with the Enterprise server, to make troubleshooting easier.

MySQL support

We have removed support for the MySQL external database version 5.7. We currently support version 8.3.0 and any versions that are supported by MySQL.

Bug fixes

We've fixed the following bugs:

If you run the updater.bat file manually in a Windows environment, it no longer deletes your installation.

Users who have permission to edit sites and folders can now view a folder when they click on it in the site tree.
