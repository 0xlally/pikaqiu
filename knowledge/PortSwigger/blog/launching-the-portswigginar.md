# Launching the PortSwigginar

Source: https://portswigger.net/blog/launching-the-portswigginar
Fetched: 2026-06-28T09:15:19.468388+00:00

Launching the PortSwigginar

Adam Armitt |

Thursday, 9 June 2022 at 23:00 UTC

Thank you to those who attended our recent PortSwigginar on Burp Suite Enterprise Edition. Below is the video of the session, which included;

A recap on “what’s new” within the tool for those who have not checked it out in a while.

How Burp Suite Professional and Burp Suite Enterprise Edition work together.

Understanding our licensing.

A run-through of our deployment options.

How to quickly set up a site and run a scan.

Launching a scan from a Jenkins pipeline.

Roadmap sneak peek!

Tune in here if you want to watch the full PortSwigginar

.

How can I join the next PortSwigginar?

We had some fantastic questions from those who attended, so we wanted to share the answers below for the benefit of anyone who missed out. Did the session reignite your interest in Burp Suite Enterprise Edition? Don’t forget you can purchase the tool directly from our site, or take a fresh trial to evaluate the tool.

Finally, if you would like to attend the next PortSwigginar or have any feedback on the session please email hello@portswigger.net, we would love to hear from you.

Questions from our audience

Does Burp Suite Enterprise Edition cover any healthcare compliance in the US to maintain patient healthcare data or PHI data? Is it HIPAA compliant?

We do not currently adhere to any specific healthcare compliant frameworks - however, Burp Suite Enterprise Edition is hosted within your own environment, which is where all scan data is stored.

What Linux distributions are supported for the installation of Burp Suite Enterprise Edition?

Burp Suite Enterprise Edition can be installed on any 64-bit Linux OS.

Can you provide additional documentation for the Kubernetes deployment? The Helm chart does not include a PVC manifest?

The PVC is a prerequisite and not included in the Helm chart. You can find more details in our documentation here.

Can Burp Suite Enterprise Edition run on ARM hardware?

Burp Suite Enterprise Edition is not compatible with ARM.

How is the database referenced in the Kubernetes deployment Helm chart?

There is no database included with the Helm chart. The database connection URL is configured after connecting to the Burp Suite Enterprise web console.

How does the web server work with the Enterprise server in Kubernetes deployment?

An example can be seen within our AWS reference architecture templates on the PortSwigger public GitHub repository.

What is the cost for Burp Suite Enterprise Edition including 15 concurrent scans?

15 concurrent scans is $11,985.00 for a 12-month subscription - a full pricing configurator is available here.

If a Jira issue is created based on scan findings, does the Jira integration also auto-close out such issues if rescans detect that a previous finding is no longer present?

The integration does not auto-close the Jira ticket, you will need to do this in Jira. We would always recommend performing further manual investigation to confirm any issues or remediation. Find more information on Jira integration here.

Can you elaborate on Burp Suite Enterprise Edition’s API capabilities, building custom plugins, and handling custom authentication?

Our GraphQL API exposes virtually all of the core functionality and data of Burp Suite Enterprise Edition.

To extend the functionality of Burp Scanner, extensions can be used, either from the existing free BApp Store or by creating your own custom extension.

For more complex application authentication, such as SSO, our recorded login feature can be used.

How do you support API testing? Can you import happy flow(s) into Burp Suite Enterprise Edition?

More information on Burp Suite Enterprise Edition’s automated API scanning capabilities can be found here.

Can Burp Suite Enterprise Edition navigate a captcha within a login form when authenticating an application?

We do not currently support captcha.

Do you only support the top 10 OWASP vulnerabilities? What about other vulnerabilities?

We have a compliance reporting template that maps against the latest OWASP Top 10 vulnerabilities. This is not the full scope of checks performed by the scanner. You can find the complete list of scan checks here.

Do you support API testing?

Yes, Burp Scanner supports some automated API scanning functions.

Can we customize the dashboard within Burp Suite Enterprise Edition?

Not currently, but we are planning to add this feature.

Can we group lists of URLs together, specifically for when scheduling scans?

Burp Suite Enterprise Edition performs crawl discovery of the application automatically. Each web application should be set up as a separate site, with the highest level URL for the application added as the site URL.

Is the grouping of URLs determinative? Is a scan executed one by one, or on URLs in the group?

Each web application is set up as a separate site in Burp Suite Enterprise Edition and scans are launched per site. Concurrent scans can be performed, providing you have available scanning resources and concurrent scan allowance - this will depend on the subscription you have purchased.

How does Burp Suite Enterprise Edition account for ephemeral web app session auth tokens that may “refresh” during a scan (e.g., AWS Cognito auth service tokens refreshing ~15 minutes and expiring tokens during a scan potentially aborting an in-progress scan)?

Session handling is performed automatically and our recorded login feature can be used for more complex application authentication, such as SSO. If a login session expires, the scanner will perform a new login.

For API scanning, at the moment only OpenAPI v3 can be parsed by Burp Scanner, are you looking to add more parsing capabilities, such as GraphQL maybe?

We may add new functionality and support to our automated API scanning in the future.

Can we perform a scan on a specific page only (and can we modify the request from Interceptor or history)?

Burp Suite Enterprise Edition is an automated scanner, with no manual testing features. Modifying requests and intercepting traffic are Burp Suite Professional Edition features (our manual penetration testing toolkit).

What type of scan does Burp Suite Enterprise Edition perform?

An automated scan consists of a crawl phase to discover content and an audit phase to discover vulnerabilities. Scan configurations can be used to determine exactly how the scan is carried out. You can use the default configuration, or override this by creating your own custom configurations or selecting from the built-in configurations.

How does the automated scanner in Burp Suite Enterprise Edition handle payloads for its scan checks?

Payloads are submitted automatically by the scanner in the audit phase.

Can we set a scheduler for the execution of a scan?

Yes, this is a key feature in Burp Suite Enterprise Edition.

Are you planning to include support for the detection of unsupported/out-of-date software?

Burp Scanner already performs some checks for vulnerable, outdated dependencies. This includes, for example, vulnerable JavaScript libraries.

Future PortSwigginars

We’re planning on running more PortSwigginars in the future, and we want you to join us! If you’d like to attend, or you have any questions, please contact us.

Adam Armitt

Latest Posts

Burp Extensibility 2026: Awards, Talks, and Highlights

19 June 2026

Burp Extensibility 2026: Awards, Talks, and Highlights

The beast needs a cage: What's next for AppSec post-Mythos

12 May 2026

The beast needs a cage: What's next for AppSec post-Mythos

3 ways custom scan checks turn practitioner knowledge into scalable automation

01 May 2026

3 ways custom scan checks turn practitioner knowledge into scalable automation

Senior pentesters have a deeply refined intuition about what is vulnerable in an environment. The problem? That expertise is often siloed with an individual and trapped in their notes or Python scripts.
