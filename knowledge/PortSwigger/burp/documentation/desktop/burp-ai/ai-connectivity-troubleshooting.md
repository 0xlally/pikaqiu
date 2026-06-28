# Troubleshooting AI connectivity

Source: https://portswigger.net/burp/documentation/desktop/burp-ai/ai-connectivity-troubleshooting
Fetched: 2026-06-28T09:15:44.913396+00:00

Support Center

Documentation

Desktop editions

Burp AI

Troubleshooting AI connectivity

Professional

Troubleshooting AI connectivity

Last updated:

June 18, 2026

Read time:

2 Minutes

To use Burp AI, your network must allow outbound HTTPS traffic to ai.portswigger.net on port 443.

If your organization uses a firewall or content filtering tool, make sure ai.portswigger.net is allowlisted. You may need to ask a network administrator to do this.

Common connectivity problems

If you can't see your AI credits or use Burp's AI features, the cause is likely to be one of the following:

You're offline.

Your network requires an upstream proxy.

An intercepting proxy is intercepting and re-signing traffic with its own certificate. Burp doesn't trust self-signed certificates by default, so it blocks the connection.

This page provides a step-by-step guide to help you troubleshoot common connectivity problems.

Step 1: Check your internet connection

Make sure your computer is online and able to access PortSwigger's AI services. To do this:

Open a browser and visit https://portswigger.net to confirm general internet access.

Try visiting https://ai.portswigger.net. You should see a 404 Not Found message - this is expected and confirms that your network can reach Burp's AI platform.

If either step fails, check your network settings or contact your administrator.

Step 2: Configure an upstream proxy

Some networks require an upstream proxy to access the internet. If this applies to your environment:

In Burp, click Settings. The Settings dialog opens.

Go to Network > Connections.

Under Upstream proxy servers, click Add. The Add upstream proxy rule dialog opens.

Enter the required proxy details. For more information, see Connections settings - Upstream proxy servers.

Click OK.

The new upstream proxy rule is added to the table.

Step 3: Identify and resolve an intercepting proxy

Some networks use intercepting proxies, such as ZScaler, that decrypt HTTPS traffic and re-sign certificates. Burp doesn't trust these certificates by default, which can block access to AI services.

To check if an intercepting proxy is affecting your connection:

In Burp's browser, go to https://ai.portswigger.net.

In Burp, go to Settings > Network > TLS.

Under Server TLS certificates, find the entry for ai.portswigger.net.

Check the certificate issuer:

If the issuer is a well-known CA provider such as Amazon, it's unlikely that an intercepting proxy is interfering with the connection.

If the certificate is issued by an intercepting proxy (such as ZScaler), or your company's security system, then your traffic is being intercepted.

If your traffic is being intercepted by a proxy, Burp might not trust the proxy's certificate. This can prevent access to AI features.

To fix this, add the proxy's certificate authority (CA) to Burp's trusted certificates:

Find the path to the proxy's certificate. If you're unsure, check your system settings or ask a network administrator.

In Burp, go to Settings > Network > TLS.

Under Custom CA certificates, click Add.

Select the certificate file.

Restart Burp, then check whether you can access AI features.
