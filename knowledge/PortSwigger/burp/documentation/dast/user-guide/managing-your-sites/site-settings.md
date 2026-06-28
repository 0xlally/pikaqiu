# Configuring site settings

Source: https://portswigger.net/burp/documentation/dast/user-guide/managing-your-sites/site-settings
Fetched: 2026-06-28T09:15:38.287921+00:00

DAST

Configuring site settings

Last updated:

June 18, 2026

Read time:

2 Minutes

Cloud

Self-hosted

Burp Suite DAST offers a number of site-related settings that enable you to fine-tune Burp Scanner's behavior and provide additional information such as login credentials.

Note

You can also configure some site settings at the folder level. These settings are inherited by any subfolders and sites in the folder. You can then fine-tune the settings for individual subfolders and sites. For more information, see Defining the scan configuration for a folder.

For individual sites, you can access the site settings from the Scan settings panel, either when you create a site or when you edit an existing site.

Note

You can use custom scan configurations to configure scan settings that are not available when using a preset scan mode, such as request throttling.

For more information, see Custom scan configuration settings (Burp Suite DAST).

The following tabs are available:

Scan configuration enables you to specify one or more configurations to use when scanning the site. See Defining the scan configuration for a site.

Burp AI and automation enables you to configure AI-enhanced scanning and use Burp AI to record login sequences. See Configuring AI-enhanced scanning.

Authentication enables you to provide login credentials and configure platform authentication for web apps. See

Configuring authentication for web apps.

Connections enables you to configure upstream proxy servers. See Configuring upstream proxy servers.

Headers & cookies enables you to add custom headers and cookies to requests made when scanning the site. See

Adding headers and cookies.

Self-hosted Extensions enables you to select any extensions that Burp Suite DAST should use when scanning the site. See Scanning with extensions.

Self-hosted Scanning pool enables you to select a scanning pool for the site to belong to. See Managing scanning pools.

Notifications enables you to configure automated notifications on scan progress. See Setting up scan notifications.

You must select a scan configuration in order to be able to save a web app site. However, you can save an API site without selecting a scan configuration. All other settings in the Scan settings section are optional.

Related pages

Defining the scan configuration for a site.

Defining the scan configuration for a folder.

Custom scan configuration settings (Burp Suite DAST).
