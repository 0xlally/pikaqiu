# How I choose a security research topic

Source: https://portswigger.net/research/how-i-choose-a-security-research-topic
Fetched: 2026-06-28T09:17:26.000425+00:00

How I choose a security research topic

James Kettle

Director of Research

@albinowax

Published: Wednesday, 14 June 2023 at 13:09 UTC

Updated: Thursday, 10 April 2025 at 08:27 UTC

How do you choose what topic to research? That’s the single most common question I get asked, probably because selecting a topic is such a daunting prospect. In this post, I’ll take a personal look at how I select topics for security research. As a case study, I’ll use Smashing the State Machine: the True Potential of Web Race Conditions.

The hardest part

Before we start, I should mention that I firmly believe that choosing a topic is not the hardest part of web security research.

I’ve spoken to so many people who have cool ideas but never attempt to execute them. On the rare occasion that someone does mention a research idea that I think is doomed from the outset, it’s clear that attempting it will still provide them with a major learning experience - hardly a terrible outcome.

In fact, I don’t think that coming up with research ideas is the hard part either. Once you start researching, you’ll likely find every topic you explore leaves you with ideas for three more projects.

I think the hardest part of research is knowing when to bail, and when to push on.

Fast failure

My primary criteria when I evaluate a topic is how much time I’ll need to invest before I have enough information to decide whether to abandon it or continue. Knowing when to abandon a topic and when to push on is an extremely valuable skill for research, and it’s worth putting thought into this before starting.

This year, the attack-concept I wanted to explore initially looked like it required a major up-front time investment. However, I identified a short-cut - if I could build a test website that was vulnerable and reasonably realistic, that would prove the concept was pursuing. I built the website, quickly discovered that the attack concept was extremely unrealistic, and quickly pivoted to a different concept.

The second concept showed just enough promise to make me waste six weeks on it before it flopped too. When looking for a third concept, race conditions was an attractive topic because I already had powerful tooling from the prior project. This meant it would only take about a day to adapt the tooling, and a week or two of manual testing to see if I could discover something significant in the wild. I found a novel high-impact vulnerability in under a week, which cemented my commitment to the topic.

The fear factor

I like to research topics I’m scared of. Fear is a great indicator of something I don’t fully understand, and challenges that I don’t know how to tackle. Race conditions provided this in buckets, and I place this up-front and center in my abstract:

For too long, web race-condition attacks have focused on a tiny handful of scenarios. Their true potential has been masked thanks to tricky workflows, missing tooling, and simple network jitter hiding all but the most trivial, obvious examples. In this session, I’ll introduce multiple new classes of race condition that go far beyond the limit-overrun exploits you’re probably already familiar with... [read full abstract]

Direct impact vs audience impact

As a security professional, it’s tempting to rate a research project’s impact based on the direct impact. For example, over the years I’ve seen a range of serious flaws in a certain popular CDN, and I suspect that if I directly targeted it, I could find multiple ways to take over all their customers’ websites - a reasonable chunk of the web. In terms of direct impact, this would be pretty good.

But when you submit to Black Hat, they ask you to specify ‘three actionable take-aways’ for the audience. How would my hypothetical CDN-popping talk answer this? The only action required would be from that sole CDN vendor - in effect I’d just be giving a war-story talk. These can be entertaining and inspiring, but that’s not what I’m aiming for.

I try to pick a topic where the audience will take away novel attack techniques, and any tools or methodology required to make them practical to apply.

Applicable audience

Over the last five years, my research has been focused on HTTP Request Smuggling and Web Cache Poisoning. Since I’m well-versed in this topic, doing further research directly on top has become relatively easy, and I’m perpetually aware of multiple promising ideas.

However, while creating the presentation for last year’s Browser-Powered Desync Attacks, I became acutely aware that it demanded an exceptional amount of prior technical knowledge from the audience.

Building on a little recent research often works well because you can summarise it yourself. However, building on a large volume of recent research means that anyone in the audience who isn’t already familiar is going to struggle, and overall less people will get the benefit.

This year, by focusing on race conditions - a topic with minimal recent developments - I’ve been able to start building on a foundation that most attendees will be familiar with. Relative to last year’s talk, you can expect this talk to have both greater potential for the experts, and greater accessibility for the masses.

Existing skill-sets vs personal development

There’s a second, more personal reason why I changed my research focus away from request smuggling. I expect request smuggling to keep yielding good research for years to come, but just like any topic, at some point it’ll dry up. If I maintain my exclusive focus on this topic, there’s a risk I’ll become over-specialised and end up in a bad place when the topic stops yielding fruit.

I deliberately choose race conditions to avoid this over-specialisation risk, even though I regarded it as a much riskier bet than doing even more request smuggling exploration. Personal development is a huge and easily overlooked part of research. I rarely repeat my presentations across months for the same reason - if you spend your time sharing the same presentation over and over, you’re sacrificing novel research time.

That said, there’s a balance to be had here - if you have specialist knowledge, that will give you an edge on certain topics. Race conditions appealed from the start because I’d observed low-level HTTP quirks that could enhance these attacks, and I’d also observed them in the wild when trying to exploit response queue poisoning.

Conclusion

No topic is perfect; this presentation has fewer case studies than usual for me because fully automated detection of these vulnerabilities is not practical. On the plus side, this leaves a large number of vulnerabilities on the table that the audience can find simply by applying the methodology.

Ultimately, I see over-thinking topic choice as a pitfall. Save your energy for the research itself - you’ll need it! If you found this useful, you might also like So you want to be a web security researcher, and the presentation Hunting Evasive Vulnerabilities.

If you’re got any thoughts or queries, feel free to ping me on Twitter or LinkedIn. Hopefully I’ll see some of you in-person at the presentation too!

How to research

Back to all articles

Related Research

How to build custom scanners for web security research automation

03 October 2023

How to build custom scanners for web security research automation

Hunting evasive vulnerabilities

13 May 2022

Hunting evasive vulnerabilities

So you want to be a web security researcher?

23 May 2018

So you want to be a web security researcher?
