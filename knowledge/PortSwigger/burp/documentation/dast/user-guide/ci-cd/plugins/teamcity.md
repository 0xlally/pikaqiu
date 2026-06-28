# Integrating Burp Suite DAST with TeamCity

Source: https://portswigger.net/burp/documentation/dast/user-guide/ci-cd/plugins/teamcity
Fetched: 2026-06-28T09:15:36.091199+00:00

DAST

Integrating Burp Suite DAST with TeamCity

Last updated:

June 18, 2026

Read time:

1 Minute

Integrating Burp Suite DAST with TeamCity is made simple thanks to our TeamCity plugin. Before beginning, you should decide which integration type you want to use. In most cases, we recommend the site-driven scan option.

Integrating with TeamCity involves the following steps.

Create an API user

Regardless of which integration type you want to use, you first need to create an API user.

Read more

Creating an API user for the CI/CD integration

Download and install the plugin

We provide a plugin for TeamCity to make the integration process as simple as possible.

Go to our website and download the TeamCity plugin. The download contains a ZIP file, but you do not need to unzip this.

Log in to TeamCity as an administrator.

Go to Administration > Plugins.

Click Upload plugin zip and upload the ZIP file that you just downloaded.

Once the plugin has been installed, you will be returned to the plugins list. In the yellow notification box, click Enable uploaded plugins.

When creating new build steps, you should now see two new build runner types available for selection: Burp site-driven scan and Burp scan.

Configure the integration

The steps for configuring the integration differ greatly depending on whether you want to use the site-driven scan or "Burp scan" option.

Read more

Configuring a site-driven scan (recommended)

Configuring a Burp scan
