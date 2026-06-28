# GraphQL endpoint found

Source: https://portswigger.net/kb/issues/00200510_graphql-endpoint-found
Fetched: 2026-06-28T09:17:09.233496+00:00

Support Center

Issue Definitions

GraphQL endpoint found

GraphQL endpoint found

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: GraphQL endpoint found

Unlike REST APIs, GraphQL servers operate on a single endpoint. All messages are sent to this endpoint, with the body of the message determining how the server handles the request.

A publicly-available endpoint does not necessarily present a security vulnerability in and of itself. However, this information can still be valuable to attackers, as by definition any attacks on the GraphQL server will use the endpoint discovered. For example, an attacker could then attempt to run an introspection query against the endpoint, which could reveal the entire GraphQL schema if successful.

Remediation: GraphQL endpoint found

Ensure that you have disabled introspection on your GraphQL server when deploying to production. This will prevent attackers from using introspection queries to discover more about the operations available in your API, and other potentially sensitive information such as field descriptions.

Also, ensure that your GraphQL endpoint is only available over the POST HTTP method. Having your API available over methods such as GET or OPTIONS presents an additional attack surface and can leave the endpoint open to vulnerabilities such as CSRF.

References

Web Security Academy: GraphQL API vulnerabilities

Typical severity

Information

Type index (hex)

0x00200510

Type index (decimal)

2098448

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
