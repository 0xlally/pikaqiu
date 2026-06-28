# Defining the scan configuration for a folder

Source: https://portswigger.net/burp/documentation/dast/user-guide/managing-your-sites/site-settings/scan-configurations/folder-configs
Fetched: 2026-06-28T09:15:38.567943+00:00

DAST

Defining the scan configuration for a folder

Last updated:

June 18, 2026

Read time:

2 Minutes

Cloud

Self-hosted

You can set a scan configuration for a folder. The configuration is inherited by any subfolders or sites that are in the folder.

Note

You will need to use a custom scan configuration if you want to configure settings such as request throttling. Folders and subfolders that use custom scan configurations cannot use a preset scan mode.

To learn about these settings, see Custom scan configuration settings (Burp Suite DAST).

You can select either a preset scan mode or define a custom configuration:

Burp Scanner's preset scan modes are predefined collections of scan settings. They offer a quick way to adjust how the scan balances speed and coverage.

You can use a custom scan configuration to fine-tune Burp Scanner's behavior to meet your needs.

If you set a general scan configuration for a folder, you can make granular changes to the scan configuration for any subfolder and site within the folder.

Note

If you select scan configurations for folders, subfolders, and sites, it's important to understand exactly how these scan configurations are combined by Burp Scanner.

How scan configurations are combined

When a site inherits scan configurations from parent folders, Burp Scanner puts the different configurations in hierarchical order. You can see this list in the site Details tab, under Scan settings:

Burp Scanner combines the settings from these scan configurations. If settings in two or more scan configurations conflict, the setting from the lowest configuration in the list takes precedence.

To view the settings that have been changed in a configuration, click next to one of the selected scan configurations. You can see that the settings are grouped together by type. If the configuration changes any of the settings in the group from the default, the group is expanded:

Note

Only the changes you make override settings that are higher in the list. Any settings that you leave at their default value do not override settings that are higher in the list. This behavior is different to Burp Suite Professional.

How preset scan modes are combined

If you select a preset scan mode at more than one level, Burp Scanner only uses the scan mode at the lowest level in the list. The other preset scan modes are ignored.

If you set a mixture of preset scan modes and custom scan configurations, the settings are combined as described in How scan configurations are combined.

Related pages

Defining the scan configuration for a site.

Using preset scan modes.

Using custom scan configurations.

Burp Scanner built-in configurations - reference information on Burp Scanner's built-in scan configurations.
