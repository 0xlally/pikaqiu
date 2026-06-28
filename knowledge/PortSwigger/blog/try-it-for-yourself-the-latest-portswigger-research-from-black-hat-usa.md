# Try it for yourself: the latest PortSwigger Research from Black Hat USA

Source: https://portswigger.net/blog/try-it-for-yourself-the-latest-portswigger-research-from-black-hat-usa
Fetched: 2026-06-28T09:15:26.612210+00:00

Try it for yourself: the latest PortSwigger Research from Black Hat USA

Amelia Coen |

Friday, 23 August 2024 at 07:44 UTC

The modern web is constantly developing, with new potential vulnerabilities emerging all the time. Ensuring your web applications are secure in the face of this evolving threat is a constant challenge.

At Black Hat USA, the PortSwigger Research team debuted three groundbreaking research releases, addressing some of the biggest threats in web application security. These innovative findings are vital in helping AppSec teams stay up to date with the latest attack threats.

Here’s some examples of how you can apply this cutting-edge research in Burp Suite, and test your skills in our new Web Security Academy labs.

Use web timing attacks that actually work

All too often, web timing attacks are theoretical - useful only on paper, or in lab environments. This has understandably led many AppSec professionals to ignore them in their testing practices.

In Listen to the whispers: web timing attacks that actually work, James Kettle shows why AppSec professionals are missing a huge opportunity, proposing three novel attack techniques to transform your web timing attacks:

Discovering hidden attack surfaces.

Server-side injection vulnerabilities.

Misconfigured reverse proxies.

These cutting-edge techniques allow you to realise the potential of web timing attacks, ultimately helping you discover more potential attack surfaces.

Ready to try practical web timing attacks yourself? All three of these techniques are now available in James’ Param Miner extension. To try them out, make sure you have the extension installed, use a 'Detect scoped SSRF' scan to detect a reverse proxy, then you can run 'Exploit scoped SSRF' to find alternative routes to internal systems, and on each alternate route, run 'Guess parameters', cookies, or HTTP headers to find hidden attack surface.

Try these new techniques in James' latest CTF at listentothewhispers.net – see if you can crack it!

Secure potential email parsing discrepancies

Some websites parse email addresses to determine the email owner’s organization. While this process appears straightforward, it is actually very complex, meaning discrepancies can arise when different parts of the application handle email addresses differently.

In Splitting the email atom: exploiting parsers to bypass access controls, Gareth Heyes explores how attackers can abuse this trust in the domain part of the email address to bypass access controls and even gain RCE (Remote Code Execution).

To combat this threat, we have created a built-in payload wordlist in Intruder, which you can now use to fuzz for these kinds of attacks.

Ready to try it out? Test these new techniques in our brand new lab inside the Web Security Academy.

To access the wordlist in Burp Suite Professional, navigate to Intruder, and select the new payload list ‘Fuzzing - email splitting attacks’. Remember to add your payload processing rules over the placeholder values before running the list.

Protect your applications from web cache exploitation

In recent years, web cache attacks have become a popular way to steal sensitive data, deface websites, and deliver exploits. We've also seen parser inconsistencies causing critical vulnerabilities like HTTP Request Smuggling. This raises the question: what happens if we attack web caches using new path confusion variants?

In Gotta cache 'em all: bending the rules of web cache exploitation, Martin Doyhenard looks at how URL parsing discrepancies can be leveraged to obtain arbitrary web cache poisoning and deception using popular HTTP servers and CDNs with default configurations.

Thanks to Martin’s research, Burp Scanner now tests for web cache deception vulnerabilities without the need to delay your pentesting by writing an extension or conducting manual exploration.

Learn how to test for web cache deception vulnerabilities in our new Web Security Academy labs. Once you’ve completed the exercises, turn the theory into practice in Burp Suite Professional using Scanner and Repeater.

Using these techniques? Let us know what you think!

This groundbreaking research helps to drive innovation in Burp Suite, ensuring that our customers are equipped with the latest tools and techniques to detect critical vulnerabilities.

If you've started using any of the techniques above, share your success stories with us on X by tagging @PortSwiggerRes

Want to keep up to date with PortSwigger Research?

The PortSwigger Discord is the perfect place to keep up to date with the latest releases from the PortSwigger Research. There's also a few upcoming events from the PortSwigger Research team, including...

Gotta Cache 'em All, with Martin Doyhenard - Thursday August 29, 11am EST (4pm BST).

Ask Me Anything, with Chief Swig and Burp Suite creator Dafydd Stuttard - Tuesday September 3, 11am EST (4pm BST).

Join the official PortSwigger Discord today!

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
