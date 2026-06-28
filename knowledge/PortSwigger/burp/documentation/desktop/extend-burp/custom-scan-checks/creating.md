# Creating custom scan checks

Source: https://portswigger.net/burp/documentation/desktop/extend-burp/custom-scan-checks/creating
Fetched: 2026-06-28T09:15:46.360885+00:00

Support Center

Documentation

Desktop editions

Extending Burp

Custom scan checks

Creating custom scan checks

Professional

Creating custom scan checks

Last updated:

June 18, 2026

Read time:

3 Minutes

Custom scan checks enable you to extend Burp Scanner with your own vulnerability detection logic. You can create two types of custom scan checks:

Scripts - Written in Java with access to our Montoya API. Best if you want to build more complex checks.

BChecks - Written in our custom BCheck language. Best for quick, lightweight checks.

To help you get started, we provide the following:

Built-in starter templates in the editor.

Inline suggestions and error highlighting in the editor.

A range of community and reference resources.

Related pages

Custom scan checks writing guide

Passive

scan check worked example

Active

scan check worked example

Bambda scripts GitHub repository - Examples of custom scan checks written in Java, created by the community and our researchers.

BChecks repository - Examples of custom scan checks written in our BCheck language, created by the community and our researchers.

Warning

Slow running or resource-intensive scripts can slow down Burp. Write your script carefully to minimize performance impact.

Creating script-based checks

To create a new custom scan check using Java:

Go to Extensions > Custom scan checks.

Click New and select Blank script or

From template.

If you selected From template:

Select the Script mode tab.

Select a template from the list.

Click Create using this template.

Select the script Type. You can choose from Active or Passive.

Select when the Script runs. You can choose from Per insertion point, Per

request, or Per host.

[Optional] For scan checks that require out-of-band testing, enable the Use Collaborator toggle to generate payloads and customize how Burp handles interaction callbacks. For more information, see Using Collaborator in checks.

Write the script in Java. For more information, see Custom scan checks writing guide.

Click Validate. Any errors are shown in the Errors panel. You must resolve these before you can use your scan check. For more information, see Troubleshooting scripts.

[Optional] Test the script against real HTTP messages. For instructions, see Testing custom scan checks.

Click Save & close.

The check is saved to your custom scan checks library for use in scans and across projects.

Creating BCheck-based checks

To create a custom scan check using our custom BChecks language:

Go to Extensions > Custom scan checks.

Click New and select either Blank BCheck or

From template.

If you selected From template:

Select the BCheck mode tab.

Select a template from the list.

Click Create using this template.

Write the script in our BCheck language. For reference documentation, see BCheck definitions.

Click Validate. Any errors are shown in the Errors panel. You must resolve these before you can use your scan check.

[Optional] To standardize the indentation and whitespace, right-click the editor and select Format BCheck.

[Optional] Test the BCheck against real HTTP messages. For more information, see Testing custom scan checks.

Click Save & close.

The check is saved to your custom scan checks library for use in scans and across projects.

Related pages

For instructions on how to use custom scan checks in your scans, see Adding custom scan checks to scans.

To get feedback, showcase your work, and connect with other developers, share your custom scan check on our

PortSwigger Discord #bambdas or #bchecks channel.

To learn how to export your custom scan checks so that you can share them with others, see Exporting custom scan checks.

To share your custom scan checks with the community, add them to our ever-growing GitHub repositories:

For information on submitting script-based custom scan checks to our Bambda scripts GitHub repository, see Submitting scripts to our GitHub repository.

For information on submitting BCheck-based custom scan checks to our BChecks GitHub repository, see Submitting BChecks to the community.
