# Configuring a site-driven scan in TeamCity

Source: https://portswigger.net/burp/documentation/dast/user-guide/ci-cd/plugins/teamcity/site-driven
Fetched: 2026-06-28T09:15:36.700213+00:00

DAST

Configuring a site-driven scan in TeamCity

Last updated:

June 18, 2026

Read time:

2 Minutes

To integrate Burp Suite DAST with TeamCity, we recommend using the site-driven scan option. In this section, we'll provide step-by-step instructions on the full configuration process.

Prerequisites

You have created an API user in Burp Suite DAST and have access to the corresponding API key

You have installed the plugin in TeamCity.

You have finished setting up the site that you want to scan in Burp Suite DAST. We recommend running a couple of scans from the web UI to make sure that you're happy with the scan configuration and scanner behavior before starting the CI/CD integration.

Whitelist your TeamCity URL

Site-driven scans interact with your DAST server via the GraphQL API. In order to support this behavior, you need to whitelist your TeamCity URL so that TeamCity can make the necessary cross-origin requests for retrieving your site tree and creating new scans.

Log in to Burp Suite DAST as an administrator.

From the settings menu, select Network.

On the network settings page, scroll down to the Allowed Origins for GraphQL API section.

In the provided field, enter your TeamCity URL, including the protocol and port. For example:

https://your-teamcity-domain.com:8080

Save your entries.

Read more

Whitelisting an application for CORS

Create the site-driven scan build step in TeamCity

Log in to TeamCity.

Open the pipeline in which you want to incorporate a scan. Alternatively, create a new dummy project if you just want to test the integration process.

Make sure your pipeline deploys the application that you want to scan to the same URL as the corresponding site in Burp Suite DAST.

Add a new build step and select the runner type Burp site-driven scan.

Enter the URL of your DAST server. This is the URL that you normally use to access Burp Suite DAST. Make sure you include the appropriate protocol and port. By default, this will be something like:

https://your-enterprise-server.com:8080

Enter the API key that you generated when creating the API user earlier. If you've lost this, you need to generate a new API key or create a new API user from the Burp Suite DAST web UI.

Once you have entered both of these values, your site tree will automatically be fetched from Burp Suite DAST. From the drop-down menu, select the site that you want to scan.

Adjust the various optional settings to fine-tune how the scan and its results will affect your build.

Save your pipeline.

Test your integration

After you finish configuring the build step, it's a good idea to check whether the integration is working correctly and that your scan is able to run successfully.

Kick off a build-on-demand and look at the build log in TeamCity. You should see the scan initialize and start crawling. Throughout the scan, you can check the status by monitoring the build log.

In Burp Suite DAST, go to your site and open the Scans tab. You should see the TeamCity-initiated scan in the list.
