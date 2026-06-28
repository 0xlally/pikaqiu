# Configuring API authentication

Source: https://portswigger.net/burp/documentation/dast/user-guide/scanning-apis/configuring-api-authentication
Fetched: 2026-06-28T09:15:40.702096+00:00

DAST

Configuring API authentication

Last updated:

June 18, 2026

Read time:

6 Minutes

Cloud

Self-hosted

Host credentials vs API authentication

When working with API definitions, you may need to provide two different types of credentials:

Host credentials - Optional credentials used to access the API definition file if it's hosted on a server that requires authentication. These are only used when fetching the definition file from a URL.

API authentication - Credentials used to authenticate requests to the API endpoints during scanning. These are configured as described on this page.

This page explains how to configure API authentication for scanning your API endpoints.

Supported authentication types

Burp Suite DAST supports the following authentication:

Basic - Enter a username and password.

Bearer Token - Adds an access token that's sent in the authorization header.

API Key / Custom token - Adds an API key or access token in a custom location.

OAuth 2.0 Client Credentials - Automatically obtains and refreshes access tokens using OAuth 2.0.

If you upload a Postman file that contains these authentication types, Burp Suite DAST extracts the credentials automatically. You can see the extracted information in the

Authentication tab.

You can also use dynamic tokens. These tokens have a limited lifespan. Burp Suite DAST enables you to fetch refreshed tokens automatically.

Note

For security reasons, API definitions should include authentication schemes but not the associated credentials. For example, a definition can define that a particular API key is needed, but it must not provide the API key.

This means that you need to add credentials for any detected schemes manually. Schemes that have been detected but not yet populated with credentials have a red notification dot next to them. To add a credential to a scheme, click its pencil icon.

Authentication status overview

Burp Suite DAST allows you to save sites with detected authentication schemes, even if the credentials aren't supplied.

Sites with missing credentials display the following:

Warning banners inform you during site creation and editing.

Visual indicators help you identify sites needing authentication.

You can complete authentication configuration at any time.

Adding basic authentication

To add basic authentication:

Select the Authentication tab.

Click Add API authentication to display the Add authentication dialog.

Select Basic.

Enter the Label, Username, and Password.

Click Save.

Adding Bearer token authentication

To add Bearer token authentication:

Select the Authentication tab.

Click Add API authentication to display the Add authentication dialog.

Select Bearer token.

For Fixed tokens:

Set the Token type to Fixed.

Enter the Label and Token.

Click Save.

For Dynamic tokens:

Set the Token type to Dynamic.

Enter a Label for the token (for example, "Auth Token").

Enter the Authentication service URL (for example, https://api.example.com/auth) and Method for the request to retrieve the token.

If necessary, expand Additional headers and enter the Name and Value for each header. Click to add more headers.

In the Body field, if necessary, enter the body of the request. For example, for a JSON request:

{

"username": "user123",

"password": "securePassword"

}

For application/x-www-form-urlencoded content type, you must set the Content-Type header in Additional headers, then enter the body accordingly:

grant_type=client_credentials&client_id=abc123&client_secret=xyz456

Enter a value for how often the token should be refreshed in the Re-fetch every field. This ensures that the scanner always uses a valid token for API requests.

In the Token location field, enter the location in the response body where the token will be located. For JSON responses, use the field name or dot separated names. For XML responses, use XPath. Leave blank to use the entire response body as the token.

For example, if the response body contains:

{

"token": "abc123xyz",

"expires_in": 3600

}

You would enter token as the token location.

Click Save.

Note

Although Burp Scanner does not officially support OAuth authentication for API scanning, it does have a workaround for the Bearer auth type. You can set it up using the Bearer auth dynamic token type in Burp Suite DAST, as long as the token is included in the Authorization header. The only difference from the standard Bearer auth setup is that you cannot specify the header name, since the Authorization header is used by default for Bearer auth.

Adding API key / custom token authentication

To add credentials for an API key, or add a token in a custom location:

Select the Authentication tab.

Click Add API authentication to display the Add authentication dialog.

Select API key / Custom token.

For Fixed tokens:

Set the Token type to Fixed.

Enter the Label, Location, and Key / token.

Click Save.

For Dynamic tokens:

Set the Token type to Dynamic.

Enter a Label for the token (for example, "Auth Token"), and choose a location from the Add to drop-down list to specify where the token should be added (for example, Header, Query Parameter, or Cookie).

Enter the Authentication service URL (for example, https://api.example.com/auth) and Method (for example, POST or GET) for the request to retrieve the token.

If necessary, expand Additional headers and enter the Name and Value for each header (for example, Content-Type: application/x-www-form-urlencoded). Click to add more headers.

In the Body field, if necessary, enter the body of the request. For example, for a JSON request:

{

"username": "user123",

"password": "securePassword"

}

For application/x-www-form-urlencoded content type, you must set the Content-Type header in Additional headers, then enter the body accordingly:

grant_type=client_credentials&client_id=abc123&client_secret=xyz456

Enter a value for how often the token should be refreshed in the Re-fetch every field (for example, every 30 minutes). This ensures that the scanner always uses a valid token for API requests.

In the Token location field, enter the location in the response body where the token will be located. For JSON responses, use the field name or dot separated names. For XML responses, use XPath. Leave blank to use the entire response body as the token.

For example, if the response body contains:

{

"token": "abc123xyz",

"expires_in": 3600

}

You would enter token as the token location.

Click Save.

Adding OAuth 2.0 client credentials authentication

To add OAuth 2.0 client credentials authentication:

Select the Authentication tab.

Click Add API authentication to display the Add authentication dialog.

Select OAuth 2.0 client credentials.

Enter a Label for the authentication.

Enter your Token URL. This is the OAuth 2.0 token endpoint.

Enter your Client ID.

Enter your Client secret.

Expand Advanced settings to configure optional settings:

Scope - Enter a space-separated list of OAuth 2.0 scopes if required by your API.

Authentication method - Select how credentials are sent. Choose POST (credentials in body) or HTTP Basic.

Refresh interval (seconds) - Set how often to refresh the token. The default is 3300 seconds (55 minutes). You can set a value between 60 and 86400 seconds.

Click Save.

Editing or deleting authentication methods

To edit an existing authentication method, click its pencil icon.

To delete an existing authentication method, click its trash icon.

Note

In order to modify authentication details for an API site after the site has been saved, you need Edit site application logins permission. This includes changing the specification upload method between a URL and a local file. Note that admin users have this permission by default.

If you have View site application logins permission but not Edit site application login details permission, you can see details of the authentication methods used in the specification and their credentials. However, you can't edit any of them, add new authentication, amend the selection of endpoints to scan, or change the API definition file or URL.

Scanning with incomplete authentication

You will see a warning if you create scans that include sites with incomplete authentication. You can still run your scan, but areas that require authentication may not be tested.

Related pages

Managing scheduled scans - explains how to schedule scans for your new site.

Defining scan configuration for a site - explains how to create and work with scan configurations.

Configuring site settings - explains the optional scan settings you can configure for a site.

Configuring your environment network and firewall settings.

Burp Scanner built-in configurations - reference information on Burp Scanner's built-in scan configurations.
