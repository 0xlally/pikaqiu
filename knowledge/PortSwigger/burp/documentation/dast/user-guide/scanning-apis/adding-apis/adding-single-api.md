# Adding a single API

Source: https://portswigger.net/burp/documentation/dast/user-guide/scanning-apis/adding-apis/adding-single-api
Fetched: 2026-06-28T09:15:39.990856+00:00

DAST

Adding a single API

Last updated:

June 18, 2026

Read time:

2 Minutes

Cloud

Self-hosted

This page explains how to create a site for a single API. You can add an API definition by uploading a file or providing a URL.

Adding API definitions by uploading a file

When you upload an API definition file, Burp Suite DAST uses that version for every scan until you upload a new one. You can't upload GraphQL API definition files.

To add an API definition by uploading a file:

Go to Sites and select Add a new site.

Select API from the Site type panel.

Enter a unique Site name.

To add the site to an existing folder, select from the Site folder drop-down menu.

Leave the field blank to create the site at the top level of the site tree.

Click Select file and select the definition file to upload.

If you upload a Postman Collection, you are given the option to upload a Postman environment file. Burp Suite DAST merges the environment variables with your Postman Collection. Click Add environment file and select your environment file.

Adding API definitions by providing a URL

When you provide a URL, Burp Suite DAST uses the latest version of the API definition for every scan. If the definition file is on a server that requires authentication, you can add host credentials. You can validate that the URL is reachable and the file can be parsed.

To add an API definition by providing a URL:

Go to Sites and select Add a new site.

Select API from the Site type panel.

Enter a unique Site name.

To add the site to an existing folder, select from the Site folder drop-down.

Leave the field blank to create the site at the top level of the site tree.

Click Host URL and enter the URL where your API definition file is hosted.

(Optional) If your API definition file is on a server that requires authentication, click Add host credentials and enter the credentials.

Click Validate to confirm that Burp Suite DAST can reach the URL and parse the API definition.

If successful, the Endpoints tab lists the parsed endpoints.

Note

If you provide a URL for a Postman Collection, Burp Suite DAST also extracts the credentials for detected authentication schemes. They are shown in the Authentication tab.

If you manually edit the credentials for your site, they may be overwritten if you later click Validate.

Saving and scanning your site

Once you've finished creating your site, click Save.

Burp Suite DAST adds the new API to the site tree and prompts you to schedule a scan.

Related pages

Scanning APIs

Creating sites for added APIs - If you use integrations to discover APIs, you can create sites directly from API finder.

Configuring API authentication

Viewing and configuring API endpoints
