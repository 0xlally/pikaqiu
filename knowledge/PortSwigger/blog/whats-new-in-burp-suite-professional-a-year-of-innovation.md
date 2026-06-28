# What's new in Burp Suite Professional: A year of innovation

Source: https://portswigger.net/blog/whats-new-in-burp-suite-professional-a-year-of-innovation
Fetched: 2026-06-28T09:15:28.316447+00:00

What's new in Burp Suite Professional: A year of innovation

Eleanor Clarke |

Wednesday, 14 May 2025 at 08:26 UTC

Over the past year, we’ve been hard at work making Burp Suite Professional faster, smarter, and more powerful than ever before. From the launch of Burp AI to major performance upgrades, there's never been a better time to use Burp.

Here’s a roundup of some of the biggest updates we’ve introduced this year to supercharge your testing workflow. To make the most of these improvements, make sure you're running the latest version of Burp Suite Professional. To update, go to the top Help menu in Burp and click Check for updates.

Performance wins

We've delivered some major performance boosts to help Burp stay fast and responsive, even under a heavy load:

Site map and table filtering is significantly quicker.

Scans now complete more quickly with reduced resource usage.

Large responses now display much faster and use less memory.

Browser load times are faster as we now reuse HTTP/1

connections for outbound requests from the proxy.

Project files with large numbers of Repeater tabs no longer cause Burp's interface to lag.

Intruder attacks now run more efficiently - by configuring a capture filter, you can avoid capturing unnecessary responses and reduce overhead.

These improvements are already making a difference to our users:

I was surprised when a very large table sorted in one second. If that’s due to the new performance stuff, I’m really happy about it! Nice stuff!

- t0xodile, Burp Suite user.

Keep the performance upgrades coming, they're LIT 🔥

- M0PAM, Burp Suite user.

We hope these changes have made a big difference to your everyday use of Burp. If you're still experiencing any performance issues, we'd love to hear from you. Please email us at support@portswigger.net.

Build your own Burp features

This year, Bambdas have become one of the most flexible and powerful tools in your testing toolkit. Bambdas are custom scripts that you can write and run directly in Burp, enabling you to automate repetitive tasks, tailor Burp to your workflow, and unlock new ways of working. You can now use these to:

Extract and analyze data in Burp Repeater with custom actions.

Create advanced match and replace rules to manipulate HTTP traffic.

Add custom table columns to surface the data you care about.

Dynamically filter the site map to cut through the noise.

To support your use of Bambdas, we've also added:

A dedicated output console for debugging scripts.

A Bambda library so you can organize, reuse, and share your favorite scripts with ease.

If you get hooked on Bambdas, why not take things further by building your own extensions? You can now kickstart development with our ready-to-use starter project.

Plus, we've expanded the Montoya API with powerful new capabilities for writing extensions and Bambdas. For example, you can now parse, add, delete, and update JSON parameters, and register custom hotkeys.

A more intuitive user interface

We've refreshed several key areas of Burp to help you work more efficiently:

Burp Intruder now has a cleaner, more intuitive side panel layout, allowing you to configure attacks without switching between tabs.

Proxy Intercept lets you manage messages more easily. You can now view an ordered queue of intercepted messages, manage messages in bulk, and manage messages in any order you like.

Site map navigation is clearer than ever, with alphabetically sorted content, new and refreshed icons, and the ability to toggle between the URL view and the Crawl paths view.

You can now hide HTTP headers that you aren't interested in from the Pretty tab of the message editor.

Improvements to complement our cutting edge research

We continue to feed our cutting-edge research straight into Burp, helping you to stay ahead of emerging vulnerabilities:

We've increased the accuracy of Burp's single-packet attack, improving Burp's ability to detect race condition vulnerabilities with small race windows. This update is based on James Kettle's research into web timing attacks.

We've added an email splitting payload list to Burp Intruder, enabling easier detection of email parsing discrepancies. The payloads are inspired by Gareth Heyes' research into email domain confusion.

We've added new scan checks for web cache deception vulnerabilities, thanks to Martin Doyhenard's work on exploiting web cache behavior.

Gareth Heyes has also developed powerful new AI extensions. Document My Pentest automatically documents your workflow, while Shadow Repeater generates and tests AI-powered payload variants to explore new code paths.

Smarter, faster scanning

We've made several major improvements to Burp Scanner to boost both speed and depth of coverage:

Burp can now handle token renewal automatically during scans.

You can launch dedicated API-only scans, with support for OpenAPI v2.0 and v3.0 (with partial support for v3.1.x), SOAP WSDLs, and Postman collections.

You can edit manually recorded logins without needing to edit raw JSON, and you can use AI to generate recorded login sequences.

Countless small improvements

We've also added dozens of one-off upgrades across Burp, which all add up to a faster, smoother, and more enjoyable experience. You can now:

Test your match and replace rules with the built-in test function.

Manually create issues for inclusion in your final report.

Configure WebSocket match and replace rules.

Set up multiple platform authentication credentials for each destination host, so you can more quickly enable and disable platform authentication for different users.

Automatically pause Intruder attacks based on response criteria.

Decode Base64

and Q-encoded data in SMTP messages automatically. This is particularly useful when testing for email splitting or HTTP Host header vulnerabilities.

Save your Collaborator settings once for use across all your Burp installations. They're now saved as user settings, instead of project settings.

These are just the highlights - there are plenty more improvements that we just didn't have the space to list here!

Saving the best for last: Introducing Burp AI

Unless you've been living under a rock, you've probably heard about Burp AI - our new suite of AI-powered features designed to give you deeper insight into vulnerabilities, cut through noise, and enhance your testing workflow.

We won't go into detail here, but if you'd like to learn more you can read the full Burp AI announcement.

Thanks for testing with us - stay tuned for more

We hope our upgrades have made your testing faster, easier, and more enjoyable! Don't forget to let us know how you're getting on by joining the PortSwigger Discord, or tagging us on X or LinkedIn. We're @Burp_Suite on X and @PortSwigger on LinkedIn.

And as always, thank you for being part of the Burp Suite community. Stay tuned - there's lots more to come.

Eleanor Clarke

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
