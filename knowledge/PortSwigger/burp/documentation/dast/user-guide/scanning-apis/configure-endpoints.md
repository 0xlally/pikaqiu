# Viewing and configuring API endpoints

Source: https://portswigger.net/burp/documentation/dast/user-guide/scanning-apis/configure-endpoints
Fetched: 2026-06-28T09:15:40.684803+00:00

DAST

Viewing and configuring API endpoints

Last updated:

June 18, 2026

Read time:

1 Minute

Cloud

Self-hosted

If you uploaded your API definition as a local file you can view details of its endpoints in the Endpoints tab. Endpoints are automatically populated from your API definition when you upload the file.

You can upload a Postman environment file alongside your Postman Collection. Burp Suite DAST merges the environment variables in the endpoint details.

The Endpoints tab contains the following information:

Request (Postman Collections only) - The name of the request.

Method (Postman Collections and OpenAPI definitions files only) - The HTTP method used by the endpoint.

Operation (SOAP WSDLs only) - The name of the SOAP operation.

Host - The protocol and server hostname.

Path and query - The URL file path and query string.

Content type - The format of the data that will be sent to the API server.

By default, all endpoints are selected for scanning. Use the checkbox to remove an endpoint from scans of the site.

Filtering endpoints

You can filter the endpoints that you see on the Endpoints tab:

To filter by a specific term, enter your search term in the Search for an endpoint field, and click the search icon.

For Postman Collections and OpenAPI definition files, you can use the filter buttons to filter by HTTP method.

After filtering the table, click the top checkbox to select or deselect all filtered endpoints.

Note

Burp Suite DAST can only scan endpoints that meet the requirements for scanning. For information about the criteria, see Requirements for API scanning.
