# Configuring a Burp scan in Jenkins

Source: https://portswigger.net/burp/documentation/dast/user-guide/ci-cd/plugins/jenkins/burp-scan
Fetched: 2026-06-28T09:15:35.921840+00:00

DAST

Configuring a Burp scan in Jenkins

Last updated:

June 18, 2026

Read time:

3 Minutes

Configuring a Burp scan in Jenkins involves largely the same process as in previous versions of Burp Suite DAST. In this section, we'll provide step-by-step instructions for the full configuration process.

Note

Although we continue to support the legacy "Burp scan" option, for most users, we recommend configuring a site-driven scan instead.

Prerequisites

You have Java 11 installed on your machine.

You are using Jenkins 2.164.1 or higher

You have created an API user in Burp Suite DAST and have access to the corresponding API key

You have installed the plugin in Jenkins.

You have familiarized yourself with Burp Suite DAST's site-matching rules.

Create the Burp scan build step in Jenkins

The following steps are the minimum configuration requirements to integrate Jenkins with Burp Suite DAST.

Log in to Jenkins.

Open the pipeline in which you want to incorporate a scan. Alternatively, create a new freestyle project if you just want to test the integration process.

If you want to scan an existing site that you have already configured in Burp Suite DAST, make sure your pipeline deploys this application to the same URL. Alternatively, if you do not want the scan to be matched with an existing site, make sure you deploy the application to a unique URL.

Add either an Execute shell or Execute Windows batch command build step. In the "Command" field, enter a command that will echo the top-level URL of the running application that you want to scan and assign it to the variable BURP_SCAN_URL as follows:

echo BURP_SCAN_URL = https://application-to-scan.com

This step will output the target URL in its build log in the correct format for the plugin to process in the next step. If you have a more dynamic deployment process, for example, to a Docker container, you should repeat this command multiple times to output each of the relevant URLs. All of these will be aggregated and scanned.

Add another new build step, but this time select the type Burp scan.

Enter the URL of your Burp Suite DAST REST API endpoint. This is the URL that you copied after creating the API user earlier. Make sure you include the appropriate protocol and port.

If you want to be able to download scan reports, exclude the API key from this URL as follows and instead enter the API key in the dedicated field beneath. This is the recommended approach.

URL: https://your-enterprise-server:8080

API key: your-api-key

If you do not want to download scan reports, you can include the API in the URL. In this case, you should leave the API key field blank. We do not recommend this approach as it is primarily to provide continued support for legacy integrations that were configured before we adjusted the input fields.

URL: https://your-enterprise-server:8080/api/your-api-key

API key: [blank]

Adjust the various optional settings to fine-tune how the scan and its results will affect your build. For "Burp scans", you also have the options to:

Upload a custom scan definition to either customize the scan configuration for a one-time scan or override the default configuration for the matched site.

Define rules for ignoring issues. This is useful for setting false positives for a "Burp scan".

Note that this option is not available for "site-driven scans" because they inherit false positive rules from their associated site in Burp Suite DAST.

Save your pipeline.

Test your integration

After you finish configuring the build step, it's a good idea to check whether the integration is working correctly and that your scan is able to run successfully.

Kick off a build on demand and look at the console output in Jenkins. You should see the scan initialize and start crawling. Throughout the scan, you can check the status by monitoring the console output for the build. Issues that are found will also be output to the console.

In Burp Suite DAST, go to your site and open the Scans tab. You should see the Jenkins-initiated scan in the list.
