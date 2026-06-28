# Custom scan configurations

Source: https://portswigger.net/burp/documentation/scanner/scan-configurations/custom-scan-configurations
Fetched: 2026-06-28T09:16:11.140708+00:00

Support Center

Documentation

Scanner

Scan configurations

Custom scan configurations

DASTProfessional

Custom scan configurations

Last updated:

June 18, 2026

Read time:

2 Minutes

Both Burp Suite DAST and Burp Suite Professional enable you to use custom scan configurations, giving you fine-grained control over Burp Scanner's behavior. You can use custom configurations in several ways:

Use one of the built-in configurations from the configuration library.

Create an entirely new configuration.

Import a configuration from another installation of Burp Suite DAST or Burp Suite Professional.

Scan configuration structure

You can configure the following types of settings in a custom scan configuration:

Crawl settings control Burp Scanner's behavior during the crawl phase of the scan. This enables you to specify details such as the maximum crawl length and how errors are handled when crawling.

Audit settings control Burp Scanner's behavior during the audit phase of the scan. This enables you to specify details such as the scan checks and the insertion point types used.

The crawl and audit settings are similar for Burp Suite Professional and Burp Suite DAST. Burp Suite DAST also has additional settings.

Related pages

Audit settings.

Crawl settings.

Custom scan configuration settings (Burp Suite DAST).

Using custom configurations in Burp Suite Professional

In Burp Suite Professional, you can create custom configurations from scratch, or start from a preset or built-in configuration and adapt it. This makes it easy to build on existing settings.

Related pages

Configuring scans in Burp Suite Professional

Using custom configurations in Burp Suite DAST

In Burp Suite DAST, you can create a new custom configuration, or import an existing one to use as a starting point.

You can set configurations for folders, subfolders, and sites. Subfolders and sites inherit the scan configurations from their parent folders. This enables you to tune Burp Scanner's behavior for certain sites and use cases.

Related pages

Defining

the scan configuration for a folder (Burp Suite DAST)

Using custom scan configurations (Burp Suite DAST).
