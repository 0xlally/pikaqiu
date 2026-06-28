# Professional / Community 2023.11.1.3

Source: https://portswigger.net/burp/releases/professional-community-2023-11-1-3
Fetched: 2026-06-28T09:16:41.533807+00:00

This release introduces new features for manual testing of GraphQL APIs, BChecks syntax highlighting, and broken access control scan checks.

Manual GraphQL testing tools

This release introduces new tools that make it simpler and more efficient to work with GraphQL APIs in Burp Suite.

Viewing and editing GraphQL requests

When Burp detects a GraphQL request from your target, it adds a GraphQL tab to the message editor for the request. This tab separates the GraphQL query from the rest of the request, and formats it in a way that makes it easy to view and edit the query structure and its associated variables.

Generating introspection queries

We've added functionality that makes it possible to generate and send an introspection query in just a few short clicks. Additionally, you can save the results of your introspection query to the site map, giving you a clear overview of the attack surface and potential vulnerabilities in GraphQL APIs.

BChecks syntax highlighting

We've added syntax highlighting to the BChecks editor. The editor now automatically colors your keywords, literals, functions, and variables, making it easier to read and edit BCheck definitions.

New scan check: Broken access control

We've added an experimental new scan check for broken access control vulnerabilities.

While we refine it to reduce the number of false positives it generates, we've disabled this check when using Normal audit accuracy. To try it out, from your audit configuration, go to Audit optimization > Audit accuracy and select Minimize false negatives. We welcome any feedback.

If you want to learn more about broken access control vulnerabilities, check out the Access control topic on the Web Security Academy.

Other updates

We have made a number of additional improvements, including:

The option to add notes and highlights to your Bambdas.

Burp Scanner now automatically generates logical examples for path parameters when scanning open API specifications, meaning fewer pages are missed during the audit.

Bug fixes

We've fixed some bugs, including:

An issue with request kettling in Repeater.

Vulnerability classifications not appearing on extension-generated reports.

Browser upgrade

We've upgraded Burp's built-in browser to 120.0.6099.62 (Linux and Mac), 120.0.6099.62/.63 (Windows). For more information, see the Chromium release notes.
