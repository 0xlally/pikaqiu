# Setting up a self-hosted scanning machine for a Cloud instance

Source: https://portswigger.net/burp/documentation/dast/user-guide/managing-scanning-resources/cloud/setup
Fetched: 2026-06-28T09:15:37.732340+00:00

DAST

Setting up a self-hosted scanning machine for a Cloud instance

Last updated:

June 18, 2026

Read time:

2 Minutes

Cloud

We provide an installer for Windows and Linux operating systems. You can download these from Burp Suite DAST.

Prerequisites

The infrastructure meets the system requirements for self-hosted scanning machines.

You have configured your network and firewall settings.

Downloading the installer

From the settings menu , select Scanning resources.

Click Manage scanning machines.

On the Self-hosted scan settings page, click Add scanning machine.

Click Generate token, and save the authentication token. You cannot retrieve the authentication token later, so keep it somewhere safe.

Choose your operating system and copy the URL.

Use the URL to download the installer.

Running the installer

Unzip and run the installer. For Linux, run the installer from the terminal.

The wizard opens. Follow the wizard, and enter the authentication token when prompted.

Enter the hostname of your instance when prompted. The format should look something like this:

xxxxxx.portswigger.cloud

Click Next. The scanning machine will be installed.

In Burp Suite DAST, the new scanning machine is displayed under Self-hosted scanning machines. The

Health status shows as Starting, and then Connected.

Note

For Linux, you need to do some additional steps to enable browser-powered scanning. This gives you access to the full capabilities of Burp Scanner. For more information, see Browser-powered scanning for Burp Suite DAST.

Scanning your sites with self-hosted scanning machines

The new scanning machine is automatically added to a default self-hosted scanning pool. A scanning pool determines which sites are scanned by which machines.

In order to use your self-hosted scanning machine, you need to assign your sites to use the same scanning pool.

If you don't assign your site to a scanning pool, the PortSwigger-hosted scanning machines are used by default.

To learn how to reassign a site to your scanning pool, see Reassigning a site to a different pool.

Related pages

Managing self-hosted scanning machines with a Cloud instance

Managing scanning pools

Assigning scan limits
