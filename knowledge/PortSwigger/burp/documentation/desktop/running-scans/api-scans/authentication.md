# Configuring authentication for API scans

Source: https://portswigger.net/burp/documentation/desktop/running-scans/api-scans/authentication
Fetched: 2026-06-28T09:15:52.337056+00:00

Support Center

Documentation

Desktop editions

Running scans

Scanning APIs

Configuring authentication

Professional

Configuring authentication for API scans

Last updated:

June 18, 2026

Read time:

8 Minutes

This topic explains how to configure authentication for API-only scans in Burp Suite Professional.

Setting up authentication credentials enables Burp Scanner to access restricted API endpoints, which are often the most critical parts of your API's attack surface. Burp currently supports the following authentication types:

Basic authentication

Bearer tokens

API keys

After you upload an API definition, you can view, add, and edit authentication methods in the API details > Authentication tab.

Detected authentication methods

When you upload an OpenAPI definition or a Postman Collection, Burp parses it to identify its endpoints and detect any specified authentication methods. If Burp detects authentication methods, it adds them to the API

details >

Authentication tab, and labels them:

Detected: Supported by Burp. Can be used during the scan after adding credentials.

Unsupported: Not supported by Burp. Can't be used during the scan.

Note

Burp only detects authentication in OpenAPI definitions. If you're working with a SOAP API, all authentication methods need to be manually added.

Adding authentication methods

After you upload your API definition, you can manually add authentication methods for Burp to use when scanning your API.

Basic authentication

To add a basic authentication method:

Go to API details > Authentication.

Click New. The Add authentication window opens.

Type: Select Basic auth.

Label: Enter a unique identifier for this authentication method. Choose a name that makes it easy to recognize.

Add to: Specifies where Burp adds the credentials to requests it sends during the scan. This is always set to Authorization header for basic authentication.

Username: Enter a username for Burp to use during the scan.

Password: Enter a password for Burp to use during the scan.

Click Save. The new authentication method is now added to the list.

Bearer token

You can use fixed or dynamic tokens for bearer token authentication.

Fixed bearer token

Fixed tokens are tokens that do not expire. Select this option if your token has a long lifespan or doesn't expire. You provide the token manually, and Burp includes this exact token in relevant requests it sends during the scan.

To add a fixed bearer token:

Go to API details > Authentication.

Click New. The Add authentication window opens.

Type: Select Bearer token.

Label: Enter a unique identifier for this authentication method. Choose a name that makes it easy to recognize.

Add to: Specifies where Burp adds the token to requests it sends during the scan. This is always set to Authorization header for bearer tokens.

Token type: Select Fixed.

Token: Enter a token for Burp to use during the scan.

Click Save. The new authentication method is now added to the list.

Dynamic bearer token

Dynamic tokens are short-lived tokens that need to be renewed regularly. Select this option if your token has a limited lifespan. Burp automatically requests new tokens from the API at defined intervals during the scan, and includes the most recent token in relevant requests.

Note

You may need to refer to your API documentation when configuring dynamic bearer tokens.

To add a dynamic bearer token:

Go to API details > Authentication.

Click New. The Add authentication window opens.

Type: Select Bearer token.

Label: Enter a unique identifier for this authentication method. Choose a name that makes it easy to recognize.

Add to: Specifies where Burp adds the token to requests it sends during the scan. This is always set to Authorization header for bearer tokens.

Token type: Select Dynamic.

Authentication service URL: Specify the URL of the endpoint used for retrieving or refreshing tokens from your API, for example: https://authservice.com/auth/token. Burp sends token retrieval requests to this URL.

Method: Select the method you want Burp to use for token retrieval requests.

Add header: If token retrieval requests require specific headers, click Add header, then enter its Name and Value. You can add multiple headers if needed.

Body: Enter the full request body required for token retrieval. Include all mandatory fields, and use the format specified by your authentication service.

Request new token every: Specify how often Burp requests a new key or token during the scan, based on how long it remains valid. For example, if it expires every hour, set the interval to one hour.

Burp will then request a new key / token half a second before the current one expires.

Token location: Specify where you want Burp to look when extracting the token from the authentication service's response:

If the token is in a JSON response, use dot-separated names to specify the exact field name. For example, token.access_token.

If the token is in an XML response, use an XPath expression to specify the token's location. For example, /response/token.

If you want to use the entire response as the token, leave this field blank.

Test: (Optional) To verify your configuration, click Test. Burp sends a request using your settings and confirms whether a token can be successfully extracted from the response.

