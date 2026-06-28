# Scanning web apps

Source: https://portswigger.net/burp/documentation/dast/user-guide/scanning-web-apps
Fetched: 2026-06-28T09:15:40.917048+00:00

DAST

Scanning web apps

Last updated:

June 18, 2026

Read time:

3 Minutes

Cloud

Self-hosted

You need to create a site in order to scan a web app. You can add an unlimited number of sites. In this context, the term web app refers to an application that runs on a web server and is accessed via a web browser.

Before you add your first web app site, you need to configure your network and firewall settings. For more information, see Configuring network and firewall settings for a site.

To add a new web app site:

Select Sites > Add a new site to go to the Create a new site page.

Under Site type, select Web app.

Enter a unique Site name.

To add the web app site to an existing folder, select from the Site folder drop-down menu. If you leave this field blank then the web app site is created at the top level of the site tree.

Enter the Start URLs that you want all the scans of this web app site to start from. No wildcards are permitted.

If necessary, configure the site scope to refine which URLs to scan. For more information, see setting the site scope.

If necessary, specify your own protocols instead of HTTP & HTTPS. For more information, see Protocol Settings.

Scroll down to Scan settings > Scan configuration and select a scan configuration for the web app site. You can either use a preset scan mode or a custom configuration. For more information, see For more information, see Defining the scan configuration for a site.

Click Save.

Burp Suite DAST adds the new web app site to the site tree and prompts you to perform a pre-scan check.

Note

When you scan a web app, Burp Scanner also scans any APIs that it finds within the site scope. If you want to scan specific APIs, see Scanning APIs.

If you want to run some test scans before you add your own web apps, you can use vulnerable-website.com. This is a demo web app with a few intentional vulnerabilities.

Optional settings for your new web app site

When you add a new web app site, you can configure a number of settings.

Detailed scope configuration

The site scope defines the locations that Burp Scanner can visit. By default, Burp Suite DAST automatically uses your Start URLs to derive the site scope.

You can refine the scope using URL prefixes (Basic) or regex patterns (Advanced). This enables you to target Burp Scanner on the locations you're interested in, and exclude any locations you want to avoid. For more information, see setting the site scope.

Protocol settings

If you don't specify a protocol, Burp Scanner uses both HTTP and HTTPS. To specify your own protocols:

Under Site scope > Protocol settings, select Scan using my specified protocols.

Enter https:// or http:// at the beginning of the Start URL.

Enter https:// or http:// at the beginning of any URLs you added in the In-scope URL prefixes or Out-of-scope URL prefixes tabs.

Scan settings

You can specify a range of optional settings for your scan. For example, you can set:

Scan configurations

Application logins

AI-enhanced scanning

Extensions

To specify these, go to Scan settings for your site or folder. For more information, see

Configuring site settings.

Note

We recommend keeping a consistent scan configuration for each site you add. Changing the scan configuration can affect issue trends over time and cause Burp Suite DAST to give inaccurate time estimates while scanning.

If you want to scan a web app that you have already added with a new configuration, we recommend adding the app again with the new configuration selected.

Related pages

Configuring AI-enhanced scanning - explains how to configure Burp AI to automatically investigate issues.

Configuring authentication for web apps - explains how to add authentication for sites that scan web apps.

Managing scheduled scans - explains how to schedule scans for your new site.

Defining scan configuration for a site - explains how to create and work with scan configurations.

Configuring site settings - explains the optional scan settings you can configure for a site.

Configuring your environment network and firewall settings.

Importing sites in bulk - explains how to add multiple sites at once.

Burp Scanner built-in configurations - reference information on Burp Scanner's built-in scan configurations.

Adding recorded login sequences.

Performing a pre-scan check.
