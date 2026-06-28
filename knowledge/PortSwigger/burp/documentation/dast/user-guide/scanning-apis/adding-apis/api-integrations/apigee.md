# Integrating with Google Apigee

Source: https://portswigger.net/burp/documentation/dast/user-guide/scanning-apis/adding-apis/api-integrations/apigee
Fetched: 2026-06-28T09:15:40.395246+00:00

DAST

Integrating with Google Apigee

Last updated:

June 18, 2026

Read time:

2 Minutes

Cloud

Self-hosted

You can integrate Burp Suite DAST with Google Apigee to automatically discover APIs in your Google Apigee organization.

Note

This integration gives Burp Suite DAST read-only access to Google Apigee. No APIs are created or scanned during the setup process. Once the connection is established, discovered APIs are shown in API finder.

This integration supports Apigee X and Apigee hybrid. It does not support Apigee Edge.

Burp Suite DAST only discovers APIs that have an OpenAPI specification attached to the proxy revision as a resource file. APIs whose specifications are stored in the Apigee Spec Store are not discovered.

Prerequisites

You have Modify Settings permission in Burp Suite DAST.

You have a Google Cloud service account and have a service account email and private key for it.

The service account has the built-in Apigee Read-Only Admin role assigned on the GCP project that contains your Apigee organization.

Connecting to Google Apigee

Go to Settings > Integrations.

On the Google Apigee tile, click Configure.

Click Add integration. The Google Apigee connection details dialog opens.

Enter a name in the Integration name field.

Enter your connection details:

Organization - The name of your Apigee organization.

Service account email - The client_email value from your service account JSON key.

Private key - The private_key value from your service account JSON key. Include the entire PEM block, including the -----BEGIN PRIVATE KEY----- and -----END PRIVATE KEY----- lines.

Enter a schedule for how often you want Burp Suite DAST to check the organization for updates. The minimum interval is 15 minutes.

Click Save.

Once Burp Suite DAST connects to Google Apigee successfully, a confirmation message appears. The connection is then listed on the Integrations page, where you can see its status and how many APIs have been discovered.

To manage the APIs discovered by the integration:

Click View discovered APIs to go to API finder.

Click on an API to review its status.

Select multiple APIs and click Create sites to create an API site for each API. For more information, see Creating sites for added APIs.

When a scheduled update discovers changes to your APIs, you will see a red notification dot in the API finder tab. For more information, see Updating your API sites

Related pages

Discovering APIs from integrations
