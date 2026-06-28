# Running scans as part of your manual testing workflow

Source: https://portswigger.net/burp/documentation/desktop/running-scans
Fetched: 2026-06-28T09:15:51.769765+00:00

Support Center

Documentation

Desktop editions

Running scans

Professional

Running scans as part of your manual testing workflow

Last updated:

June 18, 2026

Read time:

2 Minutes

Burp Scanner is a web vulnerability scanning tool built into Burp Suite Professional. You can use Burp Scanner to automatically map the attack surface and identify vulnerabilities in both web applications and APIs. This streamlines your workflow by automating repetitive tasks, freeing you to use your time and expertise on more complex manual tasks.

You can run different types of web application scans to support a wide range of use cases:

Crawl - Automatically map the application's attack surface, saving you from having to manually navigate

through the whole application, clicking every link and submitting every form.

Full crawl and audit - Automatically map the attack surface and probe discovered requests for vulnerabilities. Burp

Scanner handles the more repetitive auditing tasks so you can concentrate on more sophisticated manual testing.

Audit selected items - Automatically probe for issues in one or more requests that you think may be vulnerable. This

enables you to test for a wide range of vulnerabilities in seconds, rather than hours.

Burp's AI-powered Explore Issue feature enables you to automate follow-up testing on vulnerabilities that Burp Scanner identifies. This can help you uncover additional attack vectors and generate proof-of-concept exploits automatically.

If Burp Scanner discovers any API definitions in a web application scan, it parses the definition, then audits the discovered endpoints. For more information about which API formats Burp Scanner supports, see

Requirements for API scanning.

Burp Scanner also offers an API-only scanning option for when you need to do a standalone scan based on an OpenAPI definition, SOAP WSDL, or Postman Collection.

Related pages

This section explains how to run and configure scans in Burp Suite Professional. For information on how to create and manage scans in Burp Suite DAST, see Working with scans.

For information on how Burp Scanner works under the hood, see the Burp Scanner documentation.

In this section

Scanning web applications

Running API-only scans

Live tasks

Setting the scan scope

Configuring scans

Adding custom scan checks

Adding extension scan checks

Viewing scan results

Exploring issues with AI

Reporting scan results

Configuring application logins

Managing resource pools
