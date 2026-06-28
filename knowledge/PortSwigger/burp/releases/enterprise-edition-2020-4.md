# Enterprise Edition 2020.4

Source: https://portswigger.net/burp/releases/enterprise-edition-2020-4
Fetched: 2026-06-28T09:16:16.528342+00:00

GraphQL API

This release provides a beta version of our brand new GraphQL-based API, which exposes most of the core functionality of Burp Suite Enterprise Edition. Among other things, you can use the new API to:

Create and edit sites

Schedule one-off and regular scans

Create and edit custom scan configurations

Add folders to your site tree

Get scan results and reports

Manage your pool of agent machines, including authorizing new agent machines.

You can find more detailed information about how to use the API and the full range of supported operations in the API documentation. This also includes example payloads for typical queries.

As this is a beta version of the API, we would be grateful if customers could inform us of any problems that they encounter so that we can continue to optimize the behavior over the coming months. The Jenkins/TeamCity CI plugins and the generic CI driver will continue to use the existing public REST API. However, we are planning to release additional GraphQL-based versions in the near future.

Note: As a workaround for accessing functionality that was not supported by the public REST API, a small number of customers have integrated their own tools with Burp Suite Enterprise Edition using our internal REST API. Unfortunately, after upgrading to version 2020.4, these integrations will no longer be supported because the internal REST API has largely been replaced. However, you should be able to refactor your integrations to achieve the same results using the new GraphQL API. The vast majority of customers will be unaffected by this issue.

Bug fixes

We have also implemented several minor performance improvements and bug fixes. Most notably, the following issues have been resolved:

A null pointer exception is no longer raised when Jira tickets are created automatically using the default severity and confidence settings.

Changing the name of a site while using a slower network connection no longer causes errors.

Cloud deployment links

We no longer provide AWS CloudFormation or Azure Resource Manager templates. We're releasing an improved, much simpler deployment method soon and recommend waiting for this instead.
