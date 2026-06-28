# Bulk uploading APIs

Source: https://portswigger.net/burp/documentation/dast/user-guide/scanning-apis/adding-apis/bulk-uploading-apis
Fetched: 2026-06-28T09:15:40.650869+00:00

DAST

Bulk uploading APIs

Last updated:

June 18, 2026

Read time:

3 Minutes

Cloud

Self-hosted

You can create multiple API sites in one operation. Each file or URL creates its own site. Bulk uploading speeds up the process of onboarding large numbers of APIs and enables consistent configuration across your API estate.

You can bulk import APIs in two ways:

From the Sites menu, select Bulk upload APIs to import API definition files or URLs.

From the API finder menu, select one or more APIs and click Create sites. For more information, see Creating sites for added APIs.

Before you start

Make sure you have the API definition files ready or know the URLs where they are hosted. You can upload a mix of Postman Collections, OpenAPI definitions, and SOAP WSDL files.

Note

You must have permission to scan all URLs included in the scope of the imported sites.

How to bulk upload APIs

To bulk upload your APIs, complete the following steps:

Update behavior

Burp Suite DAST only shows this step when you create sites from the API finder menu.

Choose how API updates are applied:

Always review changes before updating - The notification dot is shown on the API finder menu when changes to the API definitions are detected. You can review the changes and update your sites manually.

Automatically keep APIs up to date - New versions of API definitions are applied to your sites automatically.

Click Next.

Import type

Burp Suite DAST only shows this step when you create sites from the Sites menu.

Choose how to add your API definitions:

Upload files - Select API definition files from your local machine. Click Upload more files to add additional files.

Host URLs - Paste a list of links to the URLs of your API definition files.

If you want to remove any of the uploaded files, select the tick boxes and click Delete.

Click Next.

Select methods

Burp Suite DAST only shows this step when you create sites from the API finder menu.

Choose the request methods to enable for this import. These also apply endpoints discovered in future automatic updates:

GET

POST

PUT

DELETE

Other - Includes PATCH, HEAD, OPTIONS, and any non-standard methods.

Click Next.

Choose folder

Select a destination folder for the imported sites.

Click Next.

Network

Configure the network settings that apply to all imported sites:

Self-hosted Scanning pool - Select which scanning pool to use.

Upstream proxy servers (optional) - Add upstream proxy server rules if needed.

Headers and cookies (optional) - Add custom headers and cookies to requests.

Click Next.

Review upload

This step only appears when you create sites from the Sites menu.

Review the sites that will be created. Make any necessary changes.

To remove one or more sites, select their tick boxes and click Delete.

If any sites failed parsing, download the log to view more details about the errors.

Click Next.

Authentication

You can view detected authentication types for your sites, or add them. Any authentication you add manually applies to all sites in this bulk upload.

To add authentication credentials:

Click Add more.

Select Basic, Bearer auth, API key / Custom token, or OAuth 2.0 client credentials.

Enter the details for the chosen authentication method.

Click Save.

To edit authentication credentials, click the pencil icon.

Click Next.

Scan configuration

Choose the scan configuration:

Default configuration - Uses the default scan configuration for API sites. If the parent folder has scan configurations applied, your sites inherit those configurations instead.

Use a custom configuration - Select a custom scan configuration.

Under Extensions, select the BChecks and custom extensions you want to use. Click Select all BChecks to use all available checks.

Click Import.

Burp Suite DAST creates a separate site for each API definition and adds them to the site tree in the selected folder.

After bulk upload

After importing your APIs, you can:

Add or update authentication credentials for individual sites.

Fine-tune scan configurations for specific sites.

Schedule scans for your imported sites.

For more information, see Configuring site settings.

Related pages

Scanning APIs

Adding a single API

Creating sites for added APIs

Configuring API authentication
