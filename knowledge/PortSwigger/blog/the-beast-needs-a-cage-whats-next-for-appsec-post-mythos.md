# The beast needs a cage: What's next for AppSec post-Mythos

Source: https://portswigger.net/blog/the-beast-needs-a-cage-whats-next-for-appsec-post-mythos
Fetched: 2026-06-28T09:15:25.364105+00:00

The beast needs a cage: What's next for AppSec post-Mythos

Dafydd Stuttard |

Tuesday, 12 May 2026 at 14:18 UTC

Now that the dust has settled on Mythos dropping, there is space for more considered reflection on the direction of travel.

Mythos wasn't a surprise; it's another data point on a trajectory that's been clear for some time. Frontier lab capabilities are moving at pace, with major implications for all domains, not least cybersecurity.

Open-weight models are following the same trajectory, with a modest lag. It's fairly likely that they'll match today's frontier capabilities within a few months. Anyone with suitable compute power will have access to Mythos-like capabilities. This was a key topic of discussion when James Kettle and I recently appeared on the Risky Business podcast.

In this post, I'll set out where I think this leaves us: the structural limits that still matter, what changes for the security practitioner, and how we're approaching all of this in the next generation of Burp Suite.

The interesting question isn't what AI can do. It's what it can't

For AppSec, it's likely that the whole traditional value chain of finding vulnerabilities, proving they're real, and then fixing them, will be automatable end-to-end.

The question stops being "Can AI do this?" and becomes "How do we do this responsibly, at scale?".

To think this through, I've found it useful to distinguish between model capability gaps and structural limitations.

In terms of model capabilities, we should just assume that the gaps get filled. Models are just going to get better and better and do everything that models can in principle do. If you start building something yourself on the edge of frontier model capabilities, it's highly likely that you're wasting your time; it'll be overtaken by an upcoming model update soon enough.

Then there's stuff that LLM models structurally can't do. LLMs are non-deterministic. Run the same query twice, you get two different results. That's useful when you're generating ideas and output. But if you give the model agency (the ability to perform actions), it's a potential problem. And if you give it access to offensive AppSec tools, it's a dangerous problem. An unrestrained model can do damage, attack the wrong target, leak sensitive data, or deliberately cover its tracks.

For anyone looking for proper assurance of their security, they need reliability, reproducibility, effective safety guards, and a robust audit trail. You can't prompt any of this into models. Fundamentally, this technology cannot self-govern.

As model capabilities improve, the structural limitations actually get more significant, not less. More capable models take bigger, more consequential actions with less oversight. As capability gaps close, the stakes go up, and the structural limitations matter more.

The power of LLMs to transform AppSec is clear. We've proven some amazing capabilities in our research labs, and we'll be sharing details of those soon. It's as if we've created a magical beast. It can do amazing things that weren't possible before. But that beast has claws. Let it loose, and it will create mayhem. To unlock the beast's power in a controlled way, we need a strong cage around it.

Architecturally, what this looks like is a strong safety and governance layer around the agentic core. Every time the model wants to perform an action, it goes through this layer, with deterministic policy enforcement, human-in-the-loop decisions, and a proper audit trail. This doesn't have to involve friction or overhead; rather, it's what enables serious users to access the sheer power in a controlled way.

The job of the security practitioner is about to get harder, not easier

The question on many pentesters' minds right now is whether they're being replaced.

The honest answer is no, but the job is going to change. And we already know the shape of the change because software engineering is going through it.

When we discussed PortSwigger's research and products recently on Risky Business.

The path ahead for security practitioners, pentesters, and security engineers is likely to follow a similar trajectory as software engineers. The best developers today are not typing code into their IDE. They are overseeing the agentic engine. They are making architectural decisions. They are guiding it and taking a risk-based approach to what PRs they actually look at. But they didn't stop being software engineers.

Security testers will make the same transition.

In the near future, you'll no longer have to set up your Intruder attacks, configure the payloads and the filters, and monitor the results. You might not even need to think about which attacks would be worth executing. If you want, you'll be able to lean on the automation to choose which attacks to propose. That's quite a lot of drudgery that can be taken off your plate.

But you'll need to understand the attacks and what they're doing. And you'll need to apply judgement about what you let happen. You're still bringing the same craft and expertise as you bring today. Just as if you were overseeing a team of junior pentesters who could go off and do the grunt work for you.

