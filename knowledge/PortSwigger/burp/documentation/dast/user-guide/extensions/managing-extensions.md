# Managing extensions in Burp Suite DAST

Source: https://portswigger.net/burp/documentation/dast/user-guide/extensions/managing-extensions
Fetched: 2026-06-28T09:15:36.450008+00:00

DAST

Managing extensions in Burp Suite DAST

Last updated:

June 18, 2026

Read time:

2 Minutes

This page explains how to view and remove existing extensions.

To display a list of current extensions:

Log in to Burp Suite DAST as a user with permission to manage extensions.

From the settings menu , select Extensions to go to the Extension library.

Move between the different tabs to view the BChecks, BApps, and custom extensions that are available in your Burp Suite DAST Extension library.

Learn more about Adding extensions to Burp Suite DAST.

Viewing extension details

In the relevant tab of the Extension library, click the info icon in the Name column to see a description of that extension.

Updating an extension

You can manually update your existing custom extensions and BChecks. This can be useful if you make changes to an extension or download a newer version of it.

When you update an extension, it's replaced by the updated version in all sites and folders where the original version was applied.

Note

BApps do not require manual updates. When the latest version of a BApp is published to the BApp Store, it will automatically be updated in Burp Suite DAST.

To update an extension:

In the relevant tab of the Extension library, click the update icon of the extension you want to update.

Select the file that you want to use to update the extension.

Custom extensions must be JAR files, and BChecks must have a .bcheck extension.

Deleting an extension

In the relevant tab of the Extension library, click the trash icon to delete that extension. This completely removes the extension from Burp Suite DAST, meaning it is no longer

available for selection when editing or creating a site. It also removes the extension from any sites that it was applied to.

Note

If you remove an extension while a scan is in progress, the scan continues to use the extension until it finishes.
