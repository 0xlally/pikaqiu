# Custom scan configuration settings

Source: https://portswigger.net/burp/documentation/dast/user-guide/reference/custom-scan-config-settings
Fetched: 2026-06-28T09:15:39.133674+00:00

DAST

Custom scan configuration settings

Last updated:

June 18, 2026

Read time:

4 Minutes

In Burp Suite DAST, custom configurations enable you to configure a number of scan settings, such as request throttling. You can define custom scan configurations for sites, folders, and subfolders.

When using a custom scan configuration, we recommend you review each setting to ensure they are configured to your requirements.

This section explains how to use a number of custom scan configuration settings.

Note

You can also use custom scan configurations to control Burp Scanner's crawl and audit behavior.

For more information about these settings, see Crawl settings and Audit settings.

Connections

Burp Suite DAST enables you to configure various connection settings, as described below:

Platform authentication

You can add credentials for NTLM and HTTP Basic authentication. This enables Burp Scanner to automatically authenticate to destination web servers at the platform level.

When configuring this setting, you need to provide:

Destination host - Enter the destination web server address that you want the rule to apply to, for example, ginandjuice.shop. You can use wildcards: * matches zero or more characters, and ? matches any character except a dot.

Type - Choose from Basic, NTLM v1, or NTLM v2.

Username - Enter a username.

Password - Enter a password.

Domain - Only required for NTLM authentication. Enter your domain name.

Domain hostname - Only required for NTLM authentication. Enter the name of your domain server.

The credentials are added to the list. Burp uses the first credentials in the list that match the destination web server. This enables you to configure authentication for individual hosts, or disable platform authentication for a specific host.

Note

You can also add platform authentication credentials in the site settings. For more information, see Configuring

platform authentication.

Upstream proxy servers

You can configure Burp to send outgoing requests to an upstream proxy server, rather than directly to the destination web server.

When configuring this setting, you need to provide:

Destination host - Enter the destination web server address that you want the rule to apply to. You can use wildcards: * matches zero or more characters, and ? matches any character except a dot. To configure a rule for all traffic, enter * as the destination host.

Proxy host - Enter the proxy host address. To create a rule for a direct, non-proxied connection, leave this blank.

Proxy port - The port that the proxy uses.

Authentication type - Choose from Basic, NTLM v1, or NTLM v2.

Username - Enter a username.

Password - Enter a password.

Domain - Only required for NTLM authentication. Enter your domain name.

Domain hostname - Only required for NTLM authentication. Enter the name of your domain server.

The server is added to the list. Burp uses the first rule in the list that matches the destination web server. This enables you to configure different rules for different destination hosts, or create an exception to a broader rule.

Note

You can also add upstream proxy servers in the site settings. For more information, see Configuring upstream proxy servers.

Client TLS

You can configure multiple client TLS certificates. When a host requests a client TLS certificate, Burp uses the first certificate listed for that host.

When configuring this setting, you will need to provide a hostname, password, and TLS certificate.

HTTP/2

Default to HTTP/2 if the server supports it - Requests sent by Burp will default to HTTP/2 if the server supports it.

Request Throttling

You can limit the frequency and number of concurrent requests Scanner makes, and impose intervals between those requests. This can prevent Scanner overloading the target server or exceeding its rate limit.

Enable concurrent request limiting - Limit how many requests are sent at the same time.

Throttle request interval - Set a delay between requests in milliseconds.

Add random variations to interval - Modifies the configured request interval by randomly adding or removing up to 50% of the request interval value. For example, a request interval of 500 will randomly vary between 250 and 750 milliseconds.

Auto backoff - Automatically adds a short delay between requests when the target server requests this behavior. This incrementally increases until the request limit complies with the server's rate limit.

Embedded Browser

Stop the embedded browser using the GPU - Stops Burp's embedded browser using the GPU during a scan. This can prevent crashes that occur if Burp's browser attempts to use a GPU where none are present.

Burp Collaborator Server

Burp Collaborator is a network service that enables you to detect invisible vulnerabilities. PortSwigger's shared, public Collaborator server is used by default. Alternatively, you can use your own instance.

PortSwigger makes no warranty about the availability or performance of its public Collaborator server. If it suffers from outage or degradation, then Collaborator-related functionality within Burp may be affected.

Collaborator type

Default - Burp uses a shared public Collaborator server provided by PortSwigger.

None - Burp does not use the Collaborator server, or any related functionality.

Private - Burp will use a server you specify for Collaborator, and then monitor for interactions with that server.

Server location - This is the domain name or IP address of your server. If you specify an IP address then any Collaborator-related functionality that relies on DNS resolution will not be available. For more details, see Setting up the domain and DNS records.

Poll over unencrypted HTTP - By default, Burp polls the Collaborator server over HTTPS, and enforces TLS trust to prevent man-in-the-middle attacks. If Burp cannot poll directly over HTTPS (for example, due to your network configuration), you can opt to poll over unencrypted HTTP.

Polling location (optional) - Specify the location from which your private Collaborator server answers polling requests. Collaborator servers can be configured to receive interactions and answer polling requests on different network interfaces, if required. You can specify the polling location by hostname or IP address, with an optional port number separated by a colon. For example, 10.20.30.40:8008.

Related pages

Defining the scan configuration for a site.

Defining the scan configuration for a folder.

Crawl settings.

Audit settings.

Burp Collaborator.
