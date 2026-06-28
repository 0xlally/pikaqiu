# ‘Train the basics’ – Bug bounty hunter ‘Xel’ on forging a lucrative career in ethical hacking

Source: https://portswigger.net/blog/train-the-basics-bug-bounty-hunter-xel-on-forging-a-lucrative-career-in-ethical-hacking
Fetched: 2026-06-28T09:15:26.576749+00:00

‘Train the basics’ – Bug bounty hunter ‘Xel’ on forging a lucrative career in ethical hacking

Adam Bannister |

Thursday, 21 January 2021 at 14:06 UTC

Switzerland-based security researcher shares the secrets of his success

INTERVIEW Ranking among the top 10 hackers on bug bounty platform YesWeHack’s all-time leaderboard, Raphaël Arrouas’ methodologies will be of interest to security researchers of all abilities.

Arrouas, who lives in Switzerland and hacks as ‘Xel’, started bug hunting in early 2019 and joined Paris-based YesWeHack in October 2019.

Speaking to The Daily Swig, he shares the secrets of his success, offers tips for bug hunting newbies, and reflects on the pleasing progress of Europe’s crowdsourced security market.

How did you get into cybersecurity and hacking in particular?

I first started looking into computer security when I was 14, but it wasn’t until I majored in cybersecurity at the Centrale Supélec engineering school, where I had the project to become a penetration tester, that I started to learn a lot about offensive security.

My hacking expertise was first self-learned in parallel with my training at the engineering school, and sharpened during my career as a penetration tester.

After three years’ working as a penetration tester I quit my job to do bug hunting full-time, as it appeared to me to be an opportunity that I shouldn’t miss out on.

DON’T FORGET TO READ Bug bounty leader Clément Domingo on cybersecurity in Africa, hacking events, and chaining vulnerabilities for maximum impact

You’re counted among the top 10 hackers on YesWeHack’s leaderboard, so you’re obviously making good returns, but did it feel like a big gamble at the time?

It was a bit of a gamble because I had only done three months of bug hunting before I quit my job.

But in the computer security fields, you know that if you’re looking for jobs you’re going to find one anyway [given the skills shortage], so it’s not that much of a gamble.

I started making good money pretty fast. I dedicated some time at first to the Swisscom program, which was the first major bug bounty program in Switzerland.

I felt this was a good opportunity to invest time in local companies and it really paid off in the end.

Swiss hacker Xel is ranked on YesWeHack’s top 10 leaderboard

How do you account for your success?

I have no commuting time so I can work at any hour of the day and it really focuses my efforts.

My training as a general engineer really helps me too, because I have confidence in knowing how parts of a system are connected and where I should conduct my research.

Read more of the latest hacking news

I also benefit from my experience as a penetration tester, because I’ve been able to interact with a lot of corporate applications, which you don’t get a lot of practice with through learning platforms.

When I start working on a bug bounty program I am often familiar with the type of technologies deployed in the scope.

Are there particular types of bugs that tend to favor?

I tend to focus on complex web applications, which have a lot of entry points for exploitation, and critical bugs.

When a new program is published, I tend not to search for low-impact bugs immediately, because a good proportion of hunters go for the low-hanging fruit first, and there is more competition.

Instead, I prefer to investigate the application in depth, and would rather spend time working out the details of an exploit with a critical impact.

Focusing on impact rather than quantity allows me to dedicate more time to researching vulnerabilities in depth and learn something in the process. And it is worthwhile considering the payout scales, which usually greatly favor high and critical impact vulnerabilities.

I don’t only focus on critical vulnerabilities, though; I report all kinds of bugs.

I have no commuting time so I can work at any hour of the day – Xel

How do you choose your programs?

Usually, I estimate whether the scope seems to be well secured already or whether there are a lot of things to find. Therefore, I can estimate the number of bugs I can detect in a short time versus the bounty payouts and make my choice.

I like Java applications as well because these are usually treasure troves for critical bugs in my experience.

I also like building relationships with the teams that operate programs and the bug bounty platforms themselves. I believe it is important to build trust with the program owners, which sometimes encourages them to include more of the infrastructure within the scope.

