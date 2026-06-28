# Getting started with the GraphQL API

Source: https://portswigger.net/burp/documentation/dast/user-guide/api-documentation/graphql-api/getting-started
Fetched: 2026-06-28T09:15:34.636349+00:00

DAST

Getting started with the GraphQL API

Last updated:

June 18, 2026

Read time:

2 Minutes

You can use the GraphQL API to integrate Burp Suite DAST with your own software or a third-party tool. This page explains some points you should be aware of as you get started with the GraphQL API.

Creating an API user

To use the GraphQL API you must create a dedicated API user in Burp Suite DAST. For instructions on how to create an API user, see Creating API users.

You can only use the API to perform actions that your user has permission for. For instructions on how to appropriately configure the permissions for the user, see Role-based access control.

Structuring the GraphQL call

All operations are performed by sending POST requests to your-web-server-url/graphql/v1. You do not need to use different endpoints for different query or mutation types as you would in a REST API.

To authorize your request, enter an Authorization header with your API key as its value.

Example request

This example shows a GetSiteTree request in cURL format.

curl --request POST \

--url [your-burp-enterprise-server-url]:[port]/graphql/v1 \

--header 'Authorization: [api-key]' \

--header 'Content-Type: application/json' \

--data '{"query":"query GetSiteTree {\nsite_tree {\nsites {\nid\nname\nscope_v2 {\nstart_urls\nin_scope_url_prefixes\nout_of_scope_url_prefixes\nprotocol_options\n}\napplication_logins {\nlogin_credentials {\nlabel\nusername\n}\nrecorded_logins {\nlabel\n}\n}\nparent_id\nextensions {\nid\n}\n}\nfolders {\nid\nname\n}\n}\n}","operationName":"GetSiteTree"}'

Using Insomnia

We recommend that you use Insomnia to build and test GraphQL calls. Insomnia integrates with our GraphQL schema documentation and allows you to easily convert your GraphQL request to other formats. For more information, refer to Insomnia's documentation.

Related pages:

For worked examples of some common tasks using the GraphQL API, see Performing common tasks with the GraphQL API.

For more comprehensive reference information and a further introduction to the GraphQL API, see Full reference information on the GraphQL API.
