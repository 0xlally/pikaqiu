# Configuring scans in Burp Suite Professional

Source: https://portswigger.net/burp/documentation/desktop/running-scans/configuring-scans
Fetched: 2026-06-28T09:15:53.064035+00:00

Support Center

Documentation

Desktop editions

Running scans

Configuring scans

Professional

Configuring scans in Burp Suite Professional

Last updated:

June 18, 2026

Read time:

3 Minutes

Scan configurations are collections of settings that define how a scan runs. You can configure them from the Scan configuration tab of the scan launcher for web application or API-only scans.

You can use scan configurations in two ways:

Set up a new configuration - Use a ready-made preset and start scanning immediately, or customize your own.

Load a configuration - Choose an existing configuration from the configuration library.

You can save the configuration to the configuration library and reuse it across your projects.

Setting up scan configurations

When setting up a new scan configuration, you have two options:

Use a preset - Pick a ready-made configuration and start scanning immediately.

Customize a configuration - Start from Burp's default settings (or a preset) and adjust the settings to suit your needs.

To create a new scan configuration:

In the scan launcher, go to the Scan configuration tab.

From the dropdown, select the type of configuration you want to use:

Presets - Choose from the following built-in scan modes that balance speed and coverage:

Lightweight - Gain fast feedback. Will complete within 15 minutes.

Fast - Gain greater coverage. Generally completes within an hour.

Balanced - Balances coverage and speed. Completes within a few hours.

Deep - Comprehensive coverage. Scanning time varies depending on the target's complexity.

Custom - Start from Burp's default scan settings and adjust them as required.

Burp automatically adjusts the scan settings based on your selection. You can run the scan as is, or review and edit the settings as required.

Saving scan configurations

You can save custom scan configurations to the configuration library for reuse across projects.

Saving complete scan configurations

You can save all of your configured settings as a single configuration. This can include configurations for a crawl, an audit, a live passive task, or a crawl and audit.

To save a complete scan configuration:

Click Save. The Save to configuration library dialog opens.

Enter a unique Configuration name.

Click Save.

Your configuration is added to your library. You can load it when setting up future scans, or export it from the library for use in other Burp installations.

Saving crawl-only or audit-only configurations

If you've configured a crawl and audit, you can save a crawl-only or audit-only scan configuration:

Click Audit configuration or Crawl configuration in the settings drop-down.

Click Save. The Save to configuration library dialog opens.

Enter a unique Configuration name.

Click Save.

Your configuration is added to your library. You can load it when setting up future scans, or export it from the library for use in other Burp installations.

Loading scan configurations

To load an existing scan configuration from the configuration library:

Go to the Scan configuration tab of the scan launcher.

Click Load. The configuration library opens.

Select a built-in configuration or a saved custom configuration.

Burp automatically adjusts the scan settings based on your selection. You can run the scan as is, or review and edit the settings as required.

Note

If the configuration includes custom scan checks that aren't in your library, they are marked by an asterisk *. To add them to your library, right-click and select Save to library.

Importing scan configurations

To use a scan configuration that you've exported from another installation of Burp, first import it into the configuration library, then load it in the scan launcher.

How Burp applies scan configurations

When you load a scan configuration, Burp applies all the settings that are marked as edited in that configuration, leaving everything else unchanged.

Since version 2025.3, all settings are treated as edited, so loading them overwrites your current settings:

Preset configurations - Overwrite all settings.

Custom crawl & audit configurations - Overwrite all settings.

Custom crawl configurations - Overwrite all crawl settings.

Custom audit configurations - Overwrite all audit settings.

Some built-in configurations and legacy custom configurations may only change specific settings. To see which settings are marked as edited in a configuration:

Go to Settings > Configuration library.

Select the configuration.

Click Edit.

Any section that appears expanded is marked as edited.

Related pages

Loading scan configurations

Exporting custom configurations

Crawl settings

Audit settings
