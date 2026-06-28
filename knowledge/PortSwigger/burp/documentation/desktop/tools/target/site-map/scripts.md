# Filtering the site map with scripts

Source: https://portswigger.net/burp/documentation/desktop/tools/target/site-map/scripts
Fetched: 2026-06-28T09:16:09.507673+00:00

Support Center

Documentation

Desktop editions

Tools

Target

Site map

Filtering the site map with scripts

ProfessionalCommunity Edition

Filtering the site map with scripts

Last updated:

June 18, 2026

Read time:

4 Minutes

You can apply scripts to create powerful custom filters for your site map. You can do this in two ways:

Load existing scripts - Load scripts from your Bambda library. This is your personal collection of reusable scripts. It includes any scripts you've created and saved, or ones you've imported, for example, from our GitHub repo. For more information, see Importing scripts.

Create new scripts - Write your own custom scripts. To get started quickly, use one of the built-in templates. These work out of the box and are easy to customize.

Keyboard shortcuts

To speed up your workflow when creating or loading scripts, you can use the following keyboard shortcuts:

Save - Ctrl + S or Cmd + S

Save as - Ctrl + Shift + S or Cmd + Shift + S

Create new script - Ctrl + N or Cmd + N

Load recent script - Ctrl + O or Cmd + O

Loading scripts from your library

You can load and apply scripts that are stored in your Bambda library to filter your site map.

To load a script from your Bambda library:

In Target > Site map, click the filter bar to open the Site map filter window.

In the Site map filter window, click Script mode.

Click Load.

Select a recent script from the list.

If the script you want to load isn't in the list, click View all to view all scripts stored

in your library.

Select a script.

Click Load.

[Optional] If required, edit the script:

Make your changes.

Click Apply to compile and test the script. Fix any errors shown in the Compilation errors panel. For more information, see Troubleshooting scripts.

Save your changes:

To overwrite the existing script, click Save to library > Save.

To save a new version, click Save to library > Save as.

Click Apply & close.

Burp compiles your script and applies it to every item already logged in your site map, and to any future site map items generated in this project.

Creating custom scripts

You can write your own scripts directly in the Site map filter window, using built-in templates or from a blank definition.

Note

Before you begin writing, we recommend exploring our Bambdas GitHub repository. There may be an existing script that meets your needs or provides inspiration for creating your own.

Converting filter settings to scripts

You can convert filter settings to a script as a starting point for further customization:

In Target > Site map, click the filter bar to open the Site map filter window.

Make changes to the filter settings as necessary.

At the bottom of the Site map filter window, click Convert to script.

Your filter is converted into a script, enabling you to customize it further using Java.

Note

Some filter settings can't be converted to scripts as they aren't currently supported. For example, these site map filter settings don't convert to Script mode:

Show only requested items

Hide not-found items

Creating your script

Two objects of the Montoya API are available to help you write your script:

SiteMapNode

Utilities

To create a script to filter your site map:

In Target > Site map, click the filter bar to open the Site map filter window.

In the Site map filter window, click Script mode.

If you want to create your script from a built-in template, select New > From template. Select a template from the list, then click

Create using this template.

Write your script using Java.

Click Apply to compile and test the script. Fix any errors shown in the Compilation errors panel. For more information, see Troubleshooting scripts.

[Optional] Click Save to library > Save. The script is saved to your Bambda library for future use across Burp.

Click Apply & close.

Burp compiles your script and applies it to every item already logged in your site map, and to any future site map items generated in this project.

Warning

Using slow running or resource-intensive scripts can slow down Burp. Write your script carefully to minimize performance impact.

Example script

In the example below, we'll create a script that filters the site map to show only items that meet the following criteria:

The item must have a POST method.

The item must have an issue reported against it.

In this example, our script is:

return node.requestResponse().request().method().equals("POST") && !node.issues().isEmpty();

Related pages

To get feedback, showcase your work, and connect with other developers, share your script on our PortSwigger

Discord #bambdas channel.

To share your scripts with the community, add them to our ever-growing GitHub repository. For more information, see Submitting scripts to our GitHub repository.
