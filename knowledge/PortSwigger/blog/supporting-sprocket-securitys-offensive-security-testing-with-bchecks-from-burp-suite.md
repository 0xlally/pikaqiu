# Supporting Sprocket Security's offensive security testing with BChecks, from Burp Suite

Source: https://portswigger.net/blog/supporting-sprocket-securitys-offensive-security-testing-with-bchecks-from-burp-suite
Fetched: 2026-06-28T09:15:25.031826+00:00

Supporting Sprocket Security's offensive security testing with BChecks, from Burp Suite

Emma Stocks |

Wednesday, 6 September 2023 at 17:55 UTC

The US-based organization Sprocket Security provides continuous penetration testing services to customers by monitoring clients’ attack surfaces and searching for new and novel exploitation techniques that they report on using their platform.They use Burp Suite Professional and Burp Suite Enterprise Edition to support their testing workflows, and have recently begun to experiment with PortSwigger’s new BChecks feature.

A lot of their research and development is centered around testing at scale, and finding solutions that support them automating and streamlining their workflows is a core focus at their fortnightly hackathon-style meetups. We spoke with Nicholas Anastasi, Director of Technical Operations, along with a few members of his team, to discuss their discovery of BChecks and how they’ve been incorporating the scan checks into their testing processes.

Discovering BChecks

Nate Fair, a Penetration Tester at Sprocket Security, spotted the BChecks competition we ran recently and felt he had to introduce it to the team - their fortnightly research and development session presented the perfect opportunity.

We sat and we went through the documentation together. But then … jumped on it and kind of started working on it. We started really simply, that NTLM authentication endpoint check that I wrote was literally the first thing we probably put together.

Learning how to work with BChecks

The BChecks language is designed to be human-readable and quick to pick up, contributing to the overall ease and flexibility of the BChecks themselves. Despite its relative simplicity, it's capable of conditional logic, regex matching, sending raw HTTP requests, multiple helper functions for encoding, and much more.

Using their fortnightly meetups, the team at Sprocket Security powered through the BChecks documentation and were able to pick up the scripting language relatively easily.

I like the scripting language. It's not super hard to follow. With any programming language, it's getting to the point where you can use it without thinking, [where you can] write it like, you know, I want to accomplish this goal, and you just do it instead of having to reference the docs over and over again.

As a group, they enjoy gamification and like to introduce competitive elements to their get-togethers. They gravitate toward tools or systems that allow them to work closely and collaboratively, and have fun at the same time. As a small team, they want tools they can easily manage and work with, as they don't have time to spend installing massive complex systems.

When we came across [BChecks], we were just like, hey, this is this little nugget of awesome power and we can immediately start to see how we can use something like this across a massive scale.

Automating BCheck production with ChatGPT

Sprocket Security's three main organizational drivers are continuous penetration testing, attack surface management, and adversary simulation. With those goals in mind, it's clear to see how AI tools like ChatGPT could save the team time and help to free up resources. But how did BChecks fare when the team put it through the OpenAI chat tool?

ChatGPT is not too smart. So the fact that it [was able to convert all the templates] kind of says to me that the language is relatively simple to follow.

Nicholas misinterpreted our BChecks competition, thinking it was measured on who could produce the most BChecks within a certain time frame, which is how he thought to start using ChatGPT initially.

I fed the BChecks documentation to ChatGPT and then fed it nuclei templates and told it to convert the contents over.

It turned out to be a happy accident though, as the team now have multiple scan checks that they can use directly from within Burp Suite. They plan to utilize these to develop their client services offerings in the future, to provide more tailored, client-specific security services.

Incorporating BChecks into their testing workflow

To allow them as much time as possible to perform manual testing, the team is always looking for ways to automate parts of their testing workflows in any direction, whether that's exploiting vulnerabilities across their client base or using a new tool.

A lot of those kinds of secret scanning BChecks that I wrote and published have kind of made their way into our workflow. It's so easy to get them there and we operate out of Burp Suite a lot.

As the team all use Burp Suite Professional on a daily basis, they're looking for tools and processes that can support their workflows within the software.

I think early on we realized. The power of this [BChecks] is that we can actually do this against crawled urls, too. It's not limited to just whatever the domain name is. Using it in the context of everything Burp gives you is where it really shines.

A large aspect of the Sprocket Security team's workflow is their documentation - they call this "Attack Narratives". They use a version of these for their clients to provide POCs and reporting, but following their discovery of BChecks they have big plans for the future development of these "Attack Narratives".

We see specific clients being able to leverage those BChecks to say, hey, anybody who

hops on this project, we saw this vulnerability previously. Here's a BCheck for it and then retest, or verify that it's still not present in another location in the app.

The team plans to continue to use custom BChecks internally before publishing them publicly on the GitHub repo.

A final thank you to the team at Sprocket Security for joining us on a call - it was a fantastic opportunity for us to see the real world impact of BChecks and we loved hearing about all the innovative ways they've been implemented across the team's workflows.

Feeling inspired?

If you've been inspired by the creative ways that the team at Sprocket Security have implemented BChecks into their testing workflows, why not have a go at writing some for yourself?

Read about how to use BChecks in our documentation, or watch our recent Burp Suite Short video. Then discover existing BChecks created by the PortSwigger team and the Burp Suite user community in the GitHub repo. If you think you've come up with a novel idea for a BCheck, make sure to submit a pull request for the PortSwigger team to review.

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
