# Scanning web applications

Source: https://portswigger.net/burp/documentation/desktop/running-scans/webapp-scans
Fetched: 2026-06-28T09:15:53.946252+00:00

Support Center

Documentation

Desktop editions

Running scans

Scanning web applications

Professional

Scanning web applications

Last updated:

June 18, 2026

Read time:

1 Minute

This section explains how to configure and run web application scans in Burp Suite Professional.

When scanning web applications, Burp automatically catalogs and analyzes the application's structure and traffic, including any REST, SOAP, and GraphQL APIs that it discovers. It adds all requests, responses, and resources found during the scan to the site map.

Related pages

For information on how to do a standalone scan based on an OpenAPI definition or SOAP WSDL, see Running

API-only scans.

Burp Scanner enables you to launch web application scans in the following ways:

Crawl and audit. Burp Scanner maps the structure and endpoints of the target application, then runs a series of automated tests to probe for vulnerabilities.

Crawl. Burp Scanner maps the structure and endpoints of a target without running any automated vulnerability checks.

Audit selected items. This is useful if you want to audit a specific HTTP request that you think might be vulnerable.

Related pages

This section focuses on launching one-off scans in Burp Suite Professional.

For information on how to set up recurring, automated DAST scans in Burp Suite DAST, see Adding web app sites.

For information on how to set up live tasks that automatically scan traffic from other tools in Burp Suite, such as the traffic that passes through Burp Proxy as you browse, see

Live tasks.

In this section

Running a full crawl and audit

Scanning specific HTTP messages

Configuring scans
