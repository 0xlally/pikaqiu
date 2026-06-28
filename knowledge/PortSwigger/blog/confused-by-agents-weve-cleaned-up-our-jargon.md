# Confused by agents? We've cleaned up our jargon ...

Source: https://portswigger.net/blog/confused-by-agents-weve-cleaned-up-our-jargon
Fetched: 2026-06-28T09:15:14.472684+00:00

Confused by agents? We've cleaned up our jargon ...

Matt Atkinson |

Wednesday, 27 April 2022 at 14:47 UTC

Enterprise Edition

Speaking to Burp Suite Enterprise Edition users, one thing has come up time and time again as a blocker to your understanding of the product. This has been our use of the term "agent" when describing the components that allow Enterprise Edition to scale and to carry out multiple scans concurrently.

Now that the term "agents" is no more, we'll be making an effort to use language more literally when talking about Burp Suite Enterprise Edition's scalability.

Our scans are designed to be easy to use. They allow for greater flexibility than most automated vulnerability scanners - because with Burp Suite Enterprise Edition you can reassign your scans to any websites, applications, or URLs you see fit. So it's ironic that we chose (what is in hindsight) some overly complex terminology to describe this.

This post is both an admission of the Homer Simpson "d'oh" moment we had when we realized the scale of the problem with the language we were using, and an apology to anyone we've inadvertently confused along the way. It should also serve as a cautionary tale for anyone who ever gets tasked with thinking up names for product features …

How to kill a word

One big problem with the "A word" was that we were using it to describe a number of different things. "Agent" could refer to one of the logical entities tasked with performing Enterprise Edition scans - but also an "agent machine" - the machine on which the scans actually run. Then there was the software installed on the "agent machine", allowing the agent entities to operate. In short, our terminology was a bit of a mess.

We've now banished the term "agent" from just about everywhere we can think of. The change has taken in the entire Burp Suite Enterprise Edition user interface, our whole website, and all associated product documentation. You should now only encounter the "A word" in any previously existing license details, or in the Enterprise Edition API (which we'll be revisiting in due course).

New terminology

Now that the term "agents" is no more, we'll be making an effort to use language more literally when talking about Burp Suite Enterprise Edition's scalability. Expect to hear us using terms like "concurrent scans" and "scanning machines" - terms which are hopefully self explanatory.

And of course, because we keep things simple, if you'd like to increase the concurrent scan limit of your existing Burp Suite Enterprise Edition license, then you can do so from your PortSwigger user account.

Enterprise Edition

Matt Atkinson

@mattatkinson42

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
