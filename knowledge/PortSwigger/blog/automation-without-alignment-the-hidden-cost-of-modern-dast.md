# Automation without alignment: The hidden cost of modern DAST

Source: https://portswigger.net/blog/automation-without-alignment-the-hidden-cost-of-modern-dast
Fetched: 2026-06-28T09:15:06.983913+00:00

Automation without alignment: The hidden cost of modern DAST

Dafydd Stuttard |

Thursday, 12 March 2026 at 12:02 UTC

Watch the webinar recording: Burp Suite DAST x Burp Suite Professional: Better Together

I'm a firm believer that if you want to understand how secure an application really is, you have to test how it behaves, not just how it was written. Automation has become essential to that. No AppSec team can test at the velocity and scale demanded by modern release cycles through manual means alone. As a result, dynamic scanning (DAST) tools are now embedded into the daily rhythm of mature security teams everywhere, often bundled as part of an all-in-one AST platform.

On paper, this looks like a well-rounded approach: Manual testing for depth, automated scanning for scale. And yet, AppSec leaders feel that they're scanning more than ever, but getting increasingly diminishing returns on that investment.

The way most organizations combine DAST automation with manual pentesting rarely works as well as it should. Not because the team lacks skill. Not because the processes are poorly designed. But because the tools were developed in isolation from each other.

I've made no secret of the fact that the first version of Burp Suite was built for one user: me. I was a web app pentester and just built the tool I wished I had, enabling me to scale myself exponentially. That practitioner-driven background shapes how we think at PortSwigger even to this day.

I believe that to unlock the full value of DAST, it's crucial to remember that it's an extension of what started as manual pentesting and still relies heavily on humans in the loop. DAST is inherently part of modern practitioner workflows and should be treated as such, rather than grounding it in a parallel ecosystem of broad-brush automation tools.

The translation tax

Regardless of which automated solutions you implement, some level of manual intervention is always necessary. Automated systems lack judgment. They surface potential issues, but it takes human expertise to determine what actually matters. That's still true despite the staggering advances we've all seen in AI over recent years.

But there's friction most teams don't fully account for. Burp Suite Professional has been the practitioner's tool of choice for web security testing for decades. Whichever DAST solution a team is running, the findings are almost certainly being validated and investigated using Burp Suite.

Think through what that process actually looks like from a practitioner's perspective. The findings arrive in a format that belongs to a different tool, built on a different scanning engine, with its own issue taxonomy, its own evidence model, its own confidence signals. Before your pentesters can even begin to validate anything, they first have to translate it. They have to map the scanner's output to their own mental model and reproduce it in Burp Suite; the tool they actually work in.

This is invisible overhead. It happens for every finding and every scan cycle, across every application in your portfolio. What starts as mild friction compounds, at scale, into a significant drain on your team's time and attention.

Instead of automation freeing up your pentesters to better prioritize and focus on the highest impact activities, their role is reduced to slowly working their way through a seemingly endless backlog of issues. Rather than extending your team's capacity, automation ends up consuming it.

Expertise that's left on the table

Over years of using Burp Suite Professional, good security teams build up a remarkable amount of institutional knowledge: Custom scan configurations finely tuned to specific tech stacks, innovative extensions that encode expert methodologies and powerful automation, and test cases developed from real findings, refined over time into repeatable checks. This isn't just tooling; it's the codified expertise of skilled practitioners, accumulated over thousands of hours of applying their craft.

None of that is accessible to the DAST component of your AST platform. Because it's built on a fundamentally different engine, with its own scanning logic, its own configuration model, its own extension framework, it has no way to draw on what your team has built up in Burp. That expertise exists. It shapes every manual test your team runs. But it simply cannot cross into a tool built around an entirely different foundation.

Consider what this means. You've invested in a highly skilled team. They've invested in deeply understanding your applications. But when your DAST scanner runs, it operates entirely in isolation. By far your most valuable security asset, practitioner expertise, simply isn't accessible to a scanner that was never built to work with it.

The root of both problems

These are separate issues, but they share a common origin.

Most DAST scanning capability was built to sit inside broader platforms, designed for enterprise procurement, built to scan and send statistics to a dashboard. Integrating naturally with how security professionals actually work wasn't a core consideration.

That origin explains both problems. It's why findings arrive in a format that needs translating rather than one that maps to how a pentester thinks. And it's why there's no pathway for practitioner-built knowledge to inform automated scanning.

What happens when DAST starts with pentesting?

When we built Burp Suite DAST, we started with a fundamentally different question: what would it mean for automated DAST to be genuinely grounded in how practitioners work, rather than running alongside them?

That question changes the answer to almost everything.

It changes how findings are generated and presented, so they arrive in a form that's immediately familiar and actionable. It changes the relationship between manual expertise and automation, so your testers' knowledge is deployed at scale. Ultimately, it changes the way we see automation in application security — from two parallel streams to a bi-directional relationship where automation and manual testing reinforce each other.

The most capable security teams aren't defined by how many tools they run. They're defined by how far their expertise can reach. When automation genuinely extends that reach, rather than consuming the capacity that makes it possible, the whole program changes. Your best people stop being triage machines and start being force multipliers, with their knowledge actively shaping what runs across your entire portfolio, at scale, every scan cycle.

Everyone else started with automation. We started with how practitioners actually work.

We'll be exploring exactly what it looks like in practice in our upcoming webinar. Join us and see what your security program looks like when expertise and automation finally pull in the same direction.

Watch the webinar

You can access a recording of the webinar using the following link: Burp Suite DAST x Burp Suite Professional: Better Together

About the author

Dafydd Stuttard is the Chief Swig of PortSwigger and the creator of Burp Suite, the industry's go-to toolkit for web app and API security testing. A former pentester himself, he is also the author of the Web Application Hacker's Handbook and created its interactive, online successor, the Web Security Academy. Both continue to serve as invaluable resources for aspiring bug bounty hunters and experienced pentesters alike.

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
