# Introducing custom scan checks to Burp Suite Enterprise Edition

Source: https://portswigger.net/blog/introducing-custom-scan-checks-to-burp-suite-enterprise-edition
Fetched: 2026-06-28T09:15:18.687231+00:00

Introducing custom scan checks to Burp Suite Enterprise Edition

Emma Stocks |

Friday, 2 February 2024 at 11:26 UTC

BChecks, in a nutshell, are easy to use custom-created scan checks that enable you to extend the capabilities of Burp Scanner in a quick and simple way. We recently released BChecks to Burp Suite Professional and, following fantastic feedback from the user community, we've now made this feature available to our Burp Suite Enterprise Edition users as well.

How can my organization benefit from BChecks?

The advantage of using BChecks to support automated, scheduled scanning within your organization is the amount of time it takes. Or rather, how little time it takes. Unlike creating a built-in scan check where you're dependent on waiting for it to be added natively to Burp Suite, you can import a BCheck and start scanning for the specific vulnerability straight away.

Being able to customize Burp Scanner so that it's fine-tuned to look for the vulnerabilities that are impacting your organization's apps most means that you can work in a more agile manner. Simply import a specific custom scan check from the GitHub repo, or write your own custom BCheck in Burp Suite Professional, then start scanning immediately.

Looking to apply a scan check to test your applications for a severe zero-day vulnerability? There's a BCheck for that. Want to check for less critically impactful bugs earlier in your pipelines? There's a BCheck available to import. If your teams already use Burp Suite Professional alongside Burp Suite Enterprise Edition, you can even write your own custom BChecks that are tailored specifically to your own applications and the vulnerabilities you're interested in scanning for.

What BChecks are available?

The BChecks GitHub repository already contains a wide variety of custom scan checks, created by both PortSwigger developers and the Burp Suite user community. Some highlights include:

Blind SSRF via out-of-band detection.

Exposed git directory.

Leaked AWS tokens.

Log4Shell via out-of-band detection.

Server-side prototype pollution.

Suspicious input transformation.

When we initially launched the feature, we shortlisted the top ten BChecks submitted by the amazing Burp Suite user community - you can view those BChecks in this blog post.

Made a BCheck in Burp Suite Professional you think the user community would benefit from? Submit it to the official BChecks repo here - you can also discover the range of BChecks available.

Adding BChecks to Burp Suite Enterprise Edition

BChecks are available, and ready to use in Burp Suite Enterprise Edition right now. To get started, simply follow the steps below:

Log in to Burp Suite Enterprise Edition as a user with permission to manage extensions.

From the settings menu, select Extensions to go to the Extension library.

On the BChecks tab, click Upload BCheck.

Select the BCheck you want to upload.

For further information and guidance, please refer to the BChecks in Burp Suite Enterprise Edition documentation.

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
