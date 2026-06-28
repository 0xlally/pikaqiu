# Two months of Burp AI: empowering security testers with the future of AppSec

Source: https://portswigger.net/blog/two-months-of-burp-ai-empowering-security-testers-with-the-future-of-appsec
Fetched: 2026-06-28T09:15:26.615017+00:00

Two months of Burp AI: empowering security testers with the future of AppSec

Amelia Coen |

Friday, 13 June 2025 at 13:51 UTC

It’s been a whirlwind two months since AI-powered features landed in Burp Suite Professional. Thousands of security testers across the world have been using Burp AI to find vulnerabilities and secure their applications, and we’ve been blown away by what you have been able to achieve.

From helping us iterate, and providing valuable feedback, to winning bug bounties, the journey so far has been exciting. Here's a look back at what’s happened, and a glimpse at what’s coming next.

Five new features

Back in April, five major capabilities designed to supercharge security testers, and optimize workflows, with AI were introduced. These are…

Explore Issue

Turn Burp AI into your personal pentesting assistant, automating follow-up analysis of scanner-identified vulnerabilities to save time, reduce blind spots, and uncover deeper insights.

Explainer

Confused by an unfamiliar cookie? Unsure what a strange header means? Just highlight it in Repeater and let Burp AI explain it from a security perspective.This feature removes the friction of switching tabs and searching docs. It’s like having a security-savvy co-pilot in your tab bar.

AI-generated recorded logins

No more fiddling around with browser recordings. Burp AI can now generate login sequences on your behalf, reducing configuration time and ensuring better scan coverage - especially for complex authentication flows.

False positive reduction: broken access control

False positives drain time and energy. With Burp AI, we’ve started cutting down on the noise - starting with one of the hardest vulnerability classes to reliably detect through automation: Broken Access Control. Burp Scanner now uses AI to intelligently filter out irrelevant findings, boosting accuracy and freeing you up to focus on real threats.

AI-powered extensibility

The Montoya API and AI extensibility features open up new creative possibilities. Security pros and developers can now use AI to build novel, customized tools right inside Burp Suite.

BApp store bursts with AI innovation

In just a few short weeks, we’ve seen a surge of new AI-powered extensions land in the BApp Store, created by both the PortSwigger team and our growing user community.

Check out AI-enhanced extensions on the BApp store, including:

Shadow Repeater - simply use Burp Repeater as you normally would, and behind the scenes Shadow Repeater will monitor your attacks, try permutations, and report any discoveries via Organizer.

HTTP Analyzer - examines HTTP requests and responses for potential security vulnerabilities such as SQL injection, XSS, CSRF, and other threats.

AI Substitutor - automatically substitute HTTP request parameters and headers with contextually relevant values.

MCP Server - integrate Burp Suite with AI Clients using the Model Context Protocol (MCP).

AI prompt fuzzer - automating prompt fuzzing against AI APIs using customizable payloads, helping identify abnormal or unsafe model behavior.

AI Recon Assistant - extract meaningful insights from requests and responses without manual inspection.

Document My Pentest - create a description of whatever you are trying to test. Whether you're probing for path traversal, SQL injection, XSS, or other vulnerabilities, Document My Pentest tries to understand what you are doing and documents it for you.

Hackvertor - supercharge your workflows by seamlessly converting, encoding, and transforming text or code.

From intelligent request generators to smarter analysis tools, these extensions are a testament to how AI is inspiring creativity and new workflows in web security testing.

Want to learn more about how to create an AI extension? Take a look at PortSwigger Researcher Gareth Heyes' video on what he learned when introducing AI into extensions.

Real feedback, real impact

Thousands of testers have already embraced Burp AI, and their feedback has been invaluable. We’ve heard from penetration testers, bug bounty hunters, and developers all making the most of AI to move faster, dig deeper, and reduce toil.

We caught up with Cristi Vlad to discuss his early experiences with Burp AI and get his take on how AI could be transformative for penetration testing in years to come.

Read more about Cristi’s journey with Burp AI.

Spotlight moments in the community

There’s also been some amazing community moments over the last two months...

Clint Gibler, founder of tl;dr sec, sat down with James Kettle and Dafydd Stuttard for a wide-ranging conversation on how Burp Suite - and now Burp AI - is elevating the art of pentesting. Expect deep dives, big insights, and a glimpse into the vision behind it all.

Watch the video.

John Hammond, renowned content creator and red teamer, took Burp AI’s features for a test drive, showcasing how AI augments traditional testing workflows to help you get more out of your search for vulnerabilities.

Watch the walkthrough.

Katie Warren, Burp AI’s Product Manager, took to the stage at API Days/HAC NYC in May to share our story: Our Journey to AI. This presentation explored how we’re weaving AI into the heart of Burp Suite while staying true to the core principles of effective security testing, and what we’ve learned along the way.

What’s Next?

Over the coming months, expect even more AI-powered capabilities that take on the most frustrating, time-consuming parts of your workflow. We’re continuing to listen, refine, and expand Burp AI based on your needs. More precision. More automation. More innovation.

It’s quick and easy to get started with Burp AI:

Update to the latest version of Burp Suite Professional.

Enjoy 10,000 free AI credits on us.

Not a Burp Suite Pro user yet? Request a free trial.

Don’t forget to share your thoughts on what AI functionality you’d like to see in Burp in the dedicated #burp-ai channel in the PortSwigger Discord. Join the PortSwigger Discord to check it out.

Amelia Coen

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
