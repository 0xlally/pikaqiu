# Enterprise Edition: CI integration

Source: https://portswigger.net/blog/enterprise-edition-ci-integration
Fetched: 2026-06-28T09:15:14.375684+00:00

Enterprise Edition: CI integration

Dafydd Stuttard |

Thursday, 30 August 2018 at 15:41 UTC

MoBP

Burp Suite

Enterprise Edition

CI integration

Jenkins

teamcity

Burp Suite Enterprise Edition has full support for integration with CI/CD systems.

There is a REST API that can be used to initiate scans and obtain the results:

There is a native Burp CI plugin for Jenkins:

And for TeamCity:

There is also a generic Burp CI driver that provides a command-line interface for use by any CI platform for which a native plugin is not available:

Using the CI integration, you can configure builds in your CI system to drive scans per commit or on a schedule, and fail software builds when certain issues are reported. This involves making your build deploy the application that is to be scanned to a suitable test server. This might be a static server that is used for this purpose, or a more dynamic deployment such as a Docker container. The build should output the URLs to be scanned within its build log, and then invoke the Burp CI integration. Optionally, you can also configure per-build the minimum severity or confidence for a discovered issue to break the build.

Note that Burp Suite Professional does not have a suitable design or architecture for use in CI integration, and is not licensed for this purpose. Users wishing to use Burp Suite to perform scanning within their CI builds should use Burp Suite Enterprise Edition.

MoBP

Burp Suite

Enterprise Edition

CI integration

Jenkins

teamcity

Dafydd Stuttard

@DafyddStuttard

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
