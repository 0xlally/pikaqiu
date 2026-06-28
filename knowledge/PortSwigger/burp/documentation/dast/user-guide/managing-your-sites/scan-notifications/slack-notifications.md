# Setting up Slack notifications

Source: https://portswigger.net/burp/documentation/dast/user-guide/managing-your-sites/scan-notifications/slack-notifications
Fetched: 2026-06-28T09:15:38.274844+00:00

DAST

Setting up Slack notifications

Last updated:

June 18, 2026

Read time:

2 Minutes

Cloud

Self-hosted

Setting up Slack notifications can help you to keep up to date with your organization's security posture. When you configure Slack notifications for a site, Burp Suite DAST sends a notification to your nominated channels as soon as a scan of that site starts, fails, or finishes.

Note

You must integrate Burp Suite DAST with Slack in order to receive Slack notifications. For more information on how to integrate Slack, see Integrating Burp Suite DAST with Slack.

Setting up Slack notifications when creating a new site

To set up Slack notifications when creating a new site:

On the top menu, select Sites > Add a new site to display the Create a new site page.

In the Scan settings section, select the Notifications tab.

In the Send scan notification to Slack section, enter a Slack channel.

To specify an additional channel, click the plus button and enter the required channel name.

Setting up Slack notifications for existing sites

To set up Slack notifications for an existing site:

On the top menu, select Sites to display the site tree.

Select the site you want to set up notifications for.

Select the Details tab and click Edit.

In the Scan settings section, select the Notifications tab.

In the Send scan notifications to Slack section, enter a Slack channel.

To specify an additional channel, click the plus button and enter the required channel name.

Click Save.

Related pages

Integrating Burp Suite DAST with Slack.

Adding new sites - explains the process of setting up a new site in detail.
