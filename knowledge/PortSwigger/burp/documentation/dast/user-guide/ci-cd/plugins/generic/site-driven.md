# Configuring a site-driven scan using the generic CI/CD driver

Source: https://portswigger.net/burp/documentation/dast/user-guide/ci-cd/plugins/generic/site-driven
Fetched: 2026-06-28T09:15:35.833531+00:00

DAST

Configuring a site-driven scan using the generic CI/CD driver

Last updated:

June 18, 2026

Read time:

2 Minutes

In this section, we'll provide step-by-step instructions on how you can configure a site-driven scan using our generic CI/CD driver.

Prerequisites

You have created an API user in Burp Suite DAST and have access to the corresponding API key

You have finished setting up the site that you want to scan in Burp Suite DAST. We recommend running a couple of scans from the web UI to make sure that you're happy with the scan configuration and crawler behavior.

Add the build steps to your pipeline

On your preferred CI/CD platform, open the pipeline in which you want to incorporate a scan. Alternatively, create a new freestyle project if you just want to test the integration process.

Make sure your pipeline deploys the application that you want to scan to the same URL as the corresponding site in Burp Suite DAST.

Set up your pipeline so that it has access to the generic CI/CD driver from our website and a suitable JRE for running the JAR. For reference, the driver was built using Java 9.

Add either an "Execute shell" or "Execute Windows batch command" build step.

Enter a command that will run the driver with the appropriate parameters for the scans that you want to trigger. For a site-driven scan, you must include:

The URL of your DAST server

The --api-key for the API user that you created earlier

The --site-id of the site that you want to scan. You can find this ID in the URL of a site in the web UI:

https://your-enterprise-server.com:8080/sites/<site-id>

You can then add optional parameters to control different settings, such as how the scan results will affect your build. A typical command might look something like this:

java -jar path/to/ci-driver.jar https://your-enterprise-server:8080 --api-key=secret --site-id=7 --min-severity=high --min-confidence=certain --report-file=scan-report.html --report-type=summary

Save your pipeline.

Note

For detailed information about the available parameters and which settings they control, please refer to our parameter reference guide or use the --help option.

Test your integration

After you finish configuring the build step, it's a good idea to check whether the integration is working correctly and that your scan is able to run successfully.

Kick off a build on demand and look at the console output. You should see the scan initialize and start crawling. Throughout the scan, you can check the status by monitoring the console output for the build.

In Burp Suite DAST, go to your site and open the Scans tab. You should see the build-initiated scan in the list.
