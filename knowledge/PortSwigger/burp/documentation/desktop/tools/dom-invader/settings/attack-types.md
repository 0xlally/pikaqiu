# DOM Invader attack types

Source: https://portswigger.net/burp/documentation/desktop/tools/dom-invader/settings/attack-types
Fetched: 2026-06-28T09:16:02.926402+00:00

Support Center

Documentation

Desktop editions

Tools

DOM Invader

Settings

Attack types

ProfessionalCommunity Edition

DOM Invader attack types

Last updated:

June 18, 2026

Read time:

1 Minute

By default, DOM Invader automatically probes for ordinary DOM XSS sources and sinks, but you can optionally configure DOM Invader to attempt other attacks.

Prototype pollution

When this setting is enabled, DOM Invader automatically tries to identify sources for client-side prototype pollution in addition to the usual DOM XSS sources and sinks.

For more information on DOM Invader's prototype pollution features, see Testing for client-side prototype pollution.

You can click the cog icon next to this setting to access some additional settings for fine-tuning this behavior. For more information on configuration settings specific to prototype pollution, see Prototype pollution settings.

DOM clobbering

When this setting is enabled, DOM Invader automatically tries to identify DOM clobbering vulnerabilities.

For more information, see Testing for DOM clobbering with DOM Invader.
