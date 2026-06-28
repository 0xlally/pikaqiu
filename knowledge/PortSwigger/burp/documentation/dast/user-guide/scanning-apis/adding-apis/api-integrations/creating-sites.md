# Creating sites for added APIs

Source: https://portswigger.net/burp/documentation/dast/user-guide/scanning-apis/adding-apis/api-integrations/creating-sites
Fetched: 2026-06-28T09:15:40.522355+00:00

DAST

Creating sites for added APIs

Last updated:

June 18, 2026

Read time:

3 Minutes

Cloud

Self-hosted

When Burp Suite DAST discovers APIs through an integration, they appear in the New tab in API finder. You need to review these APIs and create sites for the ones you want to scan. APIs that you don't want to scan can be ignored.

Note

When APIs are waiting for your review, a red dot appears on the API finder menu item.

Creating API sites

To review and create sites for discovered APIs, select API finder in the navigation bar.

The New tab lists the APIs that Burp Suite DAST has discovered. For each API, you can see:

The API type (REST, SOAP, or GraphQL).

The number of endpoints. Click this to view the individual endpoints and their HTTP methods.

The date the API was discovered.

The source: the integration the API came from. Click this to view the connection details.

Viewing API endpoints

To view the endpoints for an API, click the endpoint count. A panel shows each endpoint's HTTP method, host, path, and content type. You can filter by HTTP method or search for a specific endpoint.

To create a site directly from this panel, click Create site from API.

Creating a site for a single API

To create a site for a single API:

Click the Create site icon in the

Actions column of the API.

Click Continue to configure the site.

For more information, see Bulk uploading APIs.

Burp Suite DAST creates a site for the API and adds it to the site tree. The API moves to the Onboarded tab.

Creating sites for multiple APIs

To create sites for multiple APIs at once:

Select the checkboxes next to the APIs you want to create sites for.

Click Create sites in the action bar that appears at the bottom of the page.

Click Continue to configure the sites. For more information, see Bulk uploading APIs.

Burp Suite DAST creates a site for each selected API and adds them to the site tree. The APIs move to the Onboarded tab.

Viewing onboarded APIs

The Onboarded tab lists APIs that have been turned into scan sites. For each API, you can see the source integration and a link to the site in the site tree.

Ignoring APIs

If you don't want to create a site for an API, you can ignore it. Ignored APIs move to the Ignored tab and no longer appear in the New tab.

To ignore a single API, click the Ignore icon in the Actions column.

To ignore multiple APIs at once:

Select the checkboxes next to the APIs you want to ignore.

Click Ignore in the action bar that appears at the bottom of the page.

Restoring ignored APIs

You can restore ignored APIs and move them back to the New tab if you want to create sites for them later.

To restore a single API, click the Restore icon in the Actions column on the Ignored tab.

To restore multiple APIs at once:

Go to the Ignored tab.

Select the checkboxes next to the APIs you want to restore.

Click Revert.

Related pages

Managing your APIs

Updating your API sites

Bulk uploading APIs
