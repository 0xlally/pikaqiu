# How to detect React2Shell with Burp Suite

Source: https://portswigger.net/blog/how-to-detect-react2shell-with-burp-suite
Fetched: 2026-06-28T09:15:16.260763+00:00

How to detect React2Shell with Burp Suite

Tom Ryder |

Friday, 5 December 2025 at 13:53 UTC

Detecting React2Shell with Burp Suite

Two new critical vulnerabilities, collectively known as React2Shell (CVE-2025-55182 and CVE-2025-66478), are rapidly gaining traction in the security community.

Default scans in both versions of Burp Suite can now detect React2Shell in Next.js-based applications out of the box, with the option to include these checks in custom scan configurations as well. No extensions, no custom scan checks, and no scripts required, simply update and scan.

Burp Suite Professional – for manual investigation and validation

Burp Suite DAST – for continuous, automated coverage across many apps

This update to scan checks helps organizations and practitioners to quickly investigate and triage suspected Next.js (React server components) targets.

Please note, that if you have custom scans already configured, you may need to check the settings and add React2Shell scanning to the configuration.

Join the React2Shell conversation

We would love to hear from you. Jump into the PortSwigger Discord to share feedback, tips, and requests with the team and the community.

Join the PortSwigger Discord.

What is React2Shell?

Two new critical vulnerabilities, collectively known as React2Shell (CVE-2025-55182 and CVE-2025-66478), are rapidly gaining traction in the security community. With a CVSS score of 10.0 and unauthenticated remote code execution, many expect a trajectory similar to Log4j, including rapid weaponisation by ransomware groups.

React2Shell affects React and Next.js applications and potentially other frameworks that use React server components.

Because these frameworks underpin a huge number of production apps, a successful exploit can lead to major compromise. For most teams, this should be treated as a high-priority incident.

Early proof-of-concept checks have mostly focused on detecting the presence of React server components. That is not enough to determine exploitability, and not all public PoCs are reliable.

Important: Even if your application does not explicitly call server actions, it may still be vulnerable, as long as it supports React server components.

PortSwigger's Immediate Response to React2Shell

On December 5, 2025, PortSwigger’s team reacted quickly to the React2Shell vulnerability, releasing two quick updates to help organizations and practitioners to quickly investigate and triage suspected Next.js, (React server components) targets.

How to test for React2Shell in Burp Suite Professional

Manual testing, instant visibility

Burp Suite Professional lets you quickly investigate React2Shell behaviour and validate specific endpoints during hands-on testing. You have two main detection options:

ActiveScan++ (v2.0.8) – recommended

Ensure you have the latest version of ActiveScan++, which includes a dedicated React2Shell check, giving you automated detection directly inside Burp Suite Professional. Once installed, it:

Adds React2Shell coverage into your existing manual workflow

Runs automatically as part of your active scanning

Is ideal for quick investigation and triage of suspected Next.js (React server components) targets

Note: Current automated checks focus on Next.js applications. Other React frameworks may still require manual investigation and bespoke testing.

Custom scan check (Bambda) for targeted checks

If you need more focused, on-demand testing, you can import the community-created React2Shell Bambda and run it against specific endpoints or applications.

This is ideal for quickly validating a suspected vulnerable app or probing specific components to reproduce reported behaviour.

How to import and run the custom scan check:

Download the Bambda

In Burp Suite Professional, go to Extensions > Bambda library.

Click Import. The Import scripts dialog opens.

Select .bambda files or a folder containing .bambda files.

Click Open.

How to scan for React2Shell in Burp Suite DAST

If you need to understand React2Shell exposure across many applications or environments, Burp Suite DAST gives you continuous, automated detection at scale.

ActiveScan++ (v2.0.8) in Burp Suite DAST

Burp Suite DAST supports the updated ActiveScan++ extension. Once installed, ActiveScan++ enables automated React2Shell coverage across your Next.js estate, with scans running on a schedule or through your CI/CD pipelines, and results delivered centrally to your AppSec team.

How to enable ActiveScan++ in Burp Suite DAST

Download the ActiveScan++ BApp here:

ActiveScan++ extension

For a full breakdown of how to install BApps in Burp Suite DAST, go to the user guide.

Tom Ryder

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
