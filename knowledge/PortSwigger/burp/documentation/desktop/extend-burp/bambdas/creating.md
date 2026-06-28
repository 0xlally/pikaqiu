# Creating scripts

Source: https://portswigger.net/burp/documentation/desktop/extend-burp/bambdas/creating
Fetched: 2026-06-28T09:15:45.362403+00:00

Support Center

Documentation

Desktop editions

Extending Burp

Bambdas

Creating scripts

ProfessionalCommunity Edition

Creating scripts

Last updated:

June 18, 2026

Read time:

3 Minutes

Bambdas are lightweight, reusable Java-based scripts that enable you to fine-tune and extend Burp Suite's functionality. They can be used for tasks such as creating custom match-and-replace rules, table columns, and filters.

You can create scripts from the following locations:

Bambda library - Create any type of script, starting from a built-in template or a blank definition.

Specific Burp tools - Create scripts directly in certain tools.

Before you begin, we recommend exploring our Bambdas GitHub repository. There may be an existing script that meets your needs or provides inspiration for creating your own.

Warning

Slow running or resource-intensive scripts can slow down Burp. Write your script carefully to minimize performance impact.

Creating scripts in the Bambda library

In the Bambda library you can create new scripts using built-in templates or from a blank definition. After saving scripts to your library you can load and apply them across Burp.

To create a new script in your library:

Go to Extensions > Bambda library.

Click New and select either Blank or From template.

If you selected From template, select a template from the list, then click Create using this template.

Click the name field and enter a unique name.

Click the Function drop-down menu and select the task that the script will perform.

Click the Location drop-down menu and select the Burp tool where you want to use the script.

Write the script in Java.

[Optional] You can test scan check scripts against real HTTP messages. For more information, see Testing

custom scan checks.

Click Save. The script is saved to your library. Any errors are shown in the Compilation errors panel. You must resolve these before you can apply your script. For more information, see Troubleshooting scripts.

Click Save & close.

The script is saved to your library. If you created a script that defines a scan check function, Burp also adds it to your custom scan checks library, under

Extensions > Custom scan checks. The new scan check is immediately available from the scan launcher.

Note

Press Ctrl + S or Cmd + S to quickly save your scripts.

Related pages

To get feedback, showcase your work, and connect with other developers, share your script on our PortSwigger

Discord #bambdas channel.

To share your scripts with the community, add them to our ever-growing GitHub repository. For more information, see Submitting scripts to our GitHub repository.

Creating scripts from specific Burp tools

Many tools in Burp enable you to create and apply scripts directly. For more information, see the feature-specific instructions.

Filtering tables

For instructions on how to create scripts for filtering tables, see the following pages:

Filtering the HTTP history with scripts

Filtering the WebSockets history with scripts

Configuring the Logger view filter with scripts

Configuring the Logger capture filter with scripts

Filtering the site map with scripts

Adding custom columns

Professional For instructions on how to create scripts for adding custom columns to tables, see the following pages:

Adding custom columns in the HTTP history

Adding custom columns in the WebSockets history

Adding custom columns in Logger

Adding custom scan checks

Professional For instructions on how to create custom scan checks, see

Creating custom scan checks.

Adding custom actions

Professional Custom actions are tasks that you can apply to HTTP messages in Burp Repeater to extract, transform, and analyze data.

For instructions on how to create custom actions in Burp, see Custom actions.

For guidance on writing custom actions, see Writing custom actions.

Adding match and replace rules

Professional Match and replace rules automatically replace parts of HTTP messages as they pass through the proxy.

For instructions on how to create HTTP match and replace rules with scripts, see Creating HTTP match and replace rules with scripts.
