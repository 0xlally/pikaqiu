# GraphQL suggestions enabled

Source: https://portswigger.net/kb/issues/00200513_graphql-suggestions-enabled
Fetched: 2026-06-28T09:17:09.640523+00:00

Support Center

Issue Definitions

GraphQL suggestions enabled

GraphQL suggestions enabled

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: GraphQL suggestions enabled

GraphQL suggestions are an Apollo feature in which the server is configured to respond to invalid queries with suggestions for valid queries that have a similar syntax.

Suggestions can represent a significant security risk, as they enable attackers to glean information about a GraphQL schema even if introspection is disabled. By sending intentionally invalid queries and collating suggestions in responses, attackers can learn the names and structures of valid queries and mutations.

Remediation: GraphQL suggestions enabled

Ensure that you have disabled or otherwise masked error messages containing suggestions on your GraphQL server.

References

Disabling Apollo suggestions

Clairvoyance: A tool to gather information from suggestions

Web Security Academy: GraphQL API vulnerabilities

Vulnerability classifications

CWE-200: Information Exposure

Typical severity

Low

Type index (hex)

0x00200513

Type index (decimal)

2098451

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Burp Scanner

This issue - and many more like it - can be found using our

web vulnerability scanner

Read more

Get Burp

Scan your web application from just $499.00

Find out more
