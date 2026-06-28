# Professional / Community 2023.1

Source: https://portswigger.net/burp/releases/professional-community-2023-1
Fetched: 2026-06-28T09:16:39.907226+00:00

In this release, we have moved more of Burp Suite’s settings into the Settings dialog, making them easier to find and use. We have also upgraded the Montoya API, made improvements to macro functionality, and made various minor improvements.

Settings restructure

We have moved more settings into Burp’s Settings dialog. In particular, we have added:

All settings related to the following Burp tools into the Tools section:

Proxy.

Repeater.

Sequencer.

Intruder - User settings only. Intruder attack configuration settings remain in the Intruder attack tab.

A new page for extensions.

A new page for the configuration library.

Target scope settings into the Scope section.

Resource pools and task auto-start settings into the Tasks section.

As part of this restructuring, we have also:

Added the Repeater Default tab group setting. This enables you to configure the tab group that requests are added to by default when sent to Repeater.

Updated the viewing panel for the Hotkeys settings. This enables you to edit hotkeys from this panel directly.

Moved Inspector settings into the Message editor page.

Montoya API persistence

We have upgraded the Montoya API to version 1.0.0, which enables Burp extensions to store and manage data in project files. Any BApps that you develop with version 1.0.0 will be compatible with future versions of Burp, as all future changes to the API will be backwards compatible.

You can now use the Montoya API to:

Store extension settings and data in the current Burp project. The API can store data both to project files that were created on startup and to temporary projects that you subsequently save to a project file. Each extension can only access its own data.

Select whether or not extension data is saved when you save a copy of the current project.

Import extension data from another project file.

The Montoya API offers support for the following data types:

Primitives.

Strings.

Booleans.

Requests.

Responses.

Byte arrays.

Lists.

Hierarchies.

Note that this functionality is not available in Burp's old Wiener API. You can only write extensions that support data storage and retrieval using the Montoya API from version 1.0.0 onwards.

Macro updates

You can now define a prefix and suffix for a custom macro parameter. This can be useful, for example, to support Authorization headers, which require a static prefix followed by a dynamic value.

In addition, you can now set headers using macro parameters. When a parameter matches a request header, then Burp replaces the header value with the macro parameter value. This enables you to test APIs without configuring a Burp Extension.

Bug fix

We have fixed a bug whereby Burp Repeater tabs were not functioning correctly when a request was sent to portswigger.net and the path was then changed to an absolute URL.

Browser update

This release upgrades Burp's browser to Chromium 109.0.5414.74/.75/.87.
