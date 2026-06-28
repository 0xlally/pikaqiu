# Running API-only scans

Source: https://portswigger.net/burp/documentation/desktop/running-scans/api-scans
Fetched: 2026-06-28T09:15:52.260961+00:00

Support Center

Documentation

Desktop editions

Running scans

Scanning APIs

Professional

Running API-only scans

Last updated:

June 18, 2026

Read time:

5 Minutes

You can upload an OpenAPI definition, SOAP WSDL, or a Postman Collection to run a specific API scan.

Note

This section explains how to run and configure API-only scans in Burp Suite Professional.

For information on scanning APIs in Burp Suite DAST, see Scanning APIs.

Step 1: Configure scan type

To start an API-only scan:

Click New scan on the Dashboard. The scan launcher opens.

In the Scan type tab, select API-only scan.

Once you have specified scan details, select the API definition tab.

Step 2: Upload API definition

To begin configuring your scan, upload an OpenAPI definition, SOAP WSDL, or a Postman Collection in the API definition tab. You can do this in two ways:

By providing a URL for the API definition. To do this, enter the URL in the Upload from URL field, then click Upload.

By uploading a definition file. To do this, drag and drop the API definition file into the Upload from file field.

Burp uploads the definition and analyzes it to identify the API details that will be used in the scan. To review the API endpoints, click Next.

Note

Burp Scanner must be able to parse and validate definitions in order to upload them. For a full list of criteria that the definition is validated against, see Requirements for API scanning - API definition requirements.

Step 3: Review and configure the API details

You can view API endpoints, authentication methods, and parameters in tables in the API details tab. These are automatically populated from your API definition.

Note

You can customize and sort the API detail tables, and copy column data to your clipboard. For more information, see Customizing Burp's tables.

Viewing and configuring endpoints

API endpoints are listed in a table in the API details > Endpoints tab. The table contains the following columns:

Checkbox - Marks whether the endpoint is selected for scanning. Burp Scanner only scans selected endpoints.

Method -

For OpenAPI, the HTTP method used by the endpoint.

For SOAP, the name of the SOAP operation.

For Postman, the name of the request.

Content type - The format of the data that will be sent to the API server.

Host - The protocol and server hostname.

URL - The URL file path and query string.

By default, all endpoints are selected for scanning. To remove an endpoint from the scan, use the checkbox.

To permanently delete an endpoint, right-click it and select Delete.

You can filter the table by HTTP method or a specific term:

To filter by the HTTP method, use the filter buttons.

To filter by a specific term, click Search, then enter your search term.

Once you've filtered the table, you can deselect or select all filtered endpoints as a bulk action, using the top checkbox.

Note

Endpoints are only listed on the table if they meet the requirements for scanning. For information about the criteria, see Requirements for API scanning.

Viewing and configuring authentication

For OpenAPI definitions and Postman Collections, Burp automatically detects authentication methods when parsing the definition.

These are listed in the API details > Authentication tab, where you can add credentials to enable Burp to use them during the scan. You can also add new authentication methods.

For SOAP WSDLs, Burp doesn't currently detect authentication methods. You'll need to add authentication methods and their credentials to enable Burp to use them during the scan.

For more information, see Configuring authentication for API scans.

Viewing parameters

API parameters for all selected endpoints are listed in a table in the API details > Parameters tab. You can review these to better understand the scope of your scan.

Note

If you deselect or delete an endpoint, Burp automatically removes any corresponding parameters from the Parameters tab.

The table contains details of parameters in the following columns:

Name - The name of the parameter as defined in the API definition.

Values - One or more values taken from the example values for this parameter in the API definition. (If no values are specified in the API definition, Burp randomly generates them as needed during the

scan. These generated values don't appear in the table.)

Description (OpenAPI only) - The parameter description from the API definition.

Method -

For SOAP, the name of the method that the parameter belongs to.

For Postman, the name of the request that the parameter belongs to.

Location - Where the API parameter is located in an HTTP request, as defined in the API definition. For example, the request body, or query string.

Burp Scanner uses the parameter details to create requests when it audits an endpoint.

Once you have finalized the endpoints you want to scan and reviewed the parameters, click Next to select a scan configuration.

Step 4: Select a scan configuration

Scan configurations are collections of settings that define how a scan runs. Click Scan to start the scan with the default configuration, or select and edit a scan configuration. You have the following options:

Set up a new configuration - You can either use a ready-made preset and start scanning immediately, or customize your own.

Load a configuration - Choose an existing configuration from your configuration library.

When you've selected your scan configuration, click Scan to start the scan, or click on the Resource pool tab to choose a resource pool.

Related pages

Configuring scans in Burp Suite Professional - Detailed information on how to configure your scan.

Scan configurations (Burp Scanner) - Reference material on preset and custom scan configurations, as well as the settings available in custom scan configurations.

Importing custom configurations - How to import scan configurations from other installations of Burp into your configuration library.

Step 5: Select a resource pool

A resource pool is a group of tasks that share a quota of network resources. The default resource pool is automatically selected. You can change this in the Resource pools tab:

To use a resource pool that already exists, select Use existing resource pool, then choose a pool from the list.

To set up a new resource pool, select Create new resource pool. For more information on how to configure the pool settings, see Tasks settings - Resource pools.

Related pages

Managing resource pools for scans - Gives information on the use cases for resource pools and how to configure them.
