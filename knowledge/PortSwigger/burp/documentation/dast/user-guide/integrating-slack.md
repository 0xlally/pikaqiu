# Integrating Burp Suite DAST with Slack

Source: https://portswigger.net/burp/documentation/dast/user-guide/integrating-slack
Fetched: 2026-06-28T09:15:36.849890+00:00

DAST

Integrating Burp Suite DAST with Slack

Last updated:

June 18, 2026

Read time:

3 Minutes

Cloud

Self-hosted

If you or your teams use Slack, you may like to set up an integration with Burp Suite DAST. Once configured, this enables you to receive automatic notifications to specific Slack channels when Burp Suite DAST scans start, finish, or fail.

Prerequisites

You are the Workspace Owner within your Slack workspace.

You have created one or more channels in Slack that you want to connect with Burp Suite DAST.

Create a Slack app

First, you need to create a Slack app which Burp Suite DAST will use to send messages to Slack.

In your browser, sign in to your Slack workspace as the Workspace Owner.

If you've not already done so, you'll need to create a channel for your app to communicate with. From the left-hand menu of the main Slack communication platform, under Channels, click on Add channels, then Create a new channel.

Add some information to help you identify your channel, set your desired level of privacy, and click the Create button. Follow the prompts to add relevant members to the channel.

Open a new browser tab and visit the Your Apps page in Slack. In the upper-right hand corner, click the Create New App button.

Select the From scratch option.

Give your app a name (e.g. Burp Suite DAST), and select the Slack workspace you want to use the app in. Click the Create App button. This will take you to your app's information page.

From the left-hand navigation menu, under Features, select OAuth & Permissions. Scroll down to the Scopes section.

Under Bot Token Scopes, click Add an OAuth Scope and add the following scopes:

channels:read

groups:read

im:read

mpim:read

chat:write

users:read

From the left-hand navigation menu, under Settings, select Basic Information.

(Optional) Under Display Information, you can upload an icon to help you identify the app more easily. For example, you can use the Burp Suite DAST logo.

Under Install your app, click on the Install to Workspace button. When prompted, click Allow.

Add the app to your Slack channels

Once you've created a Slack app for Burp Suite DAST, you need to add the app to each channel that you want to receive scan notifications. The channels you add the app to at this stage will subsequently become available for use in Burp Suite DAST.

Go to the Slack workspace in which you created the app.

From the left-hand navigation menu, under Channels, click the name of a channel that you want to make available in Burp Suite DAST.

At the top of the screen, click the name of the channel to open the channel details dialog.

Go to the Integrations tab. From the Apps section, select the option to Add an App.

In the list, find the app you just created, and click the Add button.

Repeat this process for any other channels that you want to make available in Burp Suite DAST.

Connect your Slack app to Burp Suite DAST

Next, we need to configure the connection between the Slack app we just created, and Burp Suite DAST. For this, we will use an OAuth token.

Note

Burp Suite DAST does not currently support rotating OAuth tokens. If you wish to add new functionality or permissions to your Slack app, you will need to generate a new OAuth token and share this with Burp Suite DAST.

Go to the Your Apps page in Slack, and select the Slack app you just created.

From the left-hand navigation menu under Features, click OAuth & Permissions.

Under OAuth Tokens for Your Workspace , locate the Bot User OAuth Token, and copy it to your clipboard.

Log in to Burp Suite DAST as an administrator.

From the settings menu, select Integrations.

On the Slack tile, click the Configure button.

Paste your Slack OAuth token into the provided field, and click Connect. A list of all of the Slack channels to which you added the Slack app should now be imported.

Manage which Slack channels are available

Once you have added your Slack OAuth token to Burp Suite DAST, any Slack channels with the app installed will be visible in the Slack integration section under Slack channels.

By default, communication to these channels is disabled. Any channels you enable here will be available for selection when creating or editing a site.

Once you've completed the Slack integration, you can assign Slack channels to your sites.
