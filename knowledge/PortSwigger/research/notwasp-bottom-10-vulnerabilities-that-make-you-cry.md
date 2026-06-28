# nOtWASP bottom 10: vulnerabilities that make you cry

Source: https://portswigger.net/research/notwasp-bottom-10-vulnerabilities-that-make-you-cry
Fetched: 2026-06-28T09:17:27.842424+00:00

nOtWASP bottom 10: vulnerabilities that make you cry

Michael Stepankin

Researcher

@artsploit

Published: Thursday, 1 April 2021 at 10:59 UTC

Updated: Wednesday, 7 April 2021 at 14:07 UTC

Everyone's heard of the OWASP Top 10 - the often-cited list of major threats that every web developer should be conscious of. But if you cast your gaze across pentest reports and bug bounty findings, you'll discover another insidious theme emerges: 'vulnerabilities' that simply don't make sense.

Why? It varies. Some are simply misunderstandings, or even just beg-bounties. Others were once-great issues, crushed by browser updates but still living an oblivious half-life. Some are the offspring of policies, where sanity is left at the door. Then there's good old-fashioned filler. And finally, sometimes, we frankly have no idea.

Still, everyone likes lists, so we built a shortlist of uncountable terrible vulnerabilities and, after lengthy debate, have whittled it down to create... the nOtWASP Bottom 10.

10. Excessive concurrent sessions

Michael: Gmail and Facebook sessions last for years and you can access them from different devices simultaneously. If you don't want to provide this convenience to your users, you can implement a session timeout that logs them out after five minutes of inactivity.

Now imagine a scenario where you need to submit a money transfer request, and the bank asks you to fill out an online form with a dozen different input fields. You switch to another page to track down some of the details, verify them three times, then check out Reddit just for a sec. When you finally get round to submitting the form, you get an error saying that your session is no longer valid. You'll do it all over again, because you have to, but you probably won't be giving your bank a 5-star rating any time soon.

All joking aside, it's a bit of a double-edged sword: session timeouts can prevent some XSS exploitations, but the more often you need to type your password, the less attention you're going to pay each time. In the end, this probably increases the chance of someone accidentally typing their password on a malicious page.

9. Useless information disclosure

James: Some information disclosure is invaluable. Other information is near-useless outside of far-fetched, hypothetical scenarios, and yet still gets reported daily. My favourite example is "Server: Apache". This incredibly reckless banner opens the flood-gates for numerous hacks that are otherwise completely impossible. Nobody could possibly guess that a web server might be running Apache, or fingerprint it using one of 53 alternative techniques. Unfortunately, the vindictive developers won't let you disable it, so you'll need to deploy a reverse proxy. Don't worry, that never backfires.

8. Missing rate-limit/CAPTCHA

Michael: "Attacker could use this vulnerability to bomb out the email inbox of the victim" - so says one of the reports on HackerOne, sent to a government program. A month after the initial report, 23 messages had been sent back and forth about how to reproduce the vulnerability. Fix has been deployed, 10 people involved: taxpayers money well spent, right? Let's try to send one more email...

While the impact of brute-forcing one-time passwords can be devastating, it does not mean that every single application endpoint should limit the number of incoming connections from one IP. If a request just creates workload on the application, would you really want to fix it at all? Every single fix requires attention, engineering time, testing time, and sometimes even introduces new bugs. Missing rate-limiting without immediate impact (other than DOS) is often excluded from bug bounties precisely because it falls short of the risk vs. fixing cost threshold.

7. CSV Injection with no impact

James: I need to personally apologize for this one. When I proposed CSV injection as a vulnerability back in 2014, I envisaged hackers injecting malicious formulas to exfiltrate sensitive information from spreadsheets. However, during the research I discovered a formula that executes arbitrary code in Excel if the victim clicks through multiple scary warnings. The result? Pretty much any site with CSV export functionality is plagued with reports. I'm sorry.

https://www.contextis.com/en/blog/comma-separated-vulnerabilities

6. CVE-XXXX Unspecified vulnerability in unspecified component

Michael: There is nothing wrong with reporting an issue based on a vulnerable software version that you've identified, but it's very easy to get bogged down in thousands of these reports. It's likely that just a small portion of them are actually exploitable in the current conditions, or they may be not exposed to user input at all. It's hard work to find the 1% of exploitable ones and prioritize properly, but that's what companies do want to pay for. Scanning for known vulnerabilities is often just a first step; the true value is created by reporting issues that are validated and have clear exploitation vectors.