This is really the same evolution that I was driving in myself when I started work on Burp Suite, over 20 years ago. The first tool I wrote was Burp Intruder. In those days, most testing involved intercepting individual requests, changing one parameter at a time, and reading the responses. That was horrendously mechanical and boring. You could write Perl scripts as a one-off for particular attacks, but even that was painful. Burp Intruder was such a breakthrough because it let me automate a ton of boring work, set that up efficiently through a nice UI, and spend my time on more interesting things where my judgement mattered. The new AI-driven productivity is really an extension of that. Today, launching dozens of Intruder attacks is tedious: setting up the payloads and config, looking at the results. This is the next frontier of boring workload that we can take off the user.

The anxiety that some pentesters have is that their role will disappear, that the automation will do so much that there's nothing left. But this hasn't been the outcome for software engineers. As James Kettle said in our Risky Business interview:

"What these systems do, what this research is showing, is basically that it amplifies your impact, and it means you need to make serious decisions about what to do next, what to prioritize, use your intuition more at a much higher rate than you had to previously. Let's face it, a lot of pentesting is really repetitive. And because of the way that tools work with AI, that's where you get the best results. Those are the elements that you don't need to waste your time and energy on. And you get to apply it to the interesting stuff."

Just like with software engineering, the AppSec practitioner's craft, which they built up over the years of doing this work themselves, is going to be vital to be able to provide the oversight effectively. The role will evolve from doing the testing hands-on, to governing the agentic engine that does the heavy lifting. The practitioner won't have any filler tasks to do that don't require thinking. If anything, they're going to be busier.

Inside the next generation of Burp AI

At PortSwigger, our work on Burp Suite is always heavily influenced by what comes out of our incredible research team. Over the past year, some of my conversations with James Kettle really focused my attention on what we needed to build next.

James will present his full research at Black Hat in August. But suffice to say, it's hot stuff. James has essentially implemented his entire research methodology on an agentic foundation, and the results are mind-blowing. While he was sleeping, it came up with a novel attack technique and used it to compromise a bank. As James said: "I just came in in the morning and it said: here's an API key that I stole from a bank. I didn't even know it was looking at that target."

We released our first AI capability in Burp in early 2025. These are a great set of copilot features that let you offload tasks, work more efficiently, and discover issues that you might have missed.

What we built next is a new agentic engine at the heart of Burp. It has access to Burp's tools, can reason, make decisions about what actions to perform, consume the results, and continue iteratively. It's essentially Claude Code for hackers, and it unlocks the same core power that James described.

For a research-grade tool targeting bug bounty websites, power is key. But for enterprises who care about safety and governance, and for pentesters needing to provide reliable assurance, sheer power isn't enough. They need safety and policy enforcement, human-in-the-loop on the key decisions, and strong audit logs to prove what has happened. All of this is baked into the core architecture of our next generation AI features.

One key finding from James's research is that although frontier models are highly capable out of the box, their power is hugely magnified when they're given access to the right tools. Sure, a model can hand-crank HTTP requests using curl and read the responses looking for vulnerabilities. But that's crazily inefficient, expensive, and unreliable.

The sheer power of Burp Suite's agentic AI is down to our reliable, deterministic tools that have been battle-hardened in the wild by hundreds of thousands of pentesters over two decades. Those tools "just work" on different applications and different protocols, and they're already optimised for reliability and efficiency.

We're currently running a private beta with a bunch of users who are using Burp's new agentic AI every day and telling us what they find. They're helping us get all the details right. If anybody really would like to apply to join the beta programme, email trials@portswigger.net. (Of course, no promises that we can accept you.)

The new capabilities will be on public release before James's research drops at Black Hat in August.

About the author

Dafydd Stuttard is the Chief Swig of PortSwigger and the creator of Burp Suite, the industry's go-to toolkit for web app and API security testing. A former pentester himself, he is also the author of the Web Application Hacker's Handbook and created its interactive, online successor, the Web Security Academy. Both continue to serve as invaluable resources for aspiring bug bounty hunters and experienced pentesters alike.

Dafydd Stuttard

@DafyddStuttard

Latest Posts

Burp Extensibility 2026: Awards, Talks, and Highlights

19 June 2026

Burp Extensibility 2026: Awards, Talks, and Highlights

3 ways custom scan checks turn practitioner knowledge into scalable automation

01 May 2026

3 ways custom scan checks turn practitioner knowledge into scalable automation

Senior pentesters have a deeply refined intuition about what is vulnerable in an environment. The problem? That expertise is often siloed with an individual and trapped in their notes or Python scripts.

28 April 2026
