# Using custom scan configurations

Source: https://portswigger.net/burp/documentation/dast/user-guide/managing-your-sites/site-settings/scan-configurations/custom-configs
Fetched: 2026-06-28T09:15:38.330602+00:00

DAST

Using custom scan configurations

Last updated:

June 18, 2026

Read time:

2 Minutes

Cloud

Self-hosted

In addition to the Burp Suite DAST preset scan modes, you can create and import custom configurations. This section explains how to create and assign custom configurations to a site.

Note

We recommend keeping a consistent scan configuration for each site you add. Changing the scan configuration can affect issue trends over time and cause Burp Suite DAST to give inaccurate time estimates while scanning.

If you want to scan a site you have already added with a new configuration, we recommend adding the site again with the new configuration selected.

Assign a custom scan configuration to a site

To select a custom scan configuration for a pre-existing site:

From the top menu, select Sites.

Select the site from the list.

Select the Details tab and click Edit.

Under Scan settings, select the Scan configuration tab.

To display a list of scan configurations that are currently assigned to the site, select Use a custom configuration.

To add a scan configuration to your site, you have two choices:

Select a configuration from the drop-down box to add it to the list.

To create a new custom scan configuration, click Create custom configuration.

Related pages

Scan configurations.

Burp Scanner built-in configurations - reference information on Burp Scanner's built-in scan configurations.

Custom scan configuration settings (Burp Suite DAST).

Create a custom scan configuration

To create a custom scan configuration:

From the settings menu , select Scan configurations.

On the Scan configuration page, click New configuration.

Add a name for the configuration:

Click the New Scan Configuration title bar.

Enter a name.

Click OK.

Expand each scan configuration menu and change the settings as required.

When you're happy with your changes, click Save.

You can now select your new scan configuration from the configuration library when you create a new site.

Related pages

Scan configurations.

Custom scan configuration settings (Burp Suite DAST)

Exporting scan configurations

You can export your scan configurations from Burp Suite DAST or Burp Suite Professional. This enables you to:

Share your scan configurations with other users in your organization.

Share scan configurations between Burp Suite DAST and Burp Suite Professional.

Use your scan configuration in a CI-driven scan.

To export a scan configuration from Burp Suite DAST:

From the settings menu , select Scan configurations.

To download your chosen scan configuration, click the download icon in the right-hand column.

Related pages

For more information on exporting configuration files from the desktop editions for Burp, see the Configuration library page.

Importing scan configurations

You can import scan configurations from other installations of Burp Suite DAST, or Burp Suite Professional.

To import a scan configuration:

Export the scan configurations from Burp Suite DAST, or Burp Suite Professional.

From the settings menu , select Scan configurations.

Click Import to display the open file dialog.

Select the configuration file that you want to import.
