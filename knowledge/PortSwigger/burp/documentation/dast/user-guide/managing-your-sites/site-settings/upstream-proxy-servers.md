# Configuring upstream proxy servers

Source: https://portswigger.net/burp/documentation/dast/user-guide/managing-your-sites/site-settings/upstream-proxy-servers
Fetched: 2026-06-28T09:15:38.725641+00:00

DAST

Configuring upstream proxy servers

Last updated:

June 18, 2026

Read time:

2 Minutes

Cloud

Self-hosted

You can configure Burp to send outgoing requests to an upstream proxy server, rather than directly to the destination web server.

You can add upstream proxy server rules when you add or edit a site or folder:

Select the site's Details tab and click Edit.

Under Scan settings, go to Connections > Upstream proxy servers.

Click Add upstream proxy server.

In the dialog, specify the upstream proxy server rule:

Destination host - Enter the destination web server address that you want the rule to apply to. You can use wildcards: * matches zero or more characters, and ? matches any character except a dot. To configure a rule for all traffic, enter

* as the destination host.

Proxy host - Enter the proxy host address. To create a rule for a direct, non-proxied connection, leave this blank.

Proxy port - The port that the proxy uses.

Authentication type - Choose from Basic, NTLM v1, or NTLM v2.

Username - Enter a username.

Password - Enter a password.

Domain - Only required for NTLM authentication. Enter your domain name.

Domain hostname - Only required for NTLM authentication. Enter the name of your domain server.

SPNEGO encoding - Only applies to NTLM authentication.

Negotiate auth scheme - Only applies to NTLM authentication.

Click Finish to close the dialog box.

Click Save to apply your changes.

The server is added to the list in the Upstream proxy tab. All traffic to the destination host is now sent to the specified proxy host instead.

To configure additional rules, click Add upstream proxy server, then follow the steps above. Burp uses the first rule in the list that matches the destination web server. This enables you to configure different rules for different destination hosts, or create an exception to a broader rule.

If it cannot find an applicable upstream proxy rule, Burp uses a direct, non-proxied connection.

To edit upstream proxy servers, click the edit icon .

To delete upstream proxy servers, click the trash icon .

Related pages

For information about how settings from folders and sites combine, see How scan configurations are combined.

You can also configure upstream proxy servers in a custom scan configuration. For more information, see Custom scan configuration settings.
