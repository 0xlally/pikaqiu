# How this seasoned bug bounty hunter combines Burp Suite and HackerOne to uncover high-impact vulnerabilities

Source: https://portswigger.net/blog/how-this-seasoned-bug-bounty-hunter-combines-burp-suite-and-hackerone-to-uncover-high-impact-vulnerabilities
Fetched: 2026-06-28T09:15:16.394766+00:00

How this seasoned bug bounty hunter combines Burp Suite and HackerOne to uncover high-impact vulnerabilities

Amelia Coen |

Friday, 12 September 2025 at 12:21 UTC

Arman S. (Tess), a full-time independent security researcher and bug bounty hunter, talked us through how he uses Burp Suite Professional and HackerOne in tandem to find and report high-value security vulnerabilities, and how this has secured him thousands of dollars in bounties.

What is Burp Suite? And what is HackerOne?

Burp Suite Professional is a leading web vulnerability scanner and proxy tool developed by PortSwigger, used by security professionals to intercept, manipulate, and analyze HTTP requests in real time. Its extensibility and powerful features make it indispensable for web application testing.

HackerOne is a premier bug bounty platform that connects ethical hackers with organizations to report security issues in return for monetary rewards. It offers structured programs, scope definitions, and mediation services.

Together, these tools empower security researchers to work efficiently and responsibly.

Getting started as a hacker

Getting started in the industry, Tess began hacking at age 16 by experimenting with Wi-Fi networks and phishing for fun. After discovering bug bounties on Twitter, he shifted to ethical hacking and quickly realized its professional potential.

I started doing bug bounties full-time in college, dropped out, and never looked back. I was making good money, learning fast, and loving it.

Why Burp Suite is integral to every hunt

Let me be honest with you, if a hacker tells you he's not using Burp Suite, then he's not a hacker. It's like a microscope for web applications.

When participating in HackerOne programs, Burp Suite becomes essential:

Tess starts by downloading the Burp project file provided in the program’s scope on HackerOne.

He proxies all his traffic through Burp Suite, using it to intercept requests, explore endpoints, and uncover hidden behaviors in the application.

With Burp Extensions like JS Miner and the HTTP Request Smuggler, he’s able to automate and extend his testing capabilities.

You wouldn’t believe the time Burp saved me by catching backend requests the browser never shows. That’s how you find the real bugs.

HackerOne provides the platform for Tess to focus on impactful, in-scope targets. It also simplifies communication and triage:

Everything is so systematic: find the bug, report it, and if needed, open mediation. Without HackerOne, I don’t think the bug bounty ecosystem would function as well.

With this combination, Tess has seen big wins and real results. One of Tess’ most notable wins, a $38,000 bug bounty, was uncovered using Burp’s HTTP Request Smuggler extension:

I was testing an API on Zoom’s bug bounty program and Burp flagged possible smuggling. That lead turned into a $38K bounty.

Why this combination works

Burp Suite gives hackers granular control, automation, and observability.

HackerOne streamlines the process from discovery to reward.

Burp’s project files provide reproducibility and evidence when submitting reports.

Sometimes I send the Burp project file directly to the triage team. It proves the bug existed at a specific time.

Tess credits much of his success to the Web Security Academy, James Kettle’s research, and the wider community.

Solving labs helped me understand attacks deeply. When I see something in the wild, I go, 'Oh, I saw that on PortSwigger.

He also appreciates the responsiveness of PortSwigger’s support and the utility of the Discord community.

Advice for new hackers

Start with PortSwigger Labs and HackerOne CTFs. Pick one type of vulnerability, like XSS, and go deep. Learn the tools, practice the labs, and follow the research.

For Tess, Burp Suite and HackerOne aren’t optional, they’re foundational.

Burp Suite runs in the background even when I’m not actively using it. It’s my evidence, my toolkit, my safety net.

Bug bounty hunting is more accessible and effective when powered by tools that complement each other. Burp Suite Professional and HackerOne form a powerful duo for any ethical hacker looking to make an impact, build skills, and earn significant rewards.

Get rewarded for hacking

HackerOne have launched the Hacker Milestone Rewards Program, a fresh, achievement-based system designed to reward researchers for valid vulnerabilities.

This program replaces HackerOne's former reputation-only model and brings a more inclusive, results-driven approach to recognizing researcher contributions. We’re proud to partner with HackerOne in bringing this program to life, with hackers now having the opportunity to be rewarded free Burp Suite Professional license.

Learn more about the Hacker Milestone Rewards Program.

Ready to get started?

Learn more about HackerOne, or join the conversation with other bug hunters over on the PortSwigger Discord.

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
