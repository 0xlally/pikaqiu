# So you want to be a web security researcher?

Source: https://portswigger.net/research/so-you-want-to-be-a-web-security-researcher
Fetched: 2026-06-28T09:17:29.145391+00:00

So you want to be a web security researcher?

James Kettle

Director of Research

@albinowax

Published: Wednesday, 23 May 2018 at 14:00 UTC

Updated: Thursday, 1 August 2024 at 08:31 UTC

Are you interested in pushing hacking techniques beyond the current state of the art and sharing your findings with the infosec community? In this post I’ll share some guidance on how to become a web security researcher, shaped by the opportunities and pitfalls I’ve experienced while pursuing this path myself.

What is a web security researcher?

Web security researchers are people who go beyond using known hacking techniques likes SQLi and XSS, and discover new threats to websites. These can be innovations that make existing techniques more powerful like this approach to local+blind XXE exploitation, or entire new threat classes like Web Cache Deception.

It's extremely hard to defend websites against unknown attack techniques, so they can often be used to exploit huge numbers of otherwise-secure websites. This means that publishing such discoveries to give websites a chance to patch is crucial for the health of the security ecosystem.

Note that some people use the term 'security researcher' more loosely to refer to anyone who works in offensive security, even if they're just applying off-the-shelf tools and techniques.

Breaking stuff for a living

Most research is about taking existing techniques that bit further, so the first step is to get well acquainted with the current state of the art. The fastest way to achieve this is to get a job where you spend most of your time applying web hacking techniques. A lot of good people have shared detailed advice on getting into the security industry, so I’ll keep this section brief.

I recommend a practice-focused approach starting with our Web Security Academy, moving on to more open ended challenges like my own hackxor.net, advancing through soft, low-reward targets on HackerOne and BugCrowd, and then finally onto well established high-payout bounty programs. Once you have a few publicly disclosed vulnerabilities it should be pretty easy to join a security consultancy and spend every day hacking stuff. That said, bug bounty hunting isn't for everyone so we've launched the Burp Suite Certified Practitioner certification as an alternative way to prove your skills and get that full-time hacking job.

There are plenty of free online resources to help you on the way, including our Web Security Academy, HackerOne's Hacker101, and the OWASP testing guide. As for books, I’d recommend reading the WebApp Hacker’s Handbook, and The Tangled Web. The aforementioned Web Security Academy is intended to be an actively maintained, interactive replacement to the WebApp Hacker's Handbook, but it'll take us some time to cover all relevant topics, so for now I'd recommend using both.

Moving beyond known techniques

Once you start working full time breaking stuff, you’ll initially learn loads but after a while your technical expertise will plateau unless you make a concerted effort to keep learning. Refusing to let yourself stop at this barrier is the single most important step to becoming a web security researcher.

Hunt forgotten knowledge

Everyone knows you’re meant to keep up with new developments by monitoring industry experts, news aggregates and security conferences. I even run a subreddit for this purpose: r/websecurityresearch. However, to exclusively follow new developments is to overlook a treasure trove of forgotten and overlooked research.

Every time you read a good quality blog post, read the entire archive. This will often unveil invaluable, forgotten tidbits of information. For example, take this post by RSnake about DNS rebinding written in 2009. DNS rebinding completely bypasses IP/firewall based access controls on websites, and the only effective way to mitigate it is by making your application whitelist the HTTP Host header. And yet at the time, people quickly assumed it was mitigated by browsers; this forgotten vulnerability only re-entered common awareness with a string of exploits nine years later.

Perusing archives will also help you avoid wasting time replicating work that’s already been done by someone else, such as re-inventing a CSS attack one decade later. That said, some research is genuinely hard to find so occasional duplication is inevitable. I've had a published technique collision with one researcher only for both of us to discover that kuza55 had done the same thing five years prior. So, do your best to avoid duplicating research but if it happens anyway don’t panic - it happens to all of us.

Collect diversity

To connect threads and spot opportunities that other people miss, it’s crucial to collect information from a range of different sources. For a start, don’t limit yourself to reading security content - you’ll quickly find documentation can also serve as an exploit construction manual. Again, and this may be pretty obvious, but as well as trying to solve problems by Googling and posing well phrased questions to X/Reddit/StackOverflow, ensure you ask colleagues - there’s a huge amount of knowledge floating around the community that people haven’t opted to share publicly.

Beyond that, try to ensure your own experiences are diverse too.

Doing black-box pentests for a security consultancy should expose you to a broad range of external and internal web applications, the likes of which you’ll rarely encounter in a bug bounty program. But the time constraints will rob you of the chance to understand an application with the familiarity that comes from months of bug bounty hunting with a single target. And although it’s often slow and constrained, white-box source code reviews can offer an irreplaceable alternative perspective, prompting attacks a black-box tester would never conceive. To nurture research, you ideally want a healthy mix of all three. Further experiences like playing CTFs and coding web applications can also add useful perspectives.

No idea is too stupid

One of the worst traps to fall into is dooming a great idea by assuming it won’t work and not trying it, because “someone else would have noticed it already” or “that is too dumb to work”. I’ve definitely fallen for this one before - one piece of research arrived two years later than it should have done thanks to such a mistake. Whether it's bypassing authentication by trying to login with the same password repeatedly, or breaking into a Google administration page by switching from your laptop to your phone, the path to your next great exploit may well require a really stupid idea.

Abandon comfort

