# API overview

Source: https://portswigger.net/burp/documentation/dast/user-guide/api-documentation
Fetched: 2026-06-28T09:15:34.250261+00:00

DAST

API overview

Last updated:

June 18, 2026

Read time:

1 Minute

Burp Suite DAST provides two APIs that you can use to interact with the system from other third-party software. The GraphQL API offers the broadest range of functionality and is recommended for new integrations, while the REST API offers a simple migration for users who are familiar with the Burp Suite Professional API.

Using the APIs

In order to use either of Burp Suite DAST's APIs, you will need to set up an API user. API users each have a unique API key that enables them to authenticate when making requests.

Note that Burp Suite DAST's user roles apply to API users in the same way as UI users. You can only use the APIs to perform those tasks that the user permissions associated with your role allow. As such, you should make sure that any API users you set up have the correct roles applied.

Related pages

Creating API users.

GraphQL API

REST API

For more information on configuring roles in Burp Suite DAST, see Role-based access control.