5. Ex-XSS

Gareth: At number 5 are those classic XSS vectors that no longer work. I'm talking about document.write(location.pathname), where the path is always URL encoded in modern browsers, or content-sniffing when the content type is plain text or json. As researchers, we fondly remember what a mess IE was and we had many tricks up our sleeves to exploit Internet Exploder. But nowadays, unless a user decides to play the equivalent of Russian roulette by navigating to a URL with outdated Internet Explorer to see if they get owned, these vectors are dead. Unfortunately, this doesn't stop bug bounty hunters from reporting them in their copy and paste reports from a scanner, so EX-XSS sits firmly in the number 5 spot.

4. Missing security headers

Michael: In 2021, you can't just write "<html>Hello World</html>", save it to index.html, and serve it with the default configuration of nginx. You'll probably be inundated with reports telling you:

It's not protected from Clickjacking. The fact that the page doesn't have any forms to submit or actions to perform won't save you - you're damned.

It doesn't have cache control headers.

It's missing the Content Security Policy. Content Security Policy protects you from XSS and nobody cares that there's no user input reflected on your page.

It's missing the X-XSS-Protection header. Although this header is generally deprecated among the browsers, some scanners and security consultants still advise you to implement it on all pages.

Sarcasm aside, while security headers like CSP are providing good additional protection for your website, they don't necessarily need to be present on every page, like in the innocent example above.

3. Tabnabbing

Gareth: Tabnabbing is so lame, it must have been constructed in an act of desperation. The basic idea is that you click on a link and a new tab opens on a legitimate website, then you browse for a while and the site that opened the legitimate site changes it to a phishing page using window.opener. I told you it was lame.

Reverse tabnabbing - OMG two types, I know. Works by abusing target=_blank by changing the URL of the page that opened the attacker-controlled site. The idea is to try to fool you into log in to the phishing site when you close the attacker-controlled page. Thankfully, browsers are going to end this pain for bug bounty triagers by setting window.opener to null for links with target=_blank by using noopener by default.

2. Missing httponly flag

James: Over the years, I've observed a peculiar phenomenon. When a security measure is as simple as setting an HTTP header, or cookie flag, it quickly attracts a cult-like fanbase of zealots who insist it must be used everywhere possible. They then reason that any site that fails to apply one of these measures must have terrible security.

The httponly cookie flag has just such a fanbase. Devised to mitigate XSS by stopping JavaScript being used to steal session cookies, it's near useless because cookie theft is such a noisy and impractical exploitation approach that attackers never bother with it anyway. Unfortunately, the fanbase doesn't know this, and also doesn't recognize session cookies, so you'd better apply it to every cookie or risk their wrath.

https://portswigger.net/research/web-storage-the-lesser-evil-for-session-tokens

This also might go some way to explaining the prevalence of useless CSP headers that can look quite intimidating until you spot the magic phrase 'script-src unsafe-inline'.

1. Autocomplete=off not set

James: This is the unanimous winner, let's break it down:

Conventional wisdom states using a password manager is the only way for mortals to use strong unique passwords

Auditors claim this should be discouraged and/or banned by setting autocomplete=off

Disagreeing may result in failure to obtain PCI compliance

Browser vendors disagree, so all major browsers deliberately ignore this setting

Some sites work around this by not using type=password, or disabling paste

The end result? Most sites waste effort on a setting everything ignores, and some actively make their security worse.

One more thing

At this point, some of you are probably considering pointing the finger at us, as Burp Suite's scanner reports many of these. This is a little more deliberate than you might expect. Relative to many of our competitors, we have an exceptionally skilled user base, and one of the ways we take advantage of this is by reporting behavior that /might/ be dangerous, and trusting our users' judgement rather than risking false negatives. Of course, if you asked us to name one example of this approach, we'd probably pick something sexier like Suspicious Input Transformation, which is untainted... for now.

https://portswigger.net/kb/issues/00400d00_suspicious-input-transformation-reflected

https://portswigger.net/research/backslash-powered-scanning-hunting-unknown-vulnerability-classes

This high-quality post was brought to you by the entire PortSwigger Research team.

Pen Testing

Bug Bounty

Research

Cyber Warfare

Back to all articles

Related Research

Document My Pentest: you hack, the AI writes it up!

23 April 2025

Document My Pentest: you hack, the AI writes it up!

Redefining Impossible: XSS without arbitrary JavaScript

23 September 2020

Redefining Impossible: XSS without arbitrary JavaScript
