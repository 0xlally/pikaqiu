# Collaborator settings

Source: https://portswigger.net/burp/documentation/desktop/settings/project/collaborator
Fetched: 2026-06-28T09:15:55.617695+00:00

Support Center

Documentation

Desktop editions

Settings

Project

Collaborator

Professional

Collaborator settings

Last updated:

June 18, 2026

Read time:

3 Minutes

Burp Collaborator is an external service that Burp can use to help discover many kinds of vulnerabilities, such as external service interaction and out-of-band XSS.

Note

For more details about how Burp Collaborator works, see Burp Collaborator.

The Burp Collaborator server settings enable you to choose which Collaborator server you want to use:

Use the default Collaborator server - Select this setting to use a public, shared Collaborator server provided by PortSwigger. PortSwigger makes no warranty about the availability or performance of this server. If the public Collaborator server suffers from any service outage or degradation, then Collaborator-related functionality within Burp may be affected.

Don't use Burp Collaborator - Select this setting to disable all of Burp's Collaborator-related capabilities.

Use a private Collaborator server - Select this setting to use your own instance of the Collaborator server. For more information on this process, see Deploying a private Collaborator server.

Note

We periodically add new domain names for the public Collaborator server to reduce the chance of WAF blacklisting, which results in false negatives. By default, Burp Collaborator uses the domain in use when your version of Burp Suite Professional was released.

Currently, the domains in use are *.burpcollaborator.net or *.oastify.com. Make sure that your machine and target application can access both these domains on ports 80 and 443.

If you choose to use a private Collaborator server then you need to configure its location. You can provide the following information:

Server location - This is the domain name or IP address of your server. If you specify an IP address then any Collaborator-related functionality that relies on DNS resolution will not be available. For more details, see Setting up the domain and DNS records.

Polling location (optional) - You can specify the location in which your private Collaborator server answers polling requests. Collaborator servers can be configured to receive interactions and answer polling requests on different network interfaces, if required. You can specify the polling location by hostname or IP address, with an optional port number separated by a colon. For example, 10.20.30.40:8008.

Note

If you have configured your Collaborator Server to use non-standard ports, then you must specify those ports here.

For more information on configuring non-standard ports, see Setting up the ports and firewall.

The following options are also available:

Poll over unencrypted HTTP - By default, Burp polls the Collaborator server over HTTPS, and enforces TLS trust to prevent man-in-the-middle attacks. If your instance of Burp is unable to poll directly over HTTPS (for example, due to your network configuration), you can opt to poll over unencrypted HTTP.

Run health check - Select this setting to perform a quick health check of your configured Collaborator server. Burp verifies whether it is possible to interact with the server using various network services, and whether it can retrieve the details of these interactions via polling. Based on these tests, you can determine whether Burp is likely to be able to make use of the Collaborator's features.

By default, Burp Collaborator server settings are user settings, affecting all Burp installations on your

machine.

To make settings specific to the current project, switch the Override options for this project only toggle to

On.

Existing project file settings won't be affected as they will automatically have this setting enabled by

default.
