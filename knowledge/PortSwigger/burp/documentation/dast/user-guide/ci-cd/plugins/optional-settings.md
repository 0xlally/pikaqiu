# Optional settings for the CI/CD integration

Source: https://portswigger.net/burp/documentation/dast/user-guide/ci-cd/plugins/optional-settings
Fetched: 2026-06-28T09:15:35.872497+00:00

DAST

Optional settings for the CI/CD integration

Last updated:

June 18, 2026

Read time:

5 Minutes

In addition to configuring the integration between your CI/CD system and Burp Suite DAST, both the plugins and generic driver provide various optional settings that let you fine-tune how the scan and its results should impact your build pipeline.

In the case of the plugins, these options are controlled using input fields and menus in the custom build steps that they provide. For the generic driver, you specify your settings by appending parameters to the command that triggers the scan. Please refer to the parameter reference guide for details.

Configuring optional settings using the platform plugins

Once you have added the relevant build steps to your pipeline and added your API link and key, you can adjust the following settings directly in the "Burp site-driven scan" or "Burp scan" build step.

Scan definition in JSON format - (available for Burp scans only)

Description

A custom scan definition that you have created in the same JSON format used by the REST API. You can use this option to override the default scan configuration used by a site, or to provide a detailed scan definition for a one-off scan that is not matched with an existing site.

Example

{"name":"Example","scan_configurations":[{"name":"Audit checks - light active","type":"NamedConfiguration"}],"urls":["https://example.com/"]}

Lowest severity issue required to fail the build

Description

The minimum severity of issue that must be found by a scan before the build will fail.

Example

Default: medium

Lowest confidence issue required to fail the build

Description

The minimum issue confidence level that must be found by a scan before the build will fail.

Example

Default: tentative

Lowest number of issues permitted before the build will fail

Description

The number of issues that are permitted before the build will fail.

Example

Default: 0

This means that any issues that exceed the configured severity/confidence threshold will cause the build to fail.

Length of time in seconds to wait before giving up

Description

The maximum number of seconds that the CI/CD system should wait to receive a response from the scan. If no response has been received after the time is up, the build will fail.

Example

Default: 120

Output issues in JSON form (verbose mode) - (available for Burp scans only)

Description

By default, when you view the results of your scan in the console output, only the severity/confidence level, the issue type, and the URL where the issue was found are displayed. However, when verbose mode is enabled, the full issue details are displayed in JSON format.

Example

Default: disabled

Self-signed TLS certificate (public part)

Description

If you normally access Burp Suite DAST over HTTPS (the "Use TLS" option is enabled in your network settings) and you use a self-signed TLS certificate, upload the public part of your certificate here. This must be in X504 base64-encoded format and is usually found in a .pem file.

Scan report file

Description

The location and file name where you want the HTML scan report to be saved. If empty, no scan report will be generated.

Example

$WORKSPACE/scan-report.html

Scan report type

Description

The level of detail that you want to include in the scan report. You can choose either a summary report or detailed report.

Example

Default: detailed

Configuring optional settings using the generic CI/CD driver

To configure optional settings when using the generic CI/CD driver, you append the command that triggers the scan with the corresponding parameters. For more information, please refer to the parameter reference guide.

Overriding the default scan configurations from your CI/CD system

If a "Burp scan" is matched with an existing site, this site's default scan configurations are used. If the scan could not be matched with a site, Burp Scanner's default configuration is used instead. However, you can manually control the scan configuration from your CI/CD system by overriding the scan definition.

To do this, you first need to generate a new scan definition in the same JSON format used by the REST API.

Note

This approach is primarily a workaround for legacy integrations that use the "Burp scan" option. It is much easier to use a site-driven scan instead as this allows you to set the scan configuration you want using the Burp Suite DAST web UI. For more information, see Integration types.

In the browser, go to the API link that you saved after generating the API user. By default, this should be something like:

https://your-enterprise-server.com:8080/api/your-api-key

Click on the entry for the POST /scan endpoint. A dialog opens containing the scan definition toolkit.

Use the various entry fields to set the definition you want. You need to enter at least one target URL, a name for the scan, and the scope. If the entire domain of the site is in scope, just create one scope entry containing the site's top-level URL. Note that if you want the scan to be matched with an existing site, you should keep the site-matching rules in mind when entering these URLs.

Add the scan configurations that you want to use:

To use Burp Suite DAST's built-in scan configurations, select the NamedConfiguration option and enter the relevant configuration name, for example, Audit checks - light active. You need to create a new array item for each scan configuration you want to include.

Alternatively, to use a custom scan configuration, select the CustomConfiguration option and enter the settings that you want to apply in JSON format. The easiest way to do this is to create the configurations you want using Burp Suite Professional or Community Edition, export them, then copy and paste the resulting JSON into this field.

As you make changes to the various input fields, the toolkit automatically generates a corresponding curl command at the bottom of the screen. For example:

curl -vgw "\n" -X POST 'http://your-enterprise-server:8080/api/your-api-key/v0.1/scan' -d '{"name":"Example","scan_configurations":[{"name":"Audit checks - light active","type":"NamedConfiguration"}],"urls":["https://example.com/"]}'

When you're happy with your settings, copy the JSON part of the curl command. This is everything between the single quotation marks after the -d.

Log in to your CI/CD platform as an administrator.

If you're using the Jenkins or TeamCity plugins:

Open your pipeline and edit the Burp scan build step.

Under Scan definition in JSON format, paste the JSON that you copied from the REST API toolkit.

If you're using the generic CI driver:

Save the copied definition in a separate JSON file and append the command that invokes the scan with the parameter --scan-definition=your-definition.json

Save your changes to the build step. The next time the scan is triggered by your pipeline, the new scan definition will be used.

Ignoring issues

When using a "Burp scan", you can configure rules that tell the scan to ignore certain issues or ignore all issues on a particular path.

You do this by adding ignore rules to the build step that outputs the BURP_SCAN_URL as follows:

echo BURP_SCAN_URL = http://your-target-site.com

echo BURP_SCAN_IGNORE_EXACT = (High, Certain) - name @ http://your-target-site.com/example/

echo BURP_SCAN_IGNORE_GLOB = (High, Certain) - name @ http://your-target-site.com/*

echo BURP_SCAN_IGNORE_REGEX = \(High, Certain\) - .+ @ http://your-target-site.com(1|2)/.*

For example, to ignore all issues in the path http://your-target-site.com/example/, you would include the following command:

echo BURP_SCAN_IGNORE_GLOB = * @ http://your-target-site.com/example/

Note that you might need to escape special characters, such as parentheses.
