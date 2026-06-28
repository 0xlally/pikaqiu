# Discovering APIs from integrations

Source: https://portswigger.net/burp/documentation/dast/user-guide/scanning-apis/adding-apis/api-integrations
Fetched: 2026-06-28T09:15:40.337051+00:00

DAST

Discovering APIs from integrations

Last updated:

June 18, 2026

Read time:

1 Minute

Cloud

Self-hosted

You can connect Burp Suite DAST to third-party platforms to automatically discover APIs deployed in your environment. Discovered APIs appear in API finder, where you can review them and create scan sites.

You can do this in the following ways:

Integrating with AWS - Use the built-in integration for Amazon API Gateway.

Integrating with Azure API Management - Use the built-in integration for Azure API Management.

Integrating with Google Apigee - Use the built-in integration for Google Apigee.

Coding custom integrations - Write a script to push APIs into API finder from any other source using the GraphQL API.

Once your integration is set up, you can review and manage the APIs that appear in API finder:

Creating sites for added APIs - Review APIs in API finder and create scan sites for the ones you want to scan.

Updating your API sites - Keep your API sites up to date when your integration discovers new endpoints.

Related pages

Adding APIs to DAST