Click Save. The new authentication method is now added to the list.

API key / Custom token

The API key / Custom token authentication method enables you to configure either an API key or a custom token, and specify exactly where this credential should appear in requests Burp sends during the scan.

You can use fixed or dynamic keys / tokens.

Fixed API key / Custom token authentication method

Fixed API keys / custom tokens do not expire. Select this option if your key / token has a long lifespan or doesn't expire. You provide the key / token manually, and Burp includes this exact credential in relevant requests during the scan.

To add a fixed API key / custom token authentication method:

Go to API details > Authentication.

Click New. The Add authentication window opens.

Type: Select API key / Custom token.

Label: Enter a unique identifier for this authentication method. Choose a name that makes it easy to recognize.

Add to: Specify where Burp adds the key / token to requests it sends during the scan.

Name: Enter the name of the header, query parameter, or cookie you selected in the Add to drop-down.

Key / token type: Select Fixed.

Key / token: Enter a key / token for Burp to use during the scan.

Click Save. The new authentication method is now added to the list.

Dynamic API Key / Custom token authentication method

Dynamic API keys / custom tokens are short-lived and need to be renewed regularly. Select this option if your key / token has a limited lifespan. Burp automatically requests new keys / tokens from the API at defined intervals during the scan, and includes the most recent one in relevant requests during the scan.

To add a dynamic API key / custom token authentication method:

Go to API details > Authentication.

Click New. The Add authentication window opens.

Type: Select API key / Custom token.

Label: Enter a unique identifier for this authentication method. Choose a name that makes it easy to recognize.

Add to: Specify where Burp adds the key / token to requests it sends during the scan.

Name: Enter the name of the header, query parameter, or cookie you selected in the Add to drop-down.

Token type: Select Dynamic.

Authentication service URL: Specify the URL of the endpoint used for retrieving or refreshing keys / tokens from your API, for example: https://authservice.com/auth/token. Burp sends key / token

retrieval requests to this URL.

Method: Select the method you want Burp to use for key / token retrieval requests.

Add header: If key / token retrieval requests require specific headers, click Add header, then enter its Name and Value. You can add multiple headers if needed.

Body: Enter the full request body required for key / token retrieval. Include all mandatory fields, and use the format specified by your authentication service.

Request new token every: Specify how often Burp requests a new key or token during the scan, based on how long it remains valid. For example, if it expires every hour, set the interval to one hour.

Burp will then request a new key / token half a second before the current one expires.

Key / token location: Specify where you want Burp to look when extracting the key / token from the authentication service's response:

If the key / token is in a JSON response, use dot-separated names to specify the exact field name. For example, token.access_token.

If the key / token is in an XML response, use an XPath expression to specify its location. For example, /response/token.

If you want to use the entire response as the key / token, leave this field blank.

Test: (Optional) To verify your configuration, click Test. Burp sends a request using your settings and confirms whether a token can be successfully extracted from the response.

Click Save. The new authentication method is now added to the list.

Editing authentication credentials / methods

You can make changes to any supported authentication methods. These include methods labeled Detected, and methods that you added manually.

To edit an authentication method:

Select the method in the table and click Edit. This opens the Edit Authentication window.

Update the editable fields. The fields you can update depend on how the method was added:

If the method was detected by Burp, you can only edit its credentials.

If the method was added manually, you can edit any of your supplied configuration values.

Click Save to confirm your changes. The credentials are applied to the authentication method.

To learn how to configure the different types of authentication methods, including dynamic tokens, see: Adding authentication methods.

How Burp applies authentication credentials

When Burp scans your API, it adds authentication credentials to its requests. However, conflicts can arise if multiple methods target the same part of a request. For example:

API keys may conflict if they share the same header or cookie name.

Basic authentication and bearer tokens may clash because both send credentials in the Authorization header.

These conflicts can result in invalid credentials being sent, which causes the server to deny the request. To prevent this from happening, Burp applies the following logic:

Conflicts between manually added methods

Burp prevents you from saving new authentication methods that conflict with ones you've already added. This ensures that manually added methods don't interfere with each other.

Conflicts between detected methods and manually added methods

Burp allows you to manually add authentication methods, even if they conflict with Detected methods. This is because Detected methods

are tied to specific endpoints, as defined in the OpenAPI definition or Postman Collection. Manual

methods, on the other hand, ensure that the scanner is authenticated for all other requests.

To avoid conflicts during the scan:

Credentials for Detected methods are used in requests sent to their linked endpoints.

Credentials for manual methods are used in requests sent to any other endpoints.
