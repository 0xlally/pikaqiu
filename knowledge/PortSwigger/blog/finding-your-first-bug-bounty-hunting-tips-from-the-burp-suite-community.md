# Finding your first bug: bounty hunting tips from the Burp Suite community

Source: https://portswigger.net/blog/finding-your-first-bug-bounty-hunting-tips-from-the-burp-suite-community
Fetched: 2026-06-28T09:15:15.249482+00:00

Finding your first bug: bounty hunting tips from the Burp Suite community

Emma Stocks |

Wednesday, 26 August 2020 at 12:25 UTC

More and more people are getting into bug bounty hunting. In fact, HackerOne’s 2020 report showed that “the hacker community nearly doubled last year to more than 600,000”. With so many people involved, we wanted to get some tips and tricks from seasoned professionals, to help out anybody thinking of becoming a bug bounty hunter.

We asked our community on Twitter, to find out what their suggestions would be for any new hunters looking to find their very first bug.

Here’s some advice on how to find your first paid bug bounty, according to our community:

1. Understand the process

New bug bounty hunters should narrow their focus, to allow them to get familiar with a specific vulnerability type and really get to grips with it. Our community advised newbies to start small, go for simple bugs, and really understand the end-to-end process before trying to hit those bigger targets.

Focus on the specific type of vulnerability.

Read writeups on this vulnerability.

Search for this vulnerability on the program you’re targeting.

When you find a bug, change the type of vulnerability and repeat step 1.

@0x1ntegral

Get intimately familiar with the application, tech stack, or feature you are trying to break.

Focus on how things work [read the RFCs] rather than running tools and one liners.

Knowledge and curiosity is free.

Recon ! = hacking [automate this]

@atul_hax

Don't overcomplicate things. Go for something easy that you understand. Even if your first bounty is small, it will feel much better than a big one later on.

@Troll_13

2. Find the uncharted territory

Looking out for unexplored, exploitable areas of the web is what a lot of people would say hacking is all about. Those dark and dusty corners, according to some of our followers, are a great place to make a start on finding the most well-hidden bugs.

Look for the dusty old corners of applications that everybody (especially developers) has forgotten. We ran into that all the time when I worked at Google - if you see the old Google logo or Times New Roman font somewhere, it's a good place to look. :)

@iagox88

Choose an old private program that pays small bounties.

@sh1yo_

3. Never stop learning

The most popular piece of of community advice, and this is something that can probably be said of most any profession or hobby, is to always keep learning. This advice will get you far in the world, and it's certainly something we encourage ourselves. That's why we built the Web Security Academy! As far as we see it, the only way you can be sure of never achieving something, is by not even trying to learn about it in the first place.

Avoiding most bite sized tips. A lot of #bugbountytips these days are n/a issues, or ones prone to dupe. Instead, focus on deep diving web app knowledge in your academy or @PentesterLab and then deep dive an app looking for bespoke flaws.

@codingo_

Reading your articles!

@root4loot

Keep doing, don't stop. Use burp and do some hunting in the wild. A chain of bugs including Apache struts misconfiguration, reflected XSS at the URL input, sensitive internal data disclosure.

@shail_official

Read the code (so focus first on public stuff). Read unit tests. Find the obvious/implicit/assumed stuff (data or behavior). Test it with non-obvious, out-of-limit, horrible and misplaced counter stuff.

@regilero

Your first bug bounty rewards

When it came to first successful bounties for our community, there was a definite focus on content discovery. It looks like, once again, knowledge has been proven to demonstrate power!

My first finding was sensitive information leakage, discovered the page by using Google dorks from my phone on the way home from work. Site:*.[site].com-www-blog-help ... and so on

@darrensmale

My first bug on the very first @bugcrowd bounty#1 was a stored XSS in a messaging back end i'd found using DIR buster list via intruder, storing and echoing out user controllable information - advice... Content discovery is more important than anything

@n0x00

First bug I ever found as an analyst (a massive SQLi) turned into my first miniature pen test (while billed as an analyst) which led to me discovering my love for penetration testing.

@THE_TERRORIZER

We also spoke with our very own Director of Research James Kettle - you may know him better as @albinowax - to find out what his first bug bounty pay-out was. In his own words: "My first paid bug was flukey stored XSS in YouTube - after that I got stuck for ages ... until I found Blogger, put some time into understanding its crazy design, and found a whole batch of bugs over several months."

A final word of advice for upcoming bug bounty hunters

We asked James for some final advice for any would-be bounty hunters. He said, "When learning, ensure you get practical experience via labs like the Web Security Academy and hackxor.net. When you're ready to hunt for real, pick a website with complex functionality (the lower the payout the softer the target), and don't move on until you've learned how it works inside out."

Bug bounty hunting, whether undertaken as a hobby or a full-time profession, can be a foot in the door for all manner of cybersecurity careers. Ethical hacking is fast becoming an integral component of security testing. According to HackerOne, "hacker-powered security" officially became a widespread term in around 2016.

From his beginnings as a bug bounty hunter, James experimented with pentesting, then moved his focus to becoming a security researcher. When he's not scouring the web for forgotten hacking methods and vulnerabilities, James plays an active part in creating new functionality for Burp Scanner.

If you want to read the full thread, check it out here.

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
