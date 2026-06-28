# Requirements for API scanning

Source: https://portswigger.net/burp/documentation/scanner/api-scanning-reqs
Fetched: 2026-06-28T09:16:09.770927+00:00

Support Center

Documentation

Scanner

Requirements for API scanning

DASTProfessional

Requirements for API scanning

Last updated:

June 18, 2026

Read time:

4 Minutes

Burp Scanner can scan APIs for vulnerabilities. This enables you to discover a larger attack surface in your applications.

Starting an API scan

Both Burp Suite DAST and Burp Suite Professional enable you to upload an API definition to be scanned. Burp Scanner automatically detects endpoints, parameters, and authentication details in the definition, then audits the detected endpoints.

More information

DAST For more information on scanning APIs in Burp Suite DAST, see Adding new API definitions.

Professional For more information on scanning APIs in Burp Suite Professional, see Scanning APIs.

Incidental API scanning

Burp Scanner also parses any API definitions that it encounters as part of its regular crawling activity, then crawls and audits any endpoints that it discovers.

Note

To disable API scanning during regular crawling activity, deselect the Parse API definitions crawl option in the Discovery logic section of your custom scan configuration.

API definition requirements

Burp Scanner can parse and scan OpenAPI definitions, SOAP WSDLs, Postman Collections, and GraphQL APIs that meet the criteria listed in each section.

OpenAPI definition requirements

Burp can parse OpenAPI definitions that:

Are in JSON or YAML format.

Do not contain external references.

Contain server URLs that are reachable by Burp Scanner.

When uploaded from a file, contain absolute URLs for server URLs.

OpenAPI endpoints

Burp Scanner identifies each server-path-method combination as a separate endpoint.

For example, if an API definition includes three servers, and each supports GET and POST, Burp identifies six endpoints.

When auditing OpenAPI endpoints, Burp Scanner follows these rules:

For optional parameters, it sends:

One request with only mandatory parameters.

One request with both mandatory and optional parameters.

For enumerated types, it sends a separate request for each permitted value.

For numeric values, it uses the maximum and minimum values in its requests.

If the API definition includes example parameter values, it includes the final example in its request.

If no example values are provided, Burp Scanner generates values to use in requests:

For arrays, it creates the minimum required number of values.

For path parameters, it generates a minimum, maximum, and random value, sending separate requests for each.

Note

If Burp can't scan any endpoints in your OpenAPI definition, it logs these in the event log.

SOAP WSDL requirements

Burp can parse SOAP WSDLs that:

Are in WSDL format.

Do not contain external references.

Contain server URLs that are reachable by Burp Scanner.

When uploaded from a file, contain absolute URLs for server URLs.

SOAP endpoints

When auditing SOAP endpoints, Burp Scanner follows these rules:

Content type is determined automatically from the SOAP version for each endpoint.

Optional parameters are always sent.

For enumerated types, it sends a single request using the first permitted value.

For numeric values, it sends a single request using a randomly generated value.

If the API definition includes example parameter values, it includes the first example in its request.

For endpoints without example parameter values, it sends a single request using a randomly generated value.

For an array, it sends the minimum required number of values to send in its request.

Note

If Burp can't scan any endpoints in your SOAP WSDL, it logs these in the event log.

Postman Collection requirements

Burp Suite can parse Postman Collections that:

Are exported in v2.1.0 format.

Contain server URLs that are reachable by Burp Scanner.

Contain absolute server URLs.

Burp doesn't currently support the following Postman features:

Variables are supported, but environments are not. You need to define Collection variables manually in Postman's Variables tab, or by editing your exported JSON to make sure the correct values are used.

Scripts are not currently supported.

Postman requests

When auditing Postman requests, Burp Scanner follows these rules:

If variables aren't defined for placeholders, Burp will use a random value.

Burp cannot scan Postman requests that:

Have a body type of file.

Have a body type of formdata.

Have a body type of graphql.

Note

If Burp can't send any requests in your Postman Collection, it logs these in the event log.

GraphQL definition requirements

Burp can scan GraphQL APIs that:

Use a URL that is reachable by Burp Scanner.

Have introspection enabled.

GraphQL endpoints

Burp Scanner can scan and audit GraphQL API endpoints. GraphQL scanning relies on introspection, a built-in feature that enables users to query the structure of the API.

When scanning GraphQL APIs, Burp Scanner uses the following process:

If you provide a GraphQL API URL, Burp Scanner sends an introspection query to that endpoint requesting details of all available queries and mutations.

During regular crawls, Burp Scanner checks for GraphQL endpoints. As GraphQL APIs use the same endpoint for all operations, the crawler does not need to find multiple endpoints to run a full crawl as it would with a REST API.

If the initial crawl does not find a GraphQL endpoint and the Test common GraphQL endpoints setting is selected, the crawler attempts to guess GraphQL endpoints using a list of common endpoint suffixes.

Once a GraphQL endpoint has been found, Burp Scanner sends an introspection query requesting details of all available queries and mutations.

If the introspection query is successful, Burp Scanner sends requests to all available queries and mutations. It uses the rules explained in each specific API section on this page to identify the arguments to send in each request. Where required, it sends multiple permutations of the same query.

Once the crawl is complete, Burp Scanner audits the discovered queries and displays discovered issues as it would with any other target.

Note

For more information on how to test GraphQL APIs effectively, see the GraphQL API vulnerabilities Web Security Academy topic.
