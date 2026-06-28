# PortSwigginar - 13 July

Source: https://portswigger.net/blog/portswigginar-13-july
Fetched: 2026-06-28T09:15:23.582274+00:00

PortSwigginar - 13 July

Emma Stocks |

Friday, 15 July 2022 at 11:32 UTC

Burp Suite

Thank you to those who attended our recent PortSwigginar on Burp Suite Enterprise Edition.

Below is the video of the session, which included;

A recap on “what’s new” within the product for those who haven’t checked it out in a while.

How Burp Suite Professional and Burp Suite Enterprise Edition work hand in hand together.

Understanding our licensing model and pricing.

A run-through of our deployment options.

How to quickly set up a site and run a scan.

CI/CD integrations including launching a scan from a Jenkins pipeline.

Sneak peek of our 2022 roadmap!

Watch the July 13 PortSwigginar now.

How can I join the next PortSwigginar?

Didn't get the chance to attend the last one? No worries at all - we have our next PortSwigginar coming up on 10 August at 11am EST. Please use this link to register - we can't wait to see you there!

Finally, we had some fantastic questions from those who attended, so we wanted to share the answers below for the benefit of anyone who missed out.

Questions from our audience

Do you have any information on how Burp Suite Enterprise Edition handles authenticated scans?

Our guides for adding authentication for your sites can be found in our product documentation.

Do you have an integration for Azure DevOps as an issue tracker?

Azure DevOps is not a currently supported integration for issue tracking. We plan on adding more integrations, with GitHub currently in development.

Does Burp Suite Enterprise Edition have an isolated "dark" on-prem enterprise API that integrates with other CI/CD pipeline SecDevOps tools?

Whilst CICD integration is supported with Burp Suite Enterprise, offline activation is not supported. We do have plans to expand CICD functionality in the future so please check back in with us.

If Burp Suite Enterprise Edition does allow for activation in the "dark" - how does the licensing process work in this case?

Offline activation is not supported for Burp Suite Enterprise Edition, a connection to portswigger.net via port 443 is required for license activation. You can review our network and firewall requirements here.

Can Kubernetes be deployed in AWS Fargate?

Yes, AWS Fargate is supported.

Is there a possibility to scan without crawling (upload application structure)?

Web application authentication can be added for the Burp Enterprise Scanner. Multi-factor authentication is not possible for an automated scanner. You can find more information on configuring login details for sites here.

The burp web server uses http protocol, does the new version use https?

You can configure the Burp Suite Enterprise Edition web server to your preference, including https and uploading a TLS certificate. You can find more information on configuring your web server here.

Do we have to install a burp agent on our servers or will we have to run our application against the burp enterprise server proxy? Can you please explain how it captures the URLs to scan?

You don't need to install an agent on your servers. You will give the scanner a URL to crawl and audit when setting up the site in Burp Suite Enterprise Edition.

Is it possible to export a scan from Professional to Enterprise?

There is currently no integration between Burp Suite Professional and Burp Suite Enterprise Edition. They are two different products that compliment each other, one for manual scanning and the latter for automated.

Is it planned in the future to add the possibility to add a justification (for example with a text input field) when we mark a finding as a false positive?

This feature is in our development backlog, we don't have a current ETA on the release date but please feel free to check back in with us.

Burp Suite

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
