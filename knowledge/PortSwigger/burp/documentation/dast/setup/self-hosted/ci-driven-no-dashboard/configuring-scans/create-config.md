# Creating a configuration file for a CI-driven scan with no dashboard

Source: https://portswigger.net/burp/documentation/dast/setup/self-hosted/ci-driven-no-dashboard/configuring-scans/create-config
Fetched: 2026-06-28T09:15:32.479047+00:00

DAST

Creating a configuration file for a CI-driven scan with no dashboard

Last updated:

June 18, 2026

Read time:

6 Minutes

We provide a template configuration file. The file includes comments to help you to understand and edit each of the parameters. After you edit the configuration file, you can rename it to burp_config.yml, to match the integration examples we give in this section.

You can get the template YAML file here (opens in a new tab):

Template configuration file

Mandatory settings

Mandatory settings define what Burp Suite DAST should scan. These settings vary depending on whether you're scanning a web app or an API. If you only define mandatory settings when scanning an API definition, Burp Scanner uses the default scan configuration.

Common requirements

For all CI-driven scans, you must specify a DAST server URL and API key (enterpriseServer.url and enterpriseServer.apiKey). You can find these in your user account.

Web apps

For web app scans, you must provide start URLs (site.startUrls). These are the URLs that Burp Scanner starts scanning from.

APIs

You can add API definitions by either uploading a file (site.apiDefinition.fromFile) or providing a URL (site.apiDefinition.fromUrl). You must provide one of these properties when running a CI-driven scan on an API definition.

For API scans, Burp Suite DAST supports:

Postman Collections

OpenAPI definitions in JSON or YAML format

SOAP WSDLs

Note

Burp Suite DAST scans all endpoints referenced in the API definition file. To exclude endpoints from scans, remove them from the API definition file before running the scan.

We fully support OpenAPI 3.1 and provisionally support OpenAPI 3.2.

Proxy settings

If you need to use a proxy to connect to the PortSwigger licensing server, add the URL and authentication credentials into the following fields. The authentication credentials are optional:

proxyUrl

proxyUsername

proxyPassword

Defining the scope

Burp Scanner only visits URLs that are in scope. Use the YAML file to set the scope of your scan, to make sure Burp Scanner only visits URLs that you have permission to scan. You can also use the scope to focus on particular paths that you're interested in.

To define the scope, enter URLs as values in the site.inScopeUrlPrefixes or site.outOfScopeUrlPrefixes parameters.

Note

The start URLs are automatically added to the site.inScopeUrlPrefixes parameter.

Authentication

You can use authenticated scanning to scan content that is behind authentication. We support the following methods of authentication:

Login credentials (web apps only)

To define login credentials, enter a list of username and password pairs in the logins.loginCredentials setting.

Recorded logins (web apps only)

To define a recorded login sequence:

Record a login sequence and save it to the clipboard.

Save the contents of the clipboard as a JSON file in the same directory as the configuration file.

In the logins.recordedLogins parameter, enter the path to the JSON file.

API authentication (APIs only)

You can manage API authentication for CI-driven scans by adding the authentication details directly into the CI configuration YAML file. Burp Suite DAST supports the following methods of API authentication.

API key authentication

When configuring API key authentication for CI-driven scans, you need to determine whether the authentication method is already defined in your API definition.

If your OpenAPI definition file already includes the authentication scheme, you only need to add the label and key fields to your configuration file, regardless of whether the key is passed in the header, a query parameter, or a cookie.

label: Use the exact label from the API definition file.

key: Enter the API key value required by the API.

For SOAP WSDLs, Postman Collections, or OpenAPI definition files that don't include the authentication scheme, you must define all the necessary fields in your configuration file:

API key in Header:

label: Create a unique name for the authentication scheme. For example, headerAuth1.

type: This must be apiKey.

in: This must be header.

name: Specify the name of the header where the API key will be placed. For example, X-API-Key.

key: Enter the API key value. For example, AKIA9672010EXAMPLE.

API key in Query Parameter:

label: Create a unique name for the authentication scheme. For example, queryAuth1.

type: This must be apiKey.

in: This must be query.

name: Specify the name of the query parameter where the API key will be placed. For example, api_key.

