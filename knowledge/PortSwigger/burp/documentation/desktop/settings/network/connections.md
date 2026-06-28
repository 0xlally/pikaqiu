# Connections settings

Source: https://portswigger.net/burp/documentation/desktop/settings/network/connections
Fetched: 2026-06-28T09:15:54.799433+00:00

Support Center

Documentation

Desktop editions

Settings

Network

Connections

ProfessionalCommunity Edition

Connections settings

Last updated:

June 18, 2026

Read time:

4 Minutes

The Connections settings enable you to define how Burp handles network traffic. You can configure:

Platform authentication.

Timeouts.

Upstream proxy servers.

SOCKS proxy.

Platform authentication

These settings enable Burp to carry out automatic platform authentication to destination web servers. You can configure authentication types and credentials for individual hosts, and disable platform authentication on a per-host basis.

To add platform authentication credentials, select Do platform authentication and select Add to display the Add platform authentication credentials dialog. From here, you can add the following information:

Destination host.

Authentication type - This can be either Basic, NTLMv1, or NTLMv2.

Username.

Password.

Domain.

Domain hostname.

You can also Edit and Remove credentials from the list if required.

If you select Prompt for credentials on platform authentication failure, then Burp displays an interactive popup whenever it encounters an authentication failure.

The Platform authentication settings can apply at both user and project level. If you select Override options for this project only, the selected settings only apply to the current project.

Timeouts

You can specify the timeout thresholds that Burp uses when performing various network tasks:

Connect - Used when connecting to a server. This setting determines how long Burp waits for a response after opening a socket, before deciding that the server is unreachable.

Normal - Used for most network communications. This setting determines how long Burp waits before abandoning a request and recording a timeout.

Open-ended responses - Used where a response that does not contain a Content-Length or Transfer-Encoding HTTP header is being processed. Burp waits for the specified interval before determining that the transmission is complete.

Domain name resolution - This setting determines how often Burp re-performs successful domain name look-ups. This should be set to a low value if target host addresses change frequently.

Failed domain name resolution - This setting determines how often Burp reattempts unsuccessful domain name look-ups.

Values are in seconds. If you set any of these settings to zero or leave them blank, Burp will never time out when performing that function.

The Timeouts settings are project settings. They apply to the current project only.

Upstream proxy servers

These settings control whether Burp sends outgoing requests to an upstream proxy, rather than directly to the destination host.

You can define rules that specify different proxy settings for different destination hosts. Burp evaluates the rules in order and uses the first rule in the table that matches the destination host.

If no rule matches the destination host, Burp connects directly to it.

To add a new rule, click Add to display the Add upstream proxy rule dialog. You can specify the following information:

Destination host - The destination host address. You can use wildcards: * matches zero or more characters, and ? matches any character except a dot.

Proxy host - The address of the upstream proxy. If blank, Burp connects directly to the destination host.

Proxy port.

Authentication type - Basic, NTLMv1, or NTLMv2.

Description - An optional label to help identify the rule.

Depending on the selected Authentication type, additional fields are displayed:

Username.

Password.

Domain - NTLM only.

Domain hostname - NTLM only.

SPNEGO encoding - NTLM only.

Negotiate auth scheme - NTLM only.

To send all traffic through a single upstream proxy, create a rule with * as the destination host. To exclude specific destination hosts, create rules for those hosts with the

Proxy host field left blank.

Use the buttons beside the list to Edit rules, move them Up and Down the list (to change the order in which they're applied), or Remove them.

The Upstream proxy servers settings can apply at both user and project level. If you select Override options for this project only, these settings only apply to the current project.

SOCKS proxy

Use these settings to send all outbound Burp traffic through a SOCKS proxy. This works at the TCP level, so every outbound connection, including requests to upstream HTTP proxies, goes through the SOCKS proxy.

These settings can be applied at the user or project level. To apply them only to the current project, select Override options for this project only.

To configure a SOCKS proxy:

Select Use SOCKS proxy.

Select Configure to open the configuration dialog.

Enter the SOCKS proxy host and SOCKS proxy port. If required, enter a Username and Password.

To resolve domain names through the proxy instead of locally, select Do DNS lookups over SOCKS proxy. When enabled, Burp does not perform any local DNS lookups.

Select OK.

When enabled, a summary of the SOCKS proxy configuration is displayed beneath the Use SOCKS proxy toggle.

To bypass the SOCKS proxy for specific hosts, add entries to the Hosts to bypass SOCKS proxying list. Use Add to enter hosts manually, or Paste or Load to add multiple entries. Use Remove or Clear to delete entries.
