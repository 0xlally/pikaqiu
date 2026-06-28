# Scanning with extensions in Burp Suite DAST

Source: https://portswigger.net/burp/documentation/dast/user-guide/managing-your-sites/site-settings/scanning-with-extensions
Fetched: 2026-06-28T09:15:38.707683+00:00

DAST

Scanning with extensions in Burp Suite DAST

Last updated:

June 18, 2026

Read time:

3 Minutes

Self-hosted

Once your administrator has added an extension to your library, you can apply it to one or more sites. The extension is used whenever a scan runs on that site.

Applying extensions to sites

Apply extensions to your sites to have Burp Suite DAST use them whenever it runs a scan on that site.

Applying extensions to an existing site

To apply extensions to an existing site:

From the Sites page, select the site you want to apply the extension to.

On the Details tab, click Edit .

In Scan settings, go to the Extensions tab, then:

For BChecks: go to the BChecks tab.

For BApps and custom extensions: go to the BApps & custom extensions tab.

Extensions that your system administrator has added to Burp Suite DAST are listed on these tabs.

Select the extensions you want to apply to the site.

Click Save.

The selected extensions are applied to your site.

Note

Using extensions can increase the duration of your scans.

Applying extensions to new sites

You can also apply extensions when you are creating a new site in Burp Suite DAST.

To apply extensions to a new site:

On the Create a new site page, in Site settings, go to the Extensions tab.

On the Details tab, click Edit .

In Scan settings, go to the Extensions tab, then:

For BChecks: go to the BChecks tab.

For BApps and custom extensions: go to the BApps & custom extensions tab.

Extensions that your system administrator has added to Burp Suite DAST are listed on these tabs.

Select the extensions you want to apply to the site.

Finish creating your new site, then click Save.

The selected extensions are applied to your site.

Note

Using extensions can increase the duration of your scans.

Removing extensions from sites

To remove an extension from a site:

From the Sites page, select the site you want to remove the extension from.

On the Details tab, click Edit .

In Scan settings, go to the Extensions tab, then:

For BChecks: go to the BChecks tab.

For BApps and custom extensions: go to the BApps & custom extensions tab.

Remove the extensions you no longer want applied to the site.

Click Save.

The selected extensions are removed from your site.

Applying extensions to folders

You can apply extensions at folder-level in Burp Suite DAST.

These are inherited by any subfolders and sites inside the folder, meaning these extensions are used whenever scans are run on sites within this folder.

Note

It's easy to identify inherited extensions by the information banner that appears at the top of the Details tab for sites,

and at the top of the Scan settings tab for folders.

Inherited extensions can be managed from the Scan settings > Extensions tab of the parent folder they are inherited from.

To apply an extension to a folder:

From the Sites page, select the folder you want to apply the extension to.

In Scan settings, go to the Extensions tab, then:

For BChecks: go to the BChecks tab.

For BApps and custom extensions: go to the BApps & custom extensions tab.

Extensions that your system administrator has added to Burp Suite DAST are listed on these tabs.

Select the extensions you want to apply to the folder.

Click Save.

The selected extensions are applied to your folder.

Note

Using extensions can increase the duration of your scans.

Removing extensions from folders

To remove an extension from a folder:

From the Sites page, select the folder you want to remove the extension from.

In Scan settings, go to the Extensions tab, then:

For BChecks: go to the BChecks tab.

For BApps and custom extensions: go to the BApps & custom extensions tab.

Remove the extensions you no longer want applied to the folder.

Click Save.

The selected extensions are removed from your folder.
