# Key settings

Source: https://portswigger.net/burp/documentation/desktop/settings/key-settings
Fetched: 2026-06-28T09:15:54.626520+00:00

Support Center

Documentation

Desktop editions

Settings

Key settings

ProfessionalCommunity Edition

Key settings

Last updated:

June 18, 2026

Read time:

2 Minutes

Burp Suite contains a wide range of settings, enabling you to configure the system to work with almost any workflow or target application.

This page gives a brief overview of some key settings that are useful in most projects.

Target scope

The target scope configuration tells Burp which hosts and URLs you are currently interested in and willing to attack. We recommend that you set a suite-wide target scope early in your testing in order to ensure that Burp does not target any inappropriate items.

Selecting a scope enables you to fine-tune the behavior of many of Burp's tools. For example:

You can filter the target site map and Proxy history to show only those items that are in-scope.

You can configure the Proxy to intercept only in-scope requests and responses.

Professional You can configure Burp Scanner to scan in-scope items automatically.

You can configure Intruder and Repeater to follow redirects to any in-scope URLs.

Related pages

Target scope.

Proxy history.

Site map.

Platform-level authentication

Burp can carry out platform-level authentication for any application servers that require it. You can configure different authentication types and credentials for individual hosts if needed.

Burp supports the following authentication types:

Basic

NTLMv1

NTLMv2

Related pages

Platform authentication.

Session handling rules and macros

Some applications contain security features that can hinder automated or manual testing, such as reactive session termination, use of per-request tokens, and stateful multi-stage processes.

Burp enables you to configure session handling rules and macros to deal with any session-related issues in the background, helping you to continue your testing uninterrupted.

Related pages

Sessions settings.

Schedule tasks

The task scheduler enables you to configure certain tasks to run automatically at defined times. You can use the task scheduler to start and stop certain automated tasks out of hours while you are not working, and to save your work periodically or at a specific time.

Related pages

Schedule tasks.

HTTP message appearance

You can configure the font and character set that Burp uses to display HTTP messages, and also specify the font used in Burp's own UI.

Related pages

Message editor settings.

Display settings.
