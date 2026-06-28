# DNS settings

Source: https://portswigger.net/burp/documentation/desktop/settings/network/dns
Fetched: 2026-06-28T09:15:54.985612+00:00

Support Center

Documentation

Desktop editions

Settings

Network

DNS

ProfessionalCommunity Edition

DNS settings

Last updated:

June 18, 2026

Read time:

1 Minute

The DNS settings enable you to configure:

Preferred IP version for DNS resolution.

Hostname resolution overrides.

Preferred IP version for DNS resolution

These settings enable you to choose whether Burp prioritizes IPv4 or IPv6 addresses during DNS lookups, rather than relying on the operating system's default ordering. This is especially useful if routing restrictions allow only IPv4 or IPv6 traffic.

You can choose from the following options:

Use system's default behavior

Prefer IPv4

Prefer IPv6

The Preferred IP version for DNS resolution settings are project settings. They apply to the current project only.

Clearing the DNS cache

Click Clear DNS cache to clear Burp's DNS cache.

Hostname resolution overrides

These settings enable you to override your computer's DNS resolution by mapping hostnames to IP addresses. This can help you to make sure that requests are forwarded correctly when the Hosts file has been modified to invisibly proxy traffic from non-proxy-aware thick client components.

Each mapping comprises:

A hostname.

The IP address that should be associated with that hostname.

You can enable or disable rules individually using the checkbox on the list, and Edit or Remove rules using the buttons to the side.

The Hostname resolution overrides settings are project settings. They apply to the current project only.
