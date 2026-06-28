# Parameter reference for the generic CI/CD driver

Source: https://portswigger.net/burp/documentation/dast/user-guide/ci-cd/plugins/generic/parameter-reference
Fetched: 2026-06-28T09:15:35.997162+00:00

DAST

Parameter reference for the generic CI/CD driver

Last updated:

June 18, 2026

Read time:

4 Minutes

When using the generic, platform-agnostic CI/CD driver to integrate a Burp Suite DAST scan into your pipelines, you control the various options using command line parameters.

For example, a typical command to trigger a site-driven scan might look something like this:

java -jar path/to/ci-driver.jar https://your-enterprise-server:8080 --api-key=secret --site-id=7 --min-severity=high --min-confidence=certain --report-file=scan-report.html --report-type=summary

The following parameters are available.

burp_api_url

Site-driven scans

Required

Burp scans

Required

Description

The full URL of your DAST server.

In the case of existing "Burp scans" that you configured using an older version of the driver, you can may also include the API key in this URL, but this will prevent you from generating scan reports. New integrations should add this separately using the --api-key parameter.

Example

Site-driven scan:

https://your-enterprise-server.com:8080

New Burp scan:

https://your-enterprise-server.com:8080

Existing Burp scan:

https://your-enterprise-server.com:8080/api/your-api-key

--api-key

Site-driven scans

Required

Burp scans

Optional

Legacy integrations can omit this parameter and append the API key to the burp_api_url instead. However, this will prevent you from generating scan reports.

Description

The API key that you copied after creating the API user. If you have lost this, you can generate a new key from the Burp Suite DAST web UI.

Example

--api-key=secret

--site-id

Site-driven scans

Required

Burp scans

Not permitted

Description

The ID of the site in Burp Suite DAST that you want to scan. You can find this ID in the URL when viewing the site on web UI:

https://your-enterprise-server.com:8080/sites/<site-id>

If this parameter is included, the driver will trigger a site-driven scan, otherwise it will trigger a Burp scan.

Example

--site-id=7

--min-severity

Site-driven scans

Optional

Burp scans

Optional

Description

The minimum severity of issue that must be found by a scan before the build will fail.

Example

--min-severity=high

Default: medium

Permitted values: high, medium, low, info, undefined, false_positive

--min-confidence

Site-driven scans

Optional

Burp scans

Optional

Description

The minimum issue confidence level that must be found by a scan before the build will fail.

Example

--min-confidence=certain

Default: tentative

Permitted values: certain, firm, tentative, undefined

--min-issues

Site-driven scans

Optional

Burp scans

Optional

Description

The number of issues that are permitted before the build will fail.

Example

--min-issues=5

Default: 0

--timeout

Site-driven scans

Optional

Burp scans

Optional

Description

The maximum number of seconds that the CI/CD system should wait to receive a response from the scan. If no response has been received after the time is up, the build will fail.

Example

--timeout=60

Default: 120

--scan-definition

Site-driven scans

Not permitted

Burp scans

Optional

Description

The location of a custom scan definition that you have created in the same JSON format used by the REST API. You can use this option to override the default scan configuration used by a site, or to provide a detailed scan configuration for a one-off scan that is not matched with an existing site.

Example

--scan-definition=your-definition.json

--named-scan-configuration

Site-driven scans

Not permitted

Burp scans

Optional

Description

The name of a built-in scan configuration that you want to use. You can enter this parameter multiple times to use more than one scan configuration.

Example

--named-scan-configuration="Audit checks - light"

--list-named-scan-configuration

Site-driven scans

N/A

Burp scans

N/A

Description

Outputs a list of all built-in scan configurations from Burp Suite DAST and exits.

Example

N/A

--custom-scan-configuration

Site-driven scans

Not permitted

Burp scans

Optional

Description

The location of a JSON file containing a custom scan configuration that you want to use.

You can enter this parameter multiple times to use more than one custom scan configuration.

Example

--custom-scan-configuration=your-configuration.json

--json

Site-driven scans

Not permitted

Burp scans

Optional

Description

Enables verbose mode, which will output the full issue details in JSON format for each issue found.

Example

N/A

--self-signed-cert

Site-driven scans

Optional - depending on network configuration.

Burp scans

Optional - depending on network configuration.

Description

The public part of your self-signed TLS certificate. This must be in X504 base64-encoded format and is usually found in a .pem file.

This is only required if you normally access Burp Suite DAST over HTTPS (the Use TLS option is enabled in your network settings) and you use a self-signed certificate.

Example

--self-signed-cert=your-certificate.pem

--report-file

Site-driven scans

Optional

Burp scans

Optional

Description

The location and file name where you want the HTML scan report to be saved. If unspecified, no report will be generated.

Example

--report-file=scan-report.html

--report-type

Site-driven scans

Optional

Burp scans

Optional

Description

The type of scan report that you want to generate. This can either be a summary or detailed report.

Example

--report-type=summary

--help

Site-driven scans

N/A

Burp scans

N/A

Description

Outputs the built-in help text and exits.

Example

N/A

--version

Site-driven scans

N/A

Burp scans

N/A

Description

Outputs the version number of the driver and exits.

Example

N/A