key: Enter the API key value. For example, AKIA7040551EXAMPLE.

API key in Cookie:

label: Create a unique name for the authentication scheme. For example, cookieAuth1.

type: This must be apiKey.

in: This must be cookie.

name: Specify the name of the cookie where the API key will be placed. For example, api_key_cookie.

key: Enter the API key value. For example, AKIA1329734EXAMPLE.

HTTP authentication types

When configuring HTTP authentication for CI-driven scans, you need to determine whether the authentication method is already defined in your API definition.

If your API definition file already includes the HTTP authentication scheme, you only need to add the label, username, and password (for Basic Authentication) or the label and token (for Bearer Token) fields to your configuration file:

Basic Authentication:

label: Use the exact label from the API definition file.

username: Specify the username required by the API.

password: Specify the corresponding password.

Bearer Token Authentication:

label: Use the exact label from the API definition file.

token: Specify the bearer token required by the API.

If your API definition file doesn't include the HTTP authentication scheme, you must define all the necessary fields in your configuration file:

Basic Authentication:

label: Create a unique name for the authentication scheme. For example, basicAuth1.

type: This must be http.

scheme: This must be basic.

username: Specify the username required by the API. For example, carlos@portswigger.net.

password: Specify the corresponding password for the username.

Bearer Token Authentication:

label: Create a unique name for the authentication scheme. For example, bearerAuth1.

type: This must be http.

scheme: This must be bearer.

token: Specify the bearer token required by the API. For example, f5cCI6iCJ9.eyJzdWIiOiIxMjM0... (this is a shortened example, actual tokens are generally much longer).

Selecting a built-in scan configuration

You can select from the list of built-in scan configurations. These are the same built-in scan configurations used by Burp Suite DAST and Burp Suite Professional.

If you don't select a built-in scan configuration, the default configuration is used.

To use a built-in scan configuration, enter the name of the configuration in the scanConfigurations.builtIn setting. The configuration names are case-sensitive.

Configuring connection settings

The JSON file contains some parameters that enable you to configure the connection settings used when running CI-driven scans:

headersCookiesConfig enables you to add a list of custom headers and cookies to requests made when scanning a site. This enables you to, for example, configure header authentication. For more information on configuring request headers and cookies, see Adding headers and cookies.

platformAuthentication enables you to add authentication credentials for HTTP Basic and NTLM authentication. For more information on the settings available, see Configuring platform authentication.

proxies enables you to enter a list of upstream proxy servers for the connection to use. For more information on the settings available, see Configuring upstream proxy servers.

Specifying report format

By default, CI-driven scans output reports in JUnit XML format. However, they can also output in Burp XML format if required. Use the reporting.reportFormats parameter to specify the format to use.

Ignoring specific issues

You can ignore specific issues, so that they do not cause the build to fail. Burp Scanner still looks for these issues, and records them in the results. For a list of issue types, see Vulnerabilities detected by Burp Scanner.

Enter the name of the issues in the reporting.ignoredIssues parameter. Names are case-sensitive. If you name an issue and don't supply a path, the issue is ignored everywhere.

We support the use of regex for the paths.

Setting the threshold

You can set a threshold that causes Burp Scanner to tell your CI/CD system to fail the pipeline step.

To enable a threshold, set reporting.threshold.enabled to TRUE. Then enter a minimum severity and a minimum confidence. If Burp Scanner detects an issue with at least this severity and confidence, it finishes with a non-zero exit code.

You can set the reporting.threshold.enabled to:

TRUE

FALSE

You can set the threshold.minimumSeverity to:

INFO

LOW

MEDIUM

HIGH

You can set the threshold.minimumConfidence to:

TENTATIVE

FIRM

CERTAIN

If you don't input values for these parameters, the default values are TRUE, LOW, and

TENTATIVE.

Configuring output detail level

The verboseScanning parameter controls the amount of detail provided in scan output:

When verboseScanning is set to enabled: true, the scan produces detailed output, making it easier to troubleshoot and gain deeper insights into what the scan is doing.

When verboseScanning is set to enabled: false, the scan produces minimal output, showing only the most important information. This mode is useful for routine scans where detailed information is not necessary. This is the default option.

Next step - Adding a configuration file

CONTINUE
