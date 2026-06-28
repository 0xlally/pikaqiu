# How to turn security research into profit: a CL.0 case study

Source: https://portswigger.net/research/how-to-turn-security-research-into-profit
Fetched: 2026-06-28T09:17:26.305981+00:00

How to turn security research into profit: a CL.0 case study

James Kettle

Director of Research

@albinowax

Published: Tuesday, 6 September 2022 at 12:55 UTC

Updated: Tuesday, 6 September 2022 at 12:55 UTC

Have you ever seen a promising hacking technique, only to try it out and struggle to find any vulnerable systems or non-duplicate findings? In this post, I'll take a concise look at the most effective strategies for avoiding this problem. As a case study, I'll use the CL.0 desync attack class recently explored in Browser-Powered Desync Attacks.

Analysing the technique

If you're looking for bounty success, it's important to understand the competition. Who else is looking for this bug class, and with what tools and techniques? Good research gets a wildly varying amount of attention from the security community, largely based on how valuable it appears at first glance. This creates an interesting tension - the less valuable research appears, the less competition you'll have turning it into bounties. In effect, there's a scale:

If research is poorly explained or under-hyped, you can sometimes have major success simply by applying it. For example, CORS Misconfigurations missed the infosec hype train, so upon reading it I tried the technique as-is and immediately found a bunch of vulnerabilities with very little effort, leading to deeper research and ultimately Exploiting CORS Misconfigurations for Bitcoins and Bounties.

Conversely, if research is presented at a major conference and looks exciting, chances are you'll be competing against other bug bounty hunters using the same technique and tools. For example, people are already sharing successful findings based on the techniques from Browser-Powered Desync Attacks.

Immediately after a presentation is published there's likely to be many vulnerable systems, and you can beat other hackers to reporting them simply by being faster, understanding the technique better, doing more recon, or being more persistent. Over a few weeks and months, this will become tougher and less effective. At this point, you'll need to innovate.

Identifying the opportunity

Identifying opportunities to build on someone else's research is a bit of an art form. Start by getting really familiar with the research, and then ask yourself some questions:

Did the researcher miss anything?

Did they release a scanning tool? If not, can I make one?

If they did release a scanner, does it detect every vulnerability mentioned in the paper?

Can I see any blind spots in their scanner's design or code?

Try taking a look through Browser-Powered Desync Attacks and asking these questions.

One of the techniques I shared is server-side CL.0 desync attacks. It's only touched on briefly, and the corresponding scan check in HTTP Request Smuggler is quite simple. Notably, it references a presentation which mentions CL.0 style vulnerabilities two years prior! It seems like because no tool was released to test for these, it was overlooked by the community. I under-estimated this desync class myself until I stumbled on one in the wild a year ago. Note that the older publication mentions several obfuscation techniques to make a CL.0 desync happen, but these aren't implemented in HTTP Request Smuggler. This looks like an opportunity.

Going hunting

A few hours of coding later, I'd added most of the obfuscation techniques from this paper, plus some more I made up and all the classic ones usually used to hide the Transfer-Encoding header. I set this running on my 20gb Burp Suite project file of bug bounty sites, and checked back in a few hours later to find around a hundred vulnerable websites, covering roughly 15 different bug bounty programs.

So, which permutations performed the best? The following reliable old-school techniques worked:

Content-Length x: 7

Content-Length : 7

Foo: bar

Content-Length: 48

Plus these new content-length specific techniques:

Content-Length: +7

Content-Length: 0, 7

Content-Length: 7.0

And the following techniques flopped:

Content-Length: -7

Content-Length: 007

Content-Length: 7e0

I've just pushed this update out so everyone can make use of it. Also, now I've got the obfuscation system hooked into the CL.0 scancheck, adding most new techniques is trivial. Just add the permutation code:

case "CL-commaprefix":

transformed = Utilities.replace(req, "Content-Length: ", "Content-Length: 0, ");

break;

and register it:

clPermutations.register("CL-commaprefix", true);

I regard adding new permutations as the easiest way to find fresh desync vulnerabilities that everyone else is missing, and ultimately earn bounties. Even if you struggle to invent your own novel permutation techniques, you can find quite a few documented but unimplemented in assorted academic papers on the topic.

Summary

If you've found an overlooked piece of research, you might be able to turn it into profit simply by applying it. For mass success with more popular techniques, you'll probably need to bring something new to the table, but this can be as easy as a good idea and a few lines of code.

If you're interested in a broader look into the art of finding vulnerabilities others miss, you might enjoy watching Hunting Evasive Vulnerabilities, and reading So you want to be a web security researcher?

Good luck, and have fun!

Request Smuggling

Back to all articles

Related Research

How to distinguish HTTP pipelining from request smuggling

19 August 2025

How to distinguish HTTP pipelining from request smuggling

06 August 2025

Making desync attacks easy with TRACE

19 March 2024

Making desync attacks easy with TRACE

Making HTTP header injection critical via response queue poisoning

22 September 2022

Making HTTP header injection critical via response queue poisoning
