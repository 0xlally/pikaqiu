# Scan configurations

Source: https://portswigger.net/burp/documentation/scanner/scan-configurations
Fetched: 2026-06-28T09:16:11.031828+00:00

Support Center

Documentation

Scanner

Scan configurations

DASTProfessional

Scan configurations

Last updated:

June 18, 2026

Read time:

1 Minute

Scan configurations are collections of settings that define how a scan is performed. For example, a scan configuration can specify the maximum crawl depth of the crawl, or what types of issues to report.

There are two ways to configure scans for a site in Burp Suite DAST and Burp Suite Professional:

Preset scan modes are predefined collections of scan settings. They offer a quick way to adjust how the scan balances speed and coverage.

Custom configurations enable you to fine-tune Burp Scanner's behavior to meet your needs. You can either use the built-in custom configurations from the configuration library, or create your own configurations from scratch.

Note

In Burp Suite DAST, you can set scan configurations for folders, subfolders, and sites. Subfolders and sites inherit the scan configurations from their parent folders. To learn how these scan configurations are combined by Burp Scanner, see Defining the scan configuration for a folder.

In this section

Preset scan modes.

Custom scan configurations.

Burp Scanner built-in configurations.

Audit settings.

Crawl settings.
