# GraphQL introspection enabled

Source: https://portswigger.net/kb/issues/00200512_graphql-introspection-enabled
Fetched: 2026-06-28T09:17:09.684795+00:00

Support Center

Issue Definitions

GraphQL introspection enabled

GraphQL introspection enabled

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: GraphQL introspection enabled

Introspection uses built-in queries to return information on a GraphQL schema itself. Like regular GraphQL queries, introspection queries are highly customizable, enabling users to specify the content and data shape of the response.

GraphQL introspection can represent a significant security risk when enabled in production, as it enables attackers to see what operations are available to them within the API, as well as other potentially sensitive information such as type descriptions and private fields.

Remediation: GraphQL introspection enabled

Ensure that you have disabled introspection on your GraphQL server. Consult your server documentation if you are unsure how to do this.

References

GraphQL Introspection

Web Security Academy: GraphQL API vulnerabilities

Vulnerability classifications

CWE-200: Information Exposure

Typical severity

Low

Type index (hex)

0x00200512

Type index (decimal)

2098450

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
