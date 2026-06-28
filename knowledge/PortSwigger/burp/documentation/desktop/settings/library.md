# Configuration library

Source: https://portswigger.net/burp/documentation/desktop/settings/library
Fetched: 2026-06-28T09:15:54.455521+00:00

Support Center

Documentation

Desktop editions

Settings

Configuration library

ProfessionalCommunity Edition

Configuration library

Last updated:

June 18, 2026

Read time:

3 Minutes

The configuration library contains groups of settings that are configured for particular tasks, such as a crawl or an audit. Burp includes a range of built-in setting configurations for common tasks. You can also add your own custom configurations.

To access the configuration library, go to the Settings dialog.

Related pages

For a detailed list of Burp's built-in configurations, see Burp Scanner built-in configurations.

Adding a custom configuration

Each configuration defines the settings for a particular function, such as crawling or scope. To add a new custom configuration:

Click Add and select the function for the configuration. The New configuration dialog opens.

Enter a unique name for the configuration.

Edit the settings for the configuration. The dialog shows settings relevant to the chosen function.

Click OK.

Note

You do not need to configure all settings in the New configuration dialog. If your configuration does not define a particular area, then default or existing values are used.

Importing custom configurations

You can import configurations from another Burp installation into your configuration library. This enables you to reuse them across Burp.

To import configurations:

Go to Settings > Configuration library.

Click Import.

Select the configuration files you want to import. They must be in JSON format.

Click Open.

Your configuration is now available in the library. You can apply it from relevant Burp tools.

Warning

You can import project and configuration files from other users. However, for security reasons, we recommend only importing project and configuration files from trusted sources.

Exporting custom configurations

You can export configurations from your configuration library. This enables you to save backups and share them with other Burp installations.

To export configurations:

Go to Settings > Configuration library.

Select the configurations you want to export.

Click Export.

Choose a folder.

Click Save.

The configuration files are saved in JSON format.

Managing custom configurations

To manage the library, you can:

Filter by Built-in and Custom configurations.

Edit and Duplicate any configuration.

Delete custom configurations.

Many Burp tasks let you select multiple configurations. Configurations are applied in order, so if you load multiple configurations that affect the same settings, the lower configuration in the list takes precedence over configurations above it.

Configuration files

Configuration files store setting configurations. These use the JSON format.

To load and create configuration files you can:

Export or import a file from the configuration library.

Load or save separate configuration files for all user or project settings. For more information, see

Managing settings.

Load project settings from a configuration file when you launch Burp. For more information, see Creating project files.

Load configuration files when you launch Burp from the command line. For more information, see Launching

Burp Suite from the command line.

Burp extensions can load or save configuration files via the API.

The easiest way to generate a file is to create the desired configuration in Burp, then export a file from it. You can edit any file that you create in Burp, as the contents are human-readable. The structure and naming corresponds to the presentation of the settings in Burp.
