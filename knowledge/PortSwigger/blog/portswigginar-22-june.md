# PortSwigginar - 22 June

Source: https://portswigger.net/blog/portswigginar-22-june
Fetched: 2026-06-28T09:15:23.576523+00:00

PortSwigginar - 22 June

Emma Stocks |

Monday, 27 June 2022 at 14:44 UTC

Thank you to those who attended our recent PortSwigginar on Burp Suite Enterprise Edition.

Below is the video of the session, which included:

A recap on "what's new" within the product for those who haven't checked it out in a while.

How Burp Suite Professional and Burp Suite Enterprise Edition work hand in hand together.

Understanding our licensing model and pricing.

A run-through of our deployment options.

How to quickly set up a site and run a scan.

CI/CD integrations including launching a scan from a Jenkins pipeline.

Sneak peek of our 2022 roadmap!

Check out the video here: "What's new in Burp Suite Enterprise Edition?"

How can I join the next PortSwigginar?

Didn't get the chance to attend the last one? No worries at all - we have our next PortSwigginar coming up on 13 July at 11am EST. Please use this link to register - we can't wait to see you there!

Finally, we had some fantastic questions from those who attended, so we wanted to share the answers below for the benefit of anyone who missed out.

Questions from our audience

Do you have any information on how Burp Suite Enterprise Edition handles authenticated scans?

Adding authentication for your sites is detailed here.

Do you have an integration for Azure Devops as an issue tracker?

Azure DevOps is not a currently supported integration for issue tracking. We plan on adding more integrations, with GitHub currently in development.

Does Burp Suite Enterprise Edition have an isolated "dark" on-prem enterprise API that integrates with other CI/CD pipeline SecDevOps tools?

Whilst CICD integration is supported with Burp Suite Enterprise, offline activation is not supported. We do have plans to expand CICD functionality in the future so please check back in with us.

If Burp Suite Enterprise Edition does allow for activation in the "dark" - how does the licensing process work in this case?

Offline activation is not supported for Burp Suite Enterprise Edition, a connection to portswigger.net via port 443 is required for licence activation. You can review our network and firewall requirements here.

Can Kubernetes be deployed in AWS Fargate?

Yes, AWS Fargate is supported.

Does Burp Suite Enterprise Edition provide tests and features specifically for serverless functions, similar to AWS Lambda, Microsoft Azure functions, or Google Cloud functions?

There are no tests & features specifically for serverless functions, however you may be able to create a custom extension to meet your needs.

Do you provide sample infrastructure as code (e.g. terraform or cloudformation) to ease the deployment?

Our reference architecture template uses CloudFormation and can be found on our public GitHub. The link can be found in our Kubernetes documentation here. We may provide examples for other platforms in the future.

How is Burp Suite Enterprise Edition licensed?

Burp Suite Enterprise Edition is licensed on concurrent scans. We don't limit you on the number of applications, domains, URLs, users, or anything else - only scan concurrency. Unlike most automated web vulnerability scanners, Burp Suite Enterprise Edition scans can be assigned and re-assigned across any websites, applications, or URLs.

Does Burp Suite Enterprise Edition have Okta support for RBAC?

We support SSO integration (SAML & LDAP) which works with Okta. User permissions are managed on the identity provider side in this case. We do also support a SCIM integration that can be used with the SSO integration to manage user permissions in Burp Suite Enterprise.

Are there plans for a fully hosted SaaS/PaaS solution?

There are no immediate plans but it's under consideration. Currently the solution is deployed in your own infrastructure.

Does Burp Suite Enterprise Edition have the ability to record a walkthrough of an application (ie. like a HAR file) to record the page sequence and specific test data that may be needed to successfully test the entire app? Similar to the recorded login, but for the entire app?

The automated scanner currently handles the crawl and mapping of the target automatically. We are looking to add functionality such as a Selenium or Puppeteer driven crawl in the future. This would allow a specific path through the app to be set or to navigate and complete more complex multi-step forms with set steps.

Is there an ability to use multiple credential profiles?

Yes, multiple sets of application login credentials can be set for a scan.

Is there support for programmatic authentication for APIs/non-UI apps such as Auth0, PingIdentity, etc?

Our automated API scanning feature does not currently handle API level authentication that is separate to the web application. However, we do have a feature to add a custom http header, if a static authorization token can be set in advance. This has URL matching to set when the header is applied.

Is there support for skipping crawling altogether and just using something like API documentation (Postman, OpenAPI, Insomnia, etc.) or from a pre-made Burp Pro site map?

Not currently. The automated scanner performs the crawl and mapping of the target automatically. We are looking to add functionality in future to allow a Selenium or Puppeteer driven crawl.

Are there any plans for Burp Suite Enterprise Edition to be able to import scan reports from Burp Professional?

There are no plans to import scan reports at this time.

Do you have an integration with Atlassian Bamboo as a CI/CD platform?

We have a generic driver that would allow integration with that platform. In our roadmap we are also looking at a containerized CICD integration to avoid having to use a native driver per platform.

Is there any integration with CyberArk for scan creds?

We are not familiar with CyberArk specifically, but we have a recorded login sequence feature that can handle more complex application authentication, such as SSO.

Does the scan do a content discovery similar to burp pro when looking for content / pages?

Yes, the automated scanner in Burp Suite Enterprise Edition is the same as in Burp Professional - it performs content discovery automatically.

Can Burp Suite Enterprise Edition user accounts be configured as SSO / 2FA and can you apply Role Based Access Control (i.e. view results but not configure scans?

Yes, SSO and RBAC are supported.

Emma Stocks

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
