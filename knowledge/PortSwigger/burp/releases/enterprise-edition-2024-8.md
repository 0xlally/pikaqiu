# Enterprise Edition 2024.8

Source: https://portswigger.net/burp/releases/enterprise-edition-2024-8
Fetched: 2026-06-28T09:16:20.925833+00:00

This release introduces endpoint configuration for API scanning, including the ability to select and deselect endpoints, as well as search and filtering functionality. We've also added API authentication for CI-driven scans.

Configure endpoints for API scanning

When uploading an API definition to scan, you can now configure which endpoints to include or exclude from your scan, giving you better control over your testing scope. For example, this enables you to prevent scans from sending potentially destructive DELETE requests.

You can also search the list of endpoints and filter by HTTP

method, making it easy to manage APIs with a large number of endpoints.

You can access all of this functionality from the new Endpoints tab when creating a site.

API authentication for CI-driven scans

You can now manage API authentication for CI-driven scans by adding the authentication details directly into the CI configuration YAML file. You can add details for API key, Basic, and Bearer Token authentication methods.

Scan checks for detecting OpenAPI definitions

Burp Suite Enterprise Edition now includes active and passive scan checks to detect OpenAPI definitions during scans. The scan checks use a list of common OpenAPI definition file names and locations to search for publicly available definitions.

Other improvements

We've made some other improvements, including:

We updated the Azul Zulu JRE

to 21.36.17.

We added a new entry type to the user activity log that records when a scan is started, including details of which scheduled scan it belongs to.

We now enter text for recorded logins character by character, instead of as a whole string. This more realistically simulates keys being pressed and released.

Bug fixes

We've fixed some bugs, including:

A bug causing the page to freeze when the tab menu in the side panel wrapped onto multiple lines.

A bug that was causing some scans to time out and fail to start.

A bug that was preventing some OpenAPI v2

files from being parsed correctly when creating a new site.
