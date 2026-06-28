# Enterprise Edition 2024.11

Source: https://portswigger.net/burp/releases/enterprise-edition-2024-11
Fetched: 2026-06-28T09:16:20.048997+00:00

This release enables you to generate scan reports in PDF format, and generate compliance reports that are compatible with PCI DSS v4.0.1. We also added support for SOAP API scans. We made a number of other performance improvements, and fixed some bugs.

Improvements to scan reports

You can now generate standard reports and compliance reports in PDF format, as well as HTML. To generate PDF reports, go to the Scans > Reporting tab and select from the Report type dropdown menu.

In addition, you can now generate compliance reports for PCI DSS v4.0.1.

Support for SOAP API scanning

Burp Suite Enterprise Edition now supports SOAP API scans. You can upload a SOAP WSDL definition file, or provide a URL. We also support SOAP API scanning for CI-driven scans.

Performance improvements

We've made a number of performance improvements to Burp Suite Enterprise Edition, to make it more responsive. Any actions that retrieve site data are much faster. These include bulk selecting sites, loading the site tree, and loading the dashboard.

Sites for API scans now load much faster, and we've improved the site search function.

In addition, recorded logins can be replayed reliably and without delays.

Bug fixes

We fixed the following bugs:

Links in HTML scan reports are no longer broken.

Fixed an issue with validating CA certificates.

Fixed an issue when out-of-scope prefixes are removed and then re-added to a site.

We corrected the scan count for Cloud instances when you run CI-driven scans.

Fixed an issue with type_index in BChecks and extensions, that prevented issue types from being expanded in the UI.
