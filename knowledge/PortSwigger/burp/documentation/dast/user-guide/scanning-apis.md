# Scanning APIs

Source: https://portswigger.net/burp/documentation/dast/user-guide/scanning-apis
Fetched: 2026-06-28T09:15:40.420010+00:00

DAST

Scanning APIs

Last updated:

June 18, 2026

Read time:

2 Minutes

Cloud

Self-hosted

This section explains how to scan APIs in Burp Suite DAST. For information on how to add APIs, see Adding APIs to DAST.

Note

You can add as many APIs as you like to Burp Suite DAST but for scans to work correctly, you need to configure your network and firewall settings.

For more information, see

Configuring network and firewall settings for a site.

Adding API definitions

You can add API definitions by uploading a file or providing a URL. The supported formats are:

Postman Collection

OpenAPI definition file in JSON or YAML format

SOAP WSDL

GraphQL (URL only, using introspection)

For Postman Collections, you can also upload a Postman environment file to automatically merge environment variables with your collection. This removes the need to manually merge variables and speeds up your setup process.

For GraphQL APIs, make sure introspection is switched on. For more information, see GraphQL definition requirements.

Note

We fully support OpenAPI 3.1 and provisionally support OpenAPI 3.2.

Choosing how to add APIs

You can add API sites individually or in bulk:

Add a single API - Create one API site at a time by uploading a file or providing a URL. Use this approach when you need to configure each API individually or when onboarding a small number of APIs.

Bulk upload APIs - Create multiple API sites in one operation. Use this approach when onboarding large numbers of APIs with shared configuration settings. This speeds up the process and helps ensure consistency across your API estate.

For more information, see:

Adding a single API

Bulk uploading APIs

Managing authentication for API sites

When you add an API definition, Burp Suite DAST automatically detects authentication schemes. You don't have to provide credentials immediately.

To add authentication credentials after creating a site:

Go to Sites and select your API site.

Select the Details tab and click Edit.

Under API definition, select the Authentication tab. Add any credentials that are shown as missing.

Click Save.

Optional settings for your API

When you add a new API site, you can configure the following additional settings:

Scan configuration

Connections

Headers and cookies

Extensions

Scanning pool

Burp AI and automation

Notifications

For more information on configuring the optional settings for your API,

see Configuring site settings.

Related pages

Discovering APIs from integrations

Adding a single API

Bulk uploading APIs

Configuring API authentication

Viewing and configuring API endpoints
