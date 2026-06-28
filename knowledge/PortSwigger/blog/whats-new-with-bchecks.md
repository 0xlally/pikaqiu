# What's new with BChecks?

Source: https://portswigger.net/blog/whats-new-with-bchecks
Fetched: 2026-06-28T09:15:28.312397+00:00

What's new with BChecks?

Mike Eaton |

Thursday, 8 February 2024 at 09:05 UTC

Earlier this year, we released BChecks, a powerful yet simple scripting language that allows you to quickly build and create custom scan checks for anything you want to secure or test. We've already had some fantastic submissions to the GitHub repo, and loads of you have been busy creating your BChecks and sharing them with the community.

To help us make BChecks work better for you, we've spoken to Burp Suite users who are already creating custom scan checks. We aimed to discover what changes and developments they'd like to see. Based on their feedback, here's a quick roundup of our latest updates.

Syntax highlighting

Writing a custom scan check should be a painless process, especially as you likely need the scan check to test an application for a specific vulnerability quickly. Wasting time trying to understand a complex new language or struggling with readability issues within the editor is a luxury you can’t afford.

Thanks to the introduction of syntax highlighting for BChecks, you can quickly get to grips with the syntax and create your custom scan check in minutes. No more wasted time trying to understand a new language, struggling to identify sections of code, or misunderstanding the hierarchy of nested structures.

Test your BChecks during development

Not long after the release of BChecks, we quickly received feedback that the feedback loop for developing BChecks was long and awkward. Users typically needed to set up a custom scan configuration and kick off an audit task, only to find that they missed a keyword on line 78 of their BCheck. This was counterproductive and didn’t allow them to unleash their creativity.

To combat this problem, we have released the BChecks testing tool. This tool is directly adjacent to the editor within BS Code. It allows you to run specific requests/responses from other tools against the BCheck currently being worked on in a simulated environment. This instantly allows you to check if your BCheck is behaving as expected in specific scenarios or if you need to make any adjustments to achieve the expected behavior.

Improved management of BChecks

Thanks to our amazing Burp Suite community, we now have a catalog of BChecks available in our official GitHub repository. These custom scan checks have been evaluated and tested to give our users a wide range of options to extend their scanning capabilities quickly and easily. You can find this repository easily using the new clickable GitHub icon in the BChecks tab within Burp Suite.

We wanted to ensure that working with this repository or your custom BChecks is as easy as possible, so two of our talented Swiggers have created a BApp extension that you can install named ‘BCheck Helper.’ This extension allows you to automatically download and install BChecks directly from a configured GitHub repository or local file system.

We are always looking for ways to improve and make BChecks work for you, so if you have any feedback or comments, please contact us on social media or email our support team.

Mike Eaton

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
