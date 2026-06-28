# Setting up email notifications

Source: https://portswigger.net/burp/documentation/dast/user-guide/managing-your-sites/scan-notifications/email-notifications
Fetched: 2026-06-28T09:15:38.278997+00:00

DAST

Setting up email notifications

Last updated:

June 18, 2026

Read time:

2 Minutes

Cloud

Self-hosted

Setting up email notifications can help you to keep up to date with your organization's security posture. When you configure email notifications for a site, Burp Suite DAST sends a scan summary report to your nominated users as soon as a scan of that site finishes.

Note

Self-hosted

Your SMTP server must be connected to Burp Suite DAST in order for you to set up email notifications. For more information on how to set up your SMTP server, see Configuring your SMTP server

.

Setting up email notifications when creating a new site

To set up email notifications during the process of creating a new site:

Select Sites > Add a new site to display the Create a new site page.

In the Scan settings section, select the Notifications tab.

In the Send scan summary reports by email section, enter an Email address.

To specify an additional email, click the plus button and enter the required email address.

Setting up email notifications for existing sites

To set up email notifications for an existing site:

Select Sites to display the site tree.

Select the site you want to set up email notifications for.

Select the Details tab.

Click Edit.

In the Scan settings section, select the Notifications tab.

In the Send scan summary reports by email section, enter an Email address.

To specify an additional email, click the plus button and enter the required email address.

Click Save.

Related pages

Self-hosted

Configuring your SMTP server - explains how to set up an SMTP server

Adding new sites - explains the process of setting up a new site in detail.
