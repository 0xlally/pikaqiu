# Professional / Community 2024.9

Source: https://portswigger.net/burp/releases/professional-community-2024-9
Fetched: 2026-06-28T09:16:49.042862+00:00

This release introduces significant enhancements to Burp Intruder, custom Bambda HTTP match and replace rules, and support for scanning SOAP endpoints. We've also made other improvements and bug fixes.

Streamlined layout for Burp Intruder

We've given Burp Intruder a major upgrade. You can now view and edit your attack configuration from a new side panel, instead of the old subtabs. The streamlined layout enables you to edit payload positions, payloads, and attack settings without the need to constantly switch between tabs. This makes configuring your attacks faster and more efficient.

HTTP match and replace rules with Bambdas

We've introduced a feature that enables you to create HTTP match and replace rules using Bambdas. This enables you to handle complex or bulk changes more flexibly and easily. For example, you could use match and replace Bambdas to more easily delete a large number of headers, or intelligently modify response JSON data, streamlining client-side testing.

Please note, this feature is only available in Burp Suite Professional.

To learn more about Bambdas in Burp, see Bambdas.

SOAP API scanning

Burp Scanner now includes support for scanning SOAP APIs, giving you broader security coverage for web services using the SOAP protocol.

Automatic SOAP API detection: During web app scans, if the scanner detects any SOAP APIs, it automatically includes them in its crawl and audit.

Dedicated SOAP API scans: You can also run standalone SOAP API scans to focus your testing efforts when required.

Please note, this feature is currently only available in Burp Suite Professional.

Quality of life improvements

We've made the following quality of life improvements:

We've added a Last accessed column to the Open existing project table in the startup wizard. This means that you can now sort your project files based on the date they were last opened.

We've improved how Burp Scanner handles images, scripts, and stylesheets. The browser has always requested these resources during scans but only a subset of those requests, such as API calls, were audited. Now, all requests, including static resources like images and scripts, are sent for auditing. This provides broader coverage and ensures that the crawl path accurately reflects everything loaded during the scan.

Chromium incompatibility with Amazon Linux 2

In version 2024.6.4, we upgraded Burp's built-in browser to Chromium 127.0.6533.72 for Linux, which introduced compatibility issues with Amazon Linux 2. This issue persists in all subsequent versions of Chromium, meaning Burp's built-in browser remains unusable on that OS.

We advise users not to run scans on Amazon Linux 2 with Burp version 2024.6.4 or later.

Bug fixes

We've fixed the following bugs:

We've fixed an issue where importing projects containing Repeater tabs within tab groups sometimes failed.

We've fixed an issue that was causing the API parser to incorrectly identify YAML files as JSON.

Java update

We've updated Java from 21.0.4 to 22.0.2
