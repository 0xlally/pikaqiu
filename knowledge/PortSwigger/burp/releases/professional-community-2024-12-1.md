# Professional / Community 2024.12.1

Source: https://portswigger.net/burp/releases/professional-community-2024-12-1
Fetched: 2026-06-28T09:16:45.894884+00:00

This release introduces the Burp Intruder capture filter, automatic decoding of SMTP messages in Burp Collaborator, improved accuracy of recorded logins and a number of other improvements.

Burp Intruder capture filter

We've added a capture filter to the Burp Intruder attack results window. This enables you to control resource usage by choosing which types of responses Intruder captures during an attack.

For more information, see Filtering attack results - Capture filter.

Automatic decoding of SMTP messages in Burp Collaborator

Burp Collaborator now automatically decodes Base64 and Q-encoded data in SMTP messages, making it easier to analyze email content without manual decoding. This is particularly helpful when testing for email splitting or HTTP Host header vulnerabilities.

Improved accuracy of recorded logins

We've enhanced recorded logins by using aria-label properties to identify elements. The recorder now saves aria-label attributes during login recording, and replays use them to reliably locate elements, even for complex sites or login sequences.

Enhanced extensibility with the Montoya API

We've updated the Montoya API to provide greater flexibility and control when issuing requests from extensions:

You can now customize the Server Name Indication (SNI) field. This facilitates testing scenarios such as HTTP Host header attacks.

You can set custom request timeouts to define the maximum time Burp waits for a complete response after sending a request. This avoids the need to manually adjust the suite-wide timeout.

Performance improvements

We’ve improved Burp’s OpenAPI parsing to enable it to successfully process larger YAML definition files.

Burp Scanner now skips light audits for cookie and header insertion points on static resources, enabling the audit to focus more on finding critical issues. Non-static resources and other insertion points are unaffected.

Quality of life improvements

When parsing an OpenAPI definition for an API-only scan, Burp no longer displays randomly generated values in the Parameters tab. However, these values are still generated and used during the scan for parameters that don’t have values specified in the API definition.

We’ve updated dynamic API authentication by merging the API Key and Custom methods into a single tab. This allows you to configure dynamic API keys, including detected ones, alongside custom auth methods, with the flexibility to specify exactly where each is placed in requests.

Browser upgrade

We've upgraded Burp's browser to Chromium 132.0.6834.84 for Windows & Mac and 132.0.6834.83 for Linux. For more information, see the Chromium release notes.
