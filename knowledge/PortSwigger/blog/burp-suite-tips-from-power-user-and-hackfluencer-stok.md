# Burp Suite tips from power user and "hackfluencer" Stök

Source: https://portswigger.net/blog/burp-suite-tips-from-power-user-and-hackfluencer-stok
Fetched: 2026-06-28T09:15:11.983981+00:00

Burp Suite tips from power user and "hackfluencer" Stök

Emma Stocks |

Tuesday, 29 September 2020 at 14:29 UTC

Interviews

In his own words, Stök is "that hacker that your friends told you about". In other words, he's a content creator with over 25 years of experience in the IT industry. He creates education, tutorial, and review videos, to help other people learn and develop their skills in bug bounty hunting and infosec more generally. Since he proudly (and frequently) describes himself as a "Burp Suite fanboy", we decided it was about time we got in touch.

When did you first come across Burp Suite?

Stök states that as a frequent user of BackTrack aka Kali Linux, he encountered Burp Suite fairly early on as this distribution ships with our Burp Suite Community Edition. He says that he remembers the product due mainly to the name, Burp, which he claimed stood out as "sounding funny" among so many other softwares with bland-sounding names.

"To be honest [though], I really never used it. Web wasn't my game back then."

The beginning of a Burp Suite adventure

Picture the scene. It's a warm, calm night in Goa (India). Famed for its kaleidoscopic blend of cultures, it marks the perfect location for one man to have his whole world turned around.

Stök was sitting with Frans Rosén in his hotel room, editing videos for his highly successful YouTube channel, when he got chatting with Jobert Abma, one of the founders of HackerOne. Jobert showed him through a few basics of web application pentesting, and demonstrated how he used Burp Suite to hack the web. He discovered the site map, how to set a target, Burp Intruder, and Burp Repeater. Stök said that on that day, his life changed.

"It was love at first sight, and I've used Burp Suite almost daily ever since."

After getting up to speed with Burp Suite and the various functionalities of the product, Stök wanted to try his hand at his very first bug bounty adventure. He selected Race Conditions as his vulnerability of choice, and due to requiring a fully functional iteration of Burp Intruder, realized that Burp Suite Community Edition was never in scope for him. He set himself up with a Burp Suite Professional license and, a few weeks later, received his first bounty - a race condition.

Top tips from a Burp Suite power user

As someone who learned Burp Suite from scratch, without the support of coming from a web-based background, we wanted to ask Stök what his top tips would be for any beginners looking to get a head start. He shared a few different things that have helped him out along the way.

1. Stök describes hosting his own instance of Burp Collaborator as "winning in so many ways". He has encountered numerous situations where he's been able to exfiltrate using his own domain, but not going through the main collaborator domain as that is often blocked by the target.

2. He's all about the hotkey commands. His personal favorite is "CTRL + R = Send to Repeater".

3. Keen to make sure he's in control of what he's doing with Burp Suite, he recommends disabling interception from the user options menu on startup.

4. When it comes to Burp Repeater, he advises that you don't need 40,000 tabs open at once. He suggests simply naming the tab for what you're doing and using the back and forward buttons, as all of your requests are stored within the drop down list.

5. If you want to use Burp Intruder to test for a race condition vulnerability, use "null payloads" to send the same request repeatedly.

6. He suggests that when using the "search" function to highlight things of interest, combine this with stepping through requests inside tools like flow and logger++. He claims that users also get "extra points" for checking the "regex" box, and searching using regex!

7. Stök describes the "generate CSRF POC" as "awesome", stating that it's a very useful (and very lazy!) way of creating POCs with autosubmit to demonstrate impact, and definitely not just for CSRF.

Working with Burp Suite

Since Stök works with Burp Suite Professional on an almost daily basis, we were interested to find out what his most-loved tools within the product are. His winning combination is Burp Collaborator, Burp Repeater, and Burp Intruder. He also finds the BApp store incredibly useful.

Any extension that makes my life easier and notifies me on things that I might miss is priceless to me.

He has a selection of frequently used BApp extensions, these are as follows:

• Burp Bounty Pro

• HUNT Scanner Redux

• Taborator

• Turbo intruder

• Flow

• Logger++

• Autorize

• Auto repeater

• Upload Scanner

Burp Suite and bug bounties

After his initial success netting a race condition bounty, Stök spent some time working with Burp Suite to really fine tune his bug bounty hunting toolkit. Initially, he passively logs things that he has interest in, then uses Burp's extensive tooling library to add custom templates to items of major interest.

His deep-seated interest in blind out-of-band vulnerabilities means that hosting his own instance of Burp Collaborator is crucial. He also uses a number of BApp extensions, including Turbo Intruder to race things, Taborator for all of his Burp Collaborator requests, and Autorize to identify insecure direct object references (IDORs).

In his usual manner, Stök states that he has been both lucky and blessed to find a number of XML external entity (XXE) injection vulnerabilities, along with some serious information disclosures on multiple targets and programs. He's unable to disclose any of the targets, but freely admits that he could never have found and exploited the vulnerabilities without Burp Suite.

Final words of advice

We asked Stök for the one piece of advice he'd give to new Burp Suite users, looking to get into bug bounty hunting. His response?

Like anything else in life, the more you practice the better you will become.

Wise words indeed, and ones that we couldn't agree with more ourselves. He also suggested that anybody new to the field would be foolish not to try out the Web Security Academy - his words not ours!

Interviews

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
