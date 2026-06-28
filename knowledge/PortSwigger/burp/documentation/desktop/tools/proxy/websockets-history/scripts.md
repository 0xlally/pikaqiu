# Filtering the WebSockets history with scripts

Source: https://portswigger.net/burp/documentation/desktop/tools/proxy/websockets-history/scripts
Fetched: 2026-06-28T09:16:07.302878+00:00

Support Center

Documentation

Desktop editions

Tools

Burp Proxy

WebSockets history

Filtering with scripts

ProfessionalCommunity Edition

Filtering the WebSockets history with scripts

Last updated:

June 18, 2026

Read time:

4 Minutes

You can apply Java-based scripts to create powerful custom filters for your WebSockets history. You can do this in two ways:

Load existing scripts - Load scripts from your Bambda library. This is your personal collection of reusable scripts. It includes any scripts you've created and saved, or ones you've imported, for example, from our GitHub repo. For more information, see Importing scripts.

Create new scripts - Write your own custom scripts. To get started quickly, use one of the built-in templates. These work out of the box and are easy to customize.

Note

To quickly toggle the filter on or off, click Filter on or Filter off. This enables you to compare filtered and unfiltered traffic without resetting your filter.

Keyboard shortcuts

To speed up your workflow when creating or loading scripts, you can use the following keyboard shortcuts:

Save - Ctrl + S or Cmd + S

Save as - Ctrl + Shift + S or Cmd + Shift + S

Create new script - Ctrl + N or Cmd + N

Load recent script - Ctrl + O or Cmd + O

Loading scripts from your library

You can load and apply scripts that are stored in your library to filter the WebSockets history.

To load a script from your Bambda library:

In Proxy > WebSockets history, click the filter bar to open the WebSockets history filter window.

In the WebSockets history filter window, click Script mode.

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

Burp compiles your script and applies it to every item already logged in your WebSockets history, as well as any future WebSocket traffic generated in this project.

Creating custom scripts

You can write your own scripts directly in the WebSockets history filter window, using built-in templates or from a blank definition.

Note

Before you begin writing, we recommend exploring our Bambdas GitHub repository. There may be an existing script that meets your needs or provides inspiration for creating your own.

Converting filter settings to scripts

You can convert filter settings to a script as a starting point for further customization:

In Proxy > WebSockets history, click the filter bar to open the WebSockets

history filter window.

Make changes to the filter settings as necessary.

At the bottom of the WebSocket history filter window, click Convert to script.

Your filter is converted into a script, enabling you to customize it further using Java.

Creating your script

Two objects of the Montoya API are available to help you write your script:

ProxyWebSocketMessage

Utilities

To create a script to filter your WebSockets history:

In Proxy > WebSockets history, click the filter bar to open the WebSockets history

filter window.

In the WebSockets history filter window, click Script mode.

If you want to create your script from a built-in template, select New > From template. Select a template from the list, then click

Create using this template.

Write your script using Java.

Click Apply to compile and test the script. Fix any errors shown in the Compilation errors panel. For more information, see Troubleshooting scripts.

[Optional] Click Save to library > Save. The script is saved to your Bambda library for future use across Burp.

Click Apply & close.

Burp compiles your script and applies it to every item already logged in your WebSockets history, as well as any future WebSockets traffic generated in this project.

Warning

Using slow running or resource-intensive scripts can slow down Burp. Write your script carefully to minimize performance impact.

Example script

This example script filters the WebSockets history to show only items that meet the following criteria:

The message must be sent from the server.

The message payload length must be greater than 300 characters.

In this example, our script is:

return message.payload().length() > 300 && message.direction() == Direction.SERVER_TO_CLIENT;

Related pages

To get feedback, showcase your work, and connect with other developers, share your script on our PortSwigger

Discord #bambdas channel.

To share your scripts with the community, add them to our ever-growing GitHub repository. For more information, see Submitting scripts to our GitHub repository.
