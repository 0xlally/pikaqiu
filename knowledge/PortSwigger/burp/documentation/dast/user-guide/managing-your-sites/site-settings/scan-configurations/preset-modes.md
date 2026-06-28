# Using preset scan modes

Source: https://portswigger.net/burp/documentation/dast/user-guide/managing-your-sites/site-settings/scan-configurations/preset-modes
Fetched: 2026-06-28T09:15:38.549779+00:00

DAST

Using preset scan modes

Last updated:

June 18, 2026

Read time:

1 Minute

Cloud

Self-hosted

Preset scan modes are predefined collections of scan settings. They offer a quick way to adjust how the scan balances speed and coverage.

Note

Preset scan modes are only available for web app sites.

To select a preset scan mode:

From the top menu, select Sites.

Select the site from the list.

Select the Details tab and click Edit.

From the Scan settings panel, click the Scan configuration tab.

Make sure that Use a preset scan mode is selected.

Click one of the available options.

Note

We recommend keeping a consistent scan configuration for each site you add. Changing the scan configuration can affect issue trends over time and cause Burp Suite DAST to give inaccurate time estimates while scanning.

If you want to scan a site you have already added with a new configuration, we recommend adding the site again with the new configuration selected.