If a technique has a reputation for being difficult, fiddly, or dangerous, that's a topic in dire need of further research. After repeatedly experiencing breakthroughs due to being pressured into exploring topics well outside my comfort zone, I've decided that the fastest route to novel findings is actively seeking out topics that make you uncomfortable. Chances are, these topics are avoided by other hackers, giving them serious research potential. To me, this is the only plausible explanation for why I was able to take a technique first documented in 2005, and presented again at DEF CON in 2016, and use it to earn $70k in bounties in 2019.

Iterate, invent, share

Iterate

The easiest way to get started is to find some promising research by someone else, build on it by mixing in other techniques, then apply your new approach to some live targets to see if anything interesting happens

For example, this post on CORS misconfigurations pointed out an interesting behaviour and suggested that this behaviour was prevalent, but stopped short of exploring the impact on individual websites.

I took this concept and applied it to bug bounty websites where I could legally explore the impact and try my hand at evading any mitigations they might have. Along the way I made some enhancements using common open redirect exploit techniques, discovered the ‘null’ origin technique by reading the CORS spec, and explored cache poisoning possibilities.

Nothing in this process required sudden leaps of intuition or outstanding technical knowledge, and yet the final product - Exploiting CORS misconfigurations for Bitcoins and bounties - was easily as well received as flashier efforts.

Invent

Iterating on other people’s work is great, but the best research often seems to appear out of nowhere, be it Relative Path Overwrite or Web Cache Deception. My view is that such discoveries are caused by personal experiences that act as hints. I refer to these as leads or breadcrumbs as they’re often cryptic and it may take quite a few of them to guide you all the way to a useful discovery.

For example, in 2011 I was trying to crack the CSRF protection used by addons.mozilla.org. I had bypassed the token check, but they also validated that the host in the Referer header matched the current site. I asked for help on the sla.ckers forum, and ‘barbarianbob’ spotted that Django determines the current site’s host by looking at the HTTP Host header, and this could be overridden with the X-Forwarded-Host header. This could be combined with a Flash header injection vulnerability to bypass the CSRF check, but more importantly it was the first breadcrumb - it hinted that applications may rely on the host header to know their current location.

A while later, I took a look at the source code of Piwik’s password reset function and found a line that looked something like:

$passwordResetLink = getCurrentUrlWithoutQueryString() + $secretToken

Aha, I thought. Piwik uses PHP which has hilarious path handling, so I can request a password reset at http://piwik.com/reset.php/foo;http://evil.com resulting in an email with two links, and the secret token being sent to evil.com. This idea worked, got me a bounty, and laid the foundation for the subsequent finding.

The third and final crumb was the the way Piwik tried to patch this vulnerability - they replaced getCurrentUrlWithoutQueryString() with getCurrentUrlWithoutFileName(). This meant that I couldn’t use the path for an exploit anymore. Thanks to the encounter with Django earlier, I decided to dig further into the code to find how Piwik determined what the current host name was, and discovered that like Django, they used the HTTP host header, meaning I could easily generate poisoned password reset emails. As it turned out, this technique worked on addons.mozilla.org too, and Gallery, and Symfony, and Drupal, and a whole host of other sites, finally leading to Practical HTTP Host Header Attacks.

By spelling out the discovery process in such a verbose way, I’ve hopefully demystified the research and made it look less like an idea spontaneously appearing out of the blue. Viewed from this perspective, it looks like the core skill (beyond pre-existing knowledge and breadth of experience) lies in recognising these breadcrumbs and persistently chasing after them. I can’t quite articulate how to do this yet, but I do know to treat as a lead anything that makes you say “this makes no sense”.

Share

Finally, it’s crucial to share your research with the community. This will help increase your profile and perhaps persuade your employer to allocate you some more research time. Beyond that, it will help you avoid wasting time and spur further research - commenters are really good at pointing out prior work you had no idea existed, and there’s nothing more rewarding than seeing another researcher building on your ideas.

Please don’t think a technique or idea isn’t worth sharing just because you don’t have ground-breaking discovery, two logos and a presentation - just post whatever you have (ideally on a blog and not just some poorly indexed locked-down platform like X/Twitter). X is good for promoting research, but not everyone is on there I'd recommend also using alternative channels like r/websecurityresearch.

When sharing research, it’s always helpful to show at least one example of your technique being applied to exploit a real application. Without this, people will inevitably have difficulty understanding it, and may doubt that it has any practical value.

Finally, presentations are great for reaching a wider audience, but beware of getting caught up in the infosec circus circuit and spending your days repeating past presentations.

Conclusion

I have a lot more to learn about web security research myself, so I hope to revisit this topic in a few years with substantially more of a clue. Also, I expect other researchers have different perspectives, and look forward to learning from any insights they decide to share.

Summary of my tips on how to become a web security researcher

Hunt forgotten knowledge by reading archives

Consume information from as many distinct sources as possible

Prefer difficult/scary topics

Iterate, invent, and share

No idea is too stupid

If you've found this post useful, you might also enjoy my presentation Hunting Evasive Vulnerabilities, which takes an in-depth look at why people miss vulnerabilities and how you can find them, and also How I choose a security research topic. Finally, if you’re looking for some reading to get yourself started, in addition to our yearly Top 10 Web Hacking Techniques roundup I’ve created a list of various blogs that have inspired me over the years. Good luck and have fun!

James Favourites

How to research

Back to all articles

Related Research

How to build custom scanners for web security research automation

03 October 2023

How to build custom scanners for web security research automation

Smashing the state machine

the true potential of web race conditions

09 August 2023

Smashing the state machine

the true potential of web race conditions

How I choose a security research topic

14 June 2023

How I choose a security research topic

Browser-Powered Desync Attacks

10 August 2022

Browser-Powered Desync Attacks