What was the biggest bounty you’ve ever earned?

I found a series of zero-day RCE [remote code execution] vulnerabilities on the same product over one weekend, which netted me CHF32,000 ($35,000).

The highest amount for an individual bug I had was CHF10,000 ($11,000). I reached that amount several times for various vulnerabilities, including another remote code execution vulnerability.

The biggest impact I can think of is an unauthenticated RCE I identified last year on a product called Tufin SecureChange. This is a firewall orchestrator, so you can imagine the kind of impact it could have if exploited.

What hacking tools do you tend to use?

Mainly Burp Suite. And I select tools that allow me to exploit specific vulnerabilities, but my tests are done manually in general.

RECOMMENDED ‘As long as people are the ones writing code, there’s going to be insecure code’ – Tommy DeVoss on his post-jail bug bounty exploits

Have you encountered any problems with the coordinated disclosure process? If so, what happened?

I’ve encountered issues with programs that were not willing to pay what was advertised, without understandable justification. When this happened, I usually immediately stopped working with the program.

Companies that have been introduced to the bug bounty philosophy and have regular contacts with the platform generally treat researchers more fairly.

YesWeHack introduces companies to the philosophy of bug bounty hunting and they point out the importance of working with the researcher and so on, and this builds trust and long-term relationships. This environment and the variety of available scopes are part of the many reasons I enjoy working on this platform.

They are also very supportive of researchers and help companies specify safe harbor policies.

It’s an important point because here in Switzerland the law is very narrow in regards to [good faith] hacking. I’ve never had any legal issues but in in theory it’s important.

RELATED Intigriti launches EU-backed bug bounty program for Matrix secure communications tool

To what extent do you think the European bug bounty industry is catching up with its more established US counterpart?

I think the European bug bounty industry is catching up with the US.

For example, YesWeHack, which has done a great job introducing crowdsourced security to European companies, has been actively expanding outside of Europe, notably with programs coming from Asia. They have more than doubled their number of program launches this year, so I would say the industry is in full swing.

In Switzerland, where bug bounty hunting was not well established until recently, I also see more and more programs springing up.

The European bug bounty market has become more established over recent years

What advice would you give to someone who wants to become a bug hunter or has recently started bug hunting?

Train the basics about networking, development, frameworks, OS, cryptography, authentication, and network protocols to gain a deeper understanding of each scope.

Then train to exploit each category of vulnerability. Many labs are available online, such as PortSwigger’s excellent Web Security Academy. If you're bored by training, do some bug bounty for a while, until you feel like you need to get back to training.

Read a lot of security articles – vulnerability disclosures, PoCs – and save them whenever you feel they are interesting. It is important to understand the core of each vulnerability, so that you may adapt your PoC if, for example, a WAF prevents you from exploiting the vulnerability.

RELATED ‘I thought it was a complete fluke’ – Katie Paxton-Fear on her bug bounty baptism and why AI will never fully replace security researchers

Everyone is different, but I would recommend not to write down notes – except report templates or select cheat sheets – because you need to train your memory at recognizing familiar frameworks, applications, and environments, and know where you can find the information you need.

Your goal is to speed up your analysis of the scopes so that you can focus on areas worth investigating.

Analyze source code whenever available. Do not hesitate to deploy elements of the scope on your own machine, if available, to get a better understanding of attack vectors. Spend some time on the reconnaissance.

Try not to report vulnerabilities you find ASAP, but attempt to increase criticality by combining them with [other bugs]. Spending time to bypass a WAF is often worthwhile.

And finally, don’t give up – bug bounty hunting takes practice, and it is hard at first not to have duplicates.

The hard thing with bug bounty is knowing how to organize your week because there are constantly new things to test and it’s pretty stressful, so it’s also important sometimes to take a break, do some sports, things like that.

Do you expect to continue doing bug hunting for a long time? Any plans to do anything else?

I love my job, so I plan to do this for quite some time. At the moment I have no plan of doing anything else.

READ MORE Collaborative bug hunting ‘could be very lucrative’ – security pro Alex Chapman on the future of ethical hacking

Adam Bannister

@Ad_Nauseum74

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
