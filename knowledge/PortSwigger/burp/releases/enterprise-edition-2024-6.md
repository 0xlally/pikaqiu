# Enterprise Edition 2024.6

Source: https://portswigger.net/burp/releases/enterprise-edition-2024-6
Fetched: 2026-06-28T09:16:21.045984+00:00

This release introduces dedicated API scanning, enabling you to upload and scan OpenAPI (Swagger) definition files. We have also added some quality of life improvements, including verbose mode for CI-driven scans.

API scanning

You can now upload OpenAPI definition files directly to Burp Suite Enterprise Edition. We have added a new Site type option to the Create a new site page, enabling you to select whether you want to scan an API or a web app.

You can provide API definitions either by uploading a file directly or by providing a live link to the file's location. If you provide a live link, then Burp Suite Enterprise Edition obtains the latest version of the file each time it scans the API.

You can also configure authentication for the endpoints in your API definition. If you upload a file directly, then Burp Suite Enterprise Edition parses the definition for required Basic, Bearer Token, or API Key authentication schemes at the time you create the site. You can also add schemes and credentials manually.

Once you have saved your API site, you can manage it through the Sites menu as you would with a regular web app site. This includes configuring options such as scan configurations, upstream proxies, and scanning pools. Note that you do not have to specify a scan configuration to scan an API site, whereas web app scans require a scan configuration.

Quality of life improvements

We have also made the following improvements in this release:

You can now run CI-driven scans in verbose mode. When scanning in verbose mode, the scan produces more detailed output. To use verbose mode, set the verboseScanning parameter to enabled: true in the configuration file.

When you install Burp Suite Enterprise Edition on a Linux server that has FIPS or CIS enabled, a default user called burpsuite is created in a group also called burpsuite. Previously, you needed to create a user and group manually before running the installer.

Scope changes in GraphQL API

The deprecated scope field in the GraphQL API has now been removed. You should now use the scope_v2 field when making API calls, as this includes separate properties for the start URL and the included URL prefixes.

For more information, see our GraphQL API documentation.
