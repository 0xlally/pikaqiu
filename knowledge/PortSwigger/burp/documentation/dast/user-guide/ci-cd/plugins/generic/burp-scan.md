# Configuring a Burp scan using the generic CI/CD driver

Source: https://portswigger.net/burp/documentation/dast/user-guide/ci-cd/plugins/generic/burp-scan
Fetched: 2026-06-28T09:15:35.660379+00:00

DAST

Configuring a Burp scan using the generic CI/CD driver

Last updated:

June 18, 2026

Read time:

3 Minutes

In this section, we'll provide step-by-step instructions on how you can configure a Burp scan using our generic CI/CD driver.

Prerequisites

You have created an API user in Burp Suite DAST and have access to the corresponding API key

Add the build steps to your pipeline

The driver accepts URLs to scan as standard input (stdin) in the format BURP_SCAN_URL = https://application-to-scan.com. You can generate a list of URLs any way you want, as long as the output is passed in this format to the driver. For the purposes of this guide, we'll assume that you are outputting the URLs in a previous build step on your preferred CI/CD platform.

On your preferred CI/CD platform, open the pipeline in which you want to incorporate a scan. Alternatively, create a new freestyle project if you just want to test the integration process.

If you want to scan an existing site that you have already configured in Burp Suite DAST, make sure your pipeline deploys this application to the same URL. Alternatively, if you do not want the scan to be matched with an existing site, make sure you deploy the application to a unique URL.

Set up your pipeline so that it has access to the generic CI/CD driver from our website and a suitable JRE for running the JAR. For reference, the driver was built using Java 9.

Add either an "Execute shell" or "Execute Windows batch command" build step and enter the following command:

echo BURP_SCAN_URL = https://application-to-scan.com

This step will output the target URL in its build log in the correct format for the driver to process in the next step. If you have a more dynamic deployment process, for example, to a Docker container, you should repeat this command multiple times to output each of the relevant URLs. All of these will be aggregated and scanned.

Add another new "Execute shell" or "Execute Windows batch command" build step. Enter a command that will run the driver with the appropriate parameters for the scans that you want to trigger. For a Burp scan, you must include:

The API URL that you copied when creating the API user earlier.

If you want to download scan reports, you must also provide the API key for the API user that you created earlier. You should pass this in the --api-key parameter. This is the recommended approach. Alternatively, you can include the API key in the API URL as follows:

https://your-enterprise-server:8080/api/your-api-key

However, this means you will not be able to download scan reports and is primarily to provide continued support for legacy integrations that were configured using older versions of the driver.

You can then add optional parameters to control different settings, such as how the scan results will affect your build. A typical command might look something like this:

java -jar path/to/ci-driver.jar https://your-enterprise-server:8080 --api-key=secret --site-id=7 --min-severity=high --min-confidence=certain --report-file=scan-report.html --report-type=summary

Save your pipeline.

Note

For detailed information about the available parameters and which settings they control, please refer to our parameter reference guide or use the --help option.

Test your integration

After you finish configuring the build step, it's a good idea to check whether the integration is working correctly and that your scan is able to run successfully.

Kick off a build on demand and look at the console output. You should see the scan initialize and start crawling. Throughout the scan, you can check the status by monitoring the console output for the build. Issues that are found will also be output to the console.

In Burp Suite DAST, go to your site and open the Scans tab. You should see the build-initiated scan in the list.
