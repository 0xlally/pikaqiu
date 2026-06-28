# Coding custom integrations with GraphQL API

Source: https://portswigger.net/burp/documentation/dast/user-guide/scanning-apis/adding-apis/api-integrations/coding-custom-integrations
Fetched: 2026-06-28T09:15:40.519794+00:00

DAST

Coding custom integrations with GraphQL API

Last updated:

June 18, 2026

Read time:

2 Minutes

Cloud

Self-hosted

If Burp Suite DAST doesn't have a built-in integration for the platform where your APIs are stored, you can use the GraphQL API to push API definitions into API finder from any source. You can use this to discover OpenAPI and SOAP WSDL definitions, and Postman Collections.

Note

To help you get started, you can access some example scripts in the API finder examples repository on GitHub.

When to use a custom integration

Burp Suite DAST provides built-in connectors for Amazon API Gateway, Azure API management, and Google Apigee. If your APIs are managed on either of these platforms, you can connect directly to API finder without any scripting.

Use a custom integration if your APIs are stored somewhere that doesn't have a built-in connector. For example:

API definitions stored in Git repositories alongside application code.

Internal service catalogs or custom-built API registries.

Any other source that your team maintains separately from an API management platform.

Creating a custom integration

To create an integration using the GraphQL API:

Create an API user. For more information, see Creating API users.

Add the API user to the API Uploaders group. For more information, see Role-based access control.

Write a script using the GraphQL API, to push APIs into API finder. For more information, see Getting started with the GraphQL API.

Use API finder to review APIs, and create sites for them. For more information, see Creating sites for added APIs.

When your APIs change, run your script again with the same unique_id. This tells Burp Suite DAST to update the API, instead of creating a new one.

Related pages

Discovering APIs from integrations

Creating API users

GraphQL API

dast-api-finder-examples on GitHub
