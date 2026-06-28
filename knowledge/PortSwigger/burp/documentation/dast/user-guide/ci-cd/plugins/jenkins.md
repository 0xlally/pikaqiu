# Integrating Burp Suite DAST with Jenkins

Source: https://portswigger.net/burp/documentation/dast/user-guide/ci-cd/plugins/jenkins
Fetched: 2026-06-28T09:15:35.790851+00:00

DAST

Integrating Burp Suite DAST with Jenkins

Last updated:

June 18, 2026

Read time:

1 Minute

Integrating Burp Suite DAST with Jenkins is made simple thanks to our Jenkins plugin. Before beginning, you should decide which integration type you want to configure. In most cases, we recommend the site-driven scan option.

Integrating with Jenkins involves the following steps.

Create an API user

Regardless of which integration type you want to configure, you first need to create an API user.

Read more

Creating an API user for the CI/CD integration

Download and install the plugin

We provide a plugin for Jenkins to make the integration process as simple as possible. Please note that this requires Java 11 and Jenkins version 2.164.1 or higher.

Go to our website and download the Jenkins plugin. The download contains a file with the extension .hpi.

Log in to Jenkins as an administrator.

Go to Manage Jenkins > Manage Plugins and open the Advanced tab.

Under Upload Plugin, upload the HPI file that you just downloaded. The plugin will begin installing.

Once the upload is complete, restart Jenkins.

When creating new build steps, you should now see two new types available for selection: Burp site-driven scan and Burp scan.

Configure the integration

The steps for configuring the integration differ greatly depending on whether you want to use the site-driven scan or Burp scan option.

Read more

Configuring a site-driven scan (recommended)

Configuring a Burp scan
