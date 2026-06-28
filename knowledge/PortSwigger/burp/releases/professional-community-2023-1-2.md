# Professional / Community 2023.1.2

Source: https://portswigger.net/burp/releases/professional-community-2023-1-2
Fetched: 2026-06-28T09:16:39.717387+00:00

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

We have upgraded the Montoya API to version 2023.1, which enables Burp extensions to store and manage data in project files. Any BApps that you develop with version 2023.1 will be compatible with future versions of Burp, as all future changes to the API will be backwards compatible.

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

Macro updates

You can now define a prefix and suffix for a custom macro parameter. This can be useful, for example, to support Authorization headers, which require a static prefix followed by a dynamic value.

In addition, you can now set headers using macro parameters. When a parameter matches a request header, then Burp replaces the header value with the macro parameter value. This enables you to test APIs without configuring a Burp Extension.

Improvements to Burp Scanner

This release includes several minor improvements to authenticated crawling with popup-based login mechanisms:

We have added a wait after the final event in a recorded sequence. This means that the sequence now captures links that are added by the final page after a delay.

When you login after receiving a temporary failure status code, Burp now authenticates subsequent requests for the same resource.

When you change the Await navigation timeout in a crawler configuration, it now automatically updates in the recorded login sequence replayer. It is also stored in the crawler tuning.

Bug fixes

We have fixed a bug whereby Burp Repeater tabs were not functioning correctly when there was an absolute URL in the request line.

We have also released a couple of bug fixes related to the Montoya API:

Previously, the Javadoc incorrectly stated that the passiveAudit() method of the ScanCheck interface returns null if no issues are identified. The method in fact returns an empty AuditResult object if no issues are identified. We have updated the Javadoc.

We have fixed a bug whereby the copyToTempFile() was causing null pointer exceptions.

Browser update

This release upgrades Burp's browser to Chromium 110.0.5481.77/.78.

Note for Windows Server 2012 and Windows 7/8/8.1 users

Due to a recent Chrome upgrade, Burp Scanner is no longer compatible with the Windows Server 2012 and Windows 7/8/8.1 operating systems. For more information, see the related Chrome announcement.
