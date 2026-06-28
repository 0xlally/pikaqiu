# Startup behavior

Source: https://portswigger.net/burp/documentation/desktop/settings/suite/startup-behavior
Fetched: 2026-06-28T09:15:56.288800+00:00

Support Center

Documentation

Desktop editions

Settings

Suite

Startup behavior

ProfessionalCommunity Edition

Startup behavior

Last updated:

June 18, 2026

Read time:

2 Minutes

The Startup behavior tab enables you to control what happens when you open Burp.

Automated tasks on startup

This checkbox controls the default behavior of the Pause Automated Tasks setting in the startup wizard.

This setting protects you by preventing automated tasks from sending requests when you open Burp. This is especially useful if you open project files from unknown or untrusted sources.

Select Pause Automated Tasks if you want Burp to prevent any automated tasks from running when you open projects.

Deselect Pause Automated Tasks if you want Burp to run automated tasks when you open projects.

Note

If Trust this project file is deselected, automated tasks will be paused by default.

Pause automated tasks is a user setting. It applies to all installations of Burp on your machine.

Untrusted project files

This checkbox controls the default behavior of the Trust this project setting in the startup wizard.

This setting protects you against any potentially harmful project settings. This is especially useful if you open project files from unknown or untrusted sources.

Select Trust this project if you want projects to open with all of their original settings intact, including any potentially harmful ones.

Deselect Trust this project if you want Burp to remove any potentially harmful project settings from projects before opening them. This will also prevent any automated tasks from running.

Note

Even with these settings removed, we do not recommend proxying traffic through an untrusted project file.

Trust this project is a user setting. It applies to all installations of Burp on your machine.
