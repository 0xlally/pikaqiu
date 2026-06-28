# Bambdas

Source: https://portswigger.net/burp/documentation/desktop/extend-burp/bambdas
Fetched: 2026-06-28T09:15:45.469802+00:00

Support Center

Documentation

Desktop editions

Extending Burp

Bambdas

ProfessionalCommunity Edition

Bambdas

Last updated:

June 18, 2026

Read time:

2 Minutes

Bambdas are scripts that you can run directly from Burp Suite's interface. They enable you to quickly personalize various tasks, such as creating custom match-and-replace rules, table columns, and filters.

You can create your own scripts and save them to your Bambda library for easy reuse. You can also import existing scripts shared by others or downloaded from our Bambdas GitHub repository. Once a script is in your Bambda library, you can easily reuse it across Burp and in different projects.

Warning

Bambda scripts can run arbitrary code. For security reasons, please be cautious when using scripts from unverified sources.

In this section

Managing scripts in your Bambda library

Importing scripts into your Bambda library

Creating scripts

Feature specific instructions

Many tools in Burp enable you to apply scripts directly. For more information, see the feature-specific instructions.

Filtering tables

For instructions on how to use scripts for filtering tables, see the following pages:

Filtering the HTTP history with scripts

Filtering the WebSockets history with scripts

Configuring the Logger view filter with scripts

Configuring the Logger capture filter with scripts

Filtering the site map with scripts

Adding custom columns

Professional For instructions on how to use scripts for adding custom columns to tables, see the following pages:

Adding custom columns in the HTTP history

Adding custom columns in the WebSockets history

Adding custom columns in Logger

Adding custom scan checks

Professional For instructions on how to use scripts for creating and adding custom scan checks, see the following pages:

Custom scan checks

Adding custom scan checks to scans

Adding custom actions

Professional Custom actions are tasks that you can apply to HTTP messages in Burp Repeater to extract, transform, and analyze data.

For instructions on how to create custom actions, see Custom actions.

For guidance on writing custom actions, see Writing custom actions.

Adding match and replace rules

Professional Match and replace rules automatically replace parts of HTTP messages as they pass through the proxy.

For instructions on how to create HTTP match and replace rules with scripts, see Creating HTTP match and replace rules with scripts.

Related pages

To learn what a Bambda is and see a couple of filter script examples, watch the Burp Suite Shorts | Bambdas video on YouTube.

To learn more about how to use the different script types, see the following videos on YouTube:

Burp Suite #Shorts | Bambda table filters

Burp Suite #Shorts | Bambda table customization

Burp Suite: Introducing Custom actions

Join our PortSwigger Discord to chat with the

community in our #bambdas channel - get tips, share ideas, and stay up-to-date with the

latest Bambdas developments.
