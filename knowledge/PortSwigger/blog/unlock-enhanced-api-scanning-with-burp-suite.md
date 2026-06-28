# Unlock enhanced API scanning with Burp Suite

Source: https://portswigger.net/blog/unlock-enhanced-api-scanning-with-burp-suite
Fetched: 2026-06-28T09:15:26.682911+00:00

Unlock enhanced API scanning with Burp Suite

Rob Samuels |

Wednesday, 31 July 2024 at 12:17 UTC

More comprehensive scans. More vulnerabilities identified. More time saved. Enhance your API scanning with Burp Suite.

As web portfolios have diversified, APIs have become an increasingly critical function of modern web applications. According to ESG’s Securing the API Attack Surface report, the vast majority of organizations report they now have an average of 26 APIs per application.

Despite this, scanning APIs for vulnerabilities is often challenging, with many organizations reliant on workarounds. At best this solution is fiddly and time-consuming, and, at worst, leaves your application open to attacks, and affects your ability to scale testing.

APIs are the biggest gap in our testing at the moment. We’ve done a small amount of scanning, but having a Burp API scan would be amazing. A Burp Suite Enterprise Edition customer

We’ve been working to remedy this challenge by enhancing our existing API scanning capability with enhanced built-in functionality designed for easy, scalable API scanning.

Our improved API scanning functionality allows users to:

Test for vulnerabilities without having to host definition files

Easily identify any hosted APIs that have been left accessible to attackers

Test a wider range of OpenAPI Specification (OAS) endpoints

Scan APIs that require endpoint authentication

These features are now available for both Burp Suite Enterprise Edition and Burp Suite Professional users.

How were APIs scanned in Burp previously?

Users of Burp Suite have been able to scan APIs for some time. However, up to now, API endpoints have been scanned as part of a wider web application crawl & audit.

This approach, however, raises a few challenges.

Firstly, for pentesters, this approach means you can’t target APIs specifically in your scans. As your portfolio of APIs increases, this task has gone from a quality-of-life issue to a major obstacle for effective workflows.

For AppSec teams, scanning APIs as part of your wider web apps means you have to run a more thorough and time-consuming scan, reducing the ability to scale operations.

As we look at modernizing web applications and moving towards everything as an API, all of the data is accessible behind that API. We're trying to step up our game in terms of proactive discovery of API-level vulnerabilities. A Burp Suite Enterprise Edition customer

Scanning APIs exclusively in this way is no longer fit for purpose. We needed a built-in solution to API scanning.

Meet our improved API scanning features

We’ve released 4 API scanning features, allowing Burp users to scan their APIs alongside their web apps, and as a standalone too. These can be accessed in both Burp Suite Professional and Burp Suite Enterprise Edition:

1. Test for vulnerabilities without having to host definition files

You can now upload OAS definition files directly to Burp Suite. This update enables users to choose whether they want to provide an existing URL, or upload a file directly to Burp. That means quicker, hassle-free scanning, which can be easily scaled.

Read more about testing for vulnerabilities in Burp Suite Enterprise Edition.

Read more about testing for vulnerabilities in Burp Suite Professional.

2. Easily identify any hosted APIs that have been left accessible to attackers

Burp now checks whether you have left any hosted OAS definitions that may be accessed by attackers. This helps flag any potential security threats - particularly while you transition away from having to scan APIs via hosting them yourself.

3. Test a wider range of OpenAPI Specification (OAS) endpoints

When crawling your APIs, you can now include HTTP headers, allowing you to scan a much wider range of OAS endpoints. More comprehensive scans. More vulnerabilities identified.

Read more about testing OAS endpoints.

4. Scan APIs that require endpoint authentication

Finally, for Burp Suite Enterprise Edition users, you can now scan APIs that require authentication. Previously, crawlers were denied entry to authenticated endpoints, but this update allows the scanner to bypass some authentication points without having to pause scans.

Read more about endpoint authentication.

See these features in action. Watch a demo of API scanning in Burp Suite Enterprise Edition .

What’s next for API scanning in Burp Suite?

Users of Burp Suite Professional and Burp Suite Enterprise Edition now have access to all four of the features above.

We’re also planning the following key updates which will form the next release of the API scanning functionality:

Burp Suite Enterprise Edition

Endpoint configuration

When uploading an API definition, Burp Suite will soon be able to parse the file and display the endpoints for you. You’ll then be able to search endpoints, and uncheck the ones you don’t want to include in the scan.

This will help with excluding destructive endpoints, and provide the capability to bulk include and exclude specific methods - for example post or delete.

Bulk upload of API definition files

Following endpoint configuration, the next update will allow users to bulk import API targets via URL or definition file upload. This update will reduce the load of importing one API at a time, unlocking significant time savings - particularly when onboarding APIs.

Want to learn about API scanning in Burp Suite Enterprise Edition? Request your free, fully-featured trial here.

Coming soon to Burp Suite Enterprise Edition and Professional

Scanning of SOAP APIs supported

This first release enables the scanning of open APIs only, however, we will be supporting SOAP in Burp Suite in one of our next releases. This will enable customers using SOAP to perform the API scanning capabilities above.

These aren’t the only updates planned - we’ll be extending the functionality of the API scanner with each future release. To stay up to date with the latest feature drops, follow @burp_suite on X.

What do you want to see in the API scanner?

We want to hear from you about the features that work, the features that don’t, and any other features you'd like to see in the future.

Make yourself heard. Join our API product research survey here, or email us with your feedback and suggestions here.

Next steps

Ready to enhance your API security with Burp Suite Enterprise Edition? Request your free, fully-featured trial here.

Rob Samuels

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
