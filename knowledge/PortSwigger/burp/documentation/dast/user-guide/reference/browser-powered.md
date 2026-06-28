# Browser-powered scanning for Burp Suite DAST

Source: https://portswigger.net/burp/documentation/dast/user-guide/reference/browser-powered
Fetched: 2026-06-28T09:15:39.099504+00:00

DAST

Browser-powered scanning for Burp Suite DAST

Last updated:

June 18, 2026

Read time:

4 Minutes

Browser-powered scanning is an invaluable feature that unleashes the full capability of Burp Scanner. When browser-powered scanning is enabled, Burp Scanner uses Burp's browser to perform all navigation during both the crawl and audit phases of a scan. Navigating the target in this way enables it to accurately handle virtually any client-side technology that a modern browser can. This has the potential to offer dramatically increased coverage compared to the previous crawler engine.

Browser-powered scanning is almost a necessity in order to perform truly comprehensive automated testing on many modern websites. For example, some websites have a navigational UI that is dynamically generated using JavaScript, which means that it is not present in the raw HTML. In this case, the previous crawler engine would be unable to render the full content and might miss key vulnerabilities as a result. However, when crawling using Burp's browser, Burp Scanner is able to load the page, execute any scripts required to build the UI, and then continue crawling as normal.

Browser-powered scans can also handle cases where the website modifies requests on-the-fly using JavaScript event handlers. By using Burp's browser, Burp Scanner is able to trigger the relevant events and execute the corresponding script, modifying any requests as needed.

Enabling browser-powered scanning also allows you to take advantage of some new features that rely on Burp's browser to work. Most notably, you can record and upload full login sequences so that Burp Scanner is able to successfully handle more complex login mechanisms, including single sign-on.

How to enable browser-powered scanning for Burp Suite DAST

Many users won't need to do anything to enable browser-powered scanning. When using the default scan configuration, Burp Scanner will automatically check your machine's specs. If it appears to meet the system requirements, all scans will use Burp's browser by default. Otherwise, scans will revert to the previous crawler engine.

If you prefer, you can also manually enable or disable browser-powered scanning in your scan configuration. You can find this option under Crawling > Discovery logic > Use Burp's browser for crawl and audit. For many users, it makes sense to create a dedicated scan configuration for this setting so that you can easily control which scans use Burp's browser on a case-by-case basis.

Enabling browser-powered scanning on Linux machines

When you're trying to use a Linux machine to run a browser-powered scan, you may encounter the following error message:

Crawl was configured to use Burp's browser, but a browser could not be started.

This is usually due to one of the following issues:

One or more libraries that are required by Burp's browser are not installed.

Burp's browser's sandbox is owned by the wrong system user.

To fix this, please follow the appropriate instructions for your machine below.

Note

Burp's browser is installed to Burp Suite DAST's data directory. By default, this is /var/lib/BurpSuiteEnterpriseEdition. If you specified a different location during the installation, remember to adjust the path accordingly when running the provided commands.

Red Hat Enterprise Linux (RHEL) and CentOS

Install the Extra Packages for Enterprise Linux (EPEL) as described here.

Run the following command to install Chromium:

sudo yum install chromium

Create the file /etc/sysctl.d/99-burpsuite.conf with the following content:

user.max_user_namespaces=1024

Switch to the burpsuite user.

Run the following command to launch Burp's browser in headless debugging mode:

/var/lib/BurpSuiteEnterpriseEdition/burpbrowser/<version>/chrome --headless=old --remote-debugging-port=0

If this prints out Devtools is listening on the following URL to the command line, try running a browser-powered scan again. If you see a different error on the command line, or are still having issues with the scan, follow the troubleshooting steps for All other Linux distributions.

All other Linux distributions

For all other Linux distributions, see the instructions below.

Note

Scanning with Burp Suite DAST is no longer compatible with Amazon Linux 2.

Navigate to the installation directory for Burp's browser:

cd /var/lib/BurpSuiteEnterpriseEdition/burpbrowser/<version>

Check which user owns the chrome-sandbox file. If it's owned by root, skip to the next step. If it's owned by the burpsuite user, run the following commands to pass ownership to the root user:

chown root:root /var/lib/BurpSuiteEnterpriseEdition/burpbrowser/<version>/chrome-sandbox

chmod 4755 /var/lib/BurpSuiteEnterpriseEdition/burpbrowser/<version>/chrome-sandbox

Switch to the burpsuite user.

Run the following command to launch Burp's browser in headless debugging mode:

/var/lib/BurpSuiteEnterpriseEdition/burpbrowser/<version>/chrome --headless=old --remote-debugging-port=0

If this prints out Error while loading shared libraries to the command line, either install the missing libraries individually or install the latest stable Chrome package and try again.

If this prints out Devtools is listening on the following URL to the command line, try running a browser-powered scan again.

If you see a different error on the command line, or are still having issues with the scan, please contact our Support team.

Note

Each version of Burp's browser has its own chrome-sandbox file. Unfortunately, if you had to change the owner of this file to fix the problem, you will need to make this change each time you install a Burp Scanner update that includes a new Chromium version. Please keep this in mind, especially if you have enabled auto-updates for Burp Scanner.
