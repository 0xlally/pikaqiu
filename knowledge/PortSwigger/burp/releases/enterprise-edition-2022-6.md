# Enterprise Edition 2022.6

Source: https://portswigger.net/burp/releases/enterprise-edition-2022-6
Fetched: 2026-06-28T09:16:17.730553+00:00

This release provides preset scan modes, which make it much simpler to start scans for a range of use cases. We've also made it easier to monitor how your scans are progressing.

Simplified scanning with preset scan modes

It's now much easier to start scanning with our new preset scan modes. These four ready-to-use modes let you adjust the balance of speed and coverage with a single click, so you can quickly launch a scan that suits your needs. When creating or editing a site, you can choose from Lightweight, Fast, Balanced, or Deep modes.

You can still create custom scan configurations to fine-tune Burp Scanner's behavior - just select the Use a custom configuration radio button to access all of the options you're used to from previous versions.

Improved scan duration estimates

We've improved how we estimate scan durations, so you can easily monitor how your scans are progressing:

An indication of the time remaining is now shown for all scans, including new scans.

We've improved the accuracy of duration estimates for recurring scans, by considering historical scan durations.

You can now see if the scan is in the 'crawling' or 'auditing' phase.

Other improvements

This release also provides the following improvement:

When you use the 'Scan again' function, you have the option to enable verbose logging. This can be helpful for troubleshooting.

Bug fixes

We've fixed some bugs. For example:

If you use the GraphQL API to get issues one at a time, you no longer get duplicates.

We fixed an error when running a recovery or upgrade installation.

If you set a filter in the Issues tab and then click on an issue in the sidebar, the filter is no longer reset.
