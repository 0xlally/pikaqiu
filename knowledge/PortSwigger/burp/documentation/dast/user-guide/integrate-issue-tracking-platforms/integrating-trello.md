# Integrating Burp Suite DAST with Trello

Source: https://portswigger.net/burp/documentation/dast/user-guide/integrate-issue-tracking-platforms/integrating-trello
Fetched: 2026-06-28T09:15:37.757978+00:00

DAST

Integrating Burp Suite DAST with Trello

Last updated:

June 18, 2026

Read time:

3 Minutes

If you or your teams use Trello, you may like to integrate this with Burp Suite DAST. Once configured, this enables you to create Trello cards from within Burp Suite DAST for any security issues found by your scans.

Prerequisite

You must have access to Burp Suite DAST as an administrator.

(Recommended) Create a new Trello user for the integration

To integrate with Trello, Burp Suite DAST must be linked to a specific Trello user.

We recommend creating a new Trello user specifically for the integration. This allows you to control which boards are available for use in Burp Suite DAST - simply by giving your user access to those boards.

Connect Burp Suite DAST to Trello

To connect Burp Suite DAST to Trello:

Log in to Trello as the user you want to use for the integration.

Log in to Burp Suite DAST as an administrator.

From the settings menu, select Integrations.

On the Trello tile, select Configure.

Click Get my API key.

Review and accept Trello's Terms and Conditions, if relevant.

Copy your Trello API key to your clipboard.

In Burp Suite DAST, paste your Trello API key into the field provided.

Click Continue.

Under Authorization URL, copy the URL shown and paste it into your browser.

To allow BurpSuiteEnterpriseEdition access to your Trello account, click Allow.

Copy the token to your clipboard.

In Burp Suite DAST, paste your token into the field provided.

Click Connect.

If Burp Suite DAST successfully connects to Trello, you'll be presented with options to configure both manual and automatic card creation.

Note

You must enable at least one of these in order to complete the Trello configuration.

Enable manual Trello card creation

To enable users to create Trello cards manually from within Burp Suite DAST, you need to configure the list of Trello boards and lists that they can choose from:

Select a board from the Board drop-down list.

Select a list type from the List drop-down list.

Click the + symbol.

If necessary, repeat these steps to add more boards and lists.

Note

You need to add separate entries for each list, even when adding multiple lists from the same board.

Click Save.

Enable automatic Trello card creation

You can configure Burp Suite DAST to create Trello cards automatically. Cards are created for any issues that meet the minimum severity and confidence levels that you specify.

Note

To avoid inadvertently flooding your Trello backlog with an overwhelming number of cards, we recommend setting high severity and confidence levels initially. You can then lower these once you have a better understanding of how many cards are created as a result of your scans.

Click Enable.

Select a board from the Board drop-down list.

Select a list from the List drop-down list.

Use the sliders to set the minimum issue severity and confidence levels that trigger Trello card

creation.

Click Save.

Raising Trello cards from within Burp Suite DAST

For information on how users can manually raise Trello cards, refer to Raise Trello cards from within Burp Suite DAST.
