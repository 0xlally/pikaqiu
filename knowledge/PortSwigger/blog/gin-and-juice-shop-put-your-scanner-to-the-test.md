# Gin and Juice Shop: put your scanner to the test

Source: https://portswigger.net/blog/gin-and-juice-shop-put-your-scanner-to-the-test
Fetched: 2026-06-28T09:15:15.577538+00:00

Gin and Juice Shop: put your scanner to the test

Matt Atkinson |

Monday, 16 May 2022 at 13:44 UTC

"Word". We heard that a lot of you have been having problems finding a truly dope vulnerable web application to wave your scanner at. As makers of the web's OG vulnerability scanner, we couldn't be letting that sorta situation stand.

So, Carlos Montoya has been busy - and he's got himself a shop. A Gin and Juice Shop, to be precise. And we want you to knock it over.

Montoya has outdone himself this time.

As you can see, Carlos has done a pretty good job of the design here, fo-shizzle. His site is filled with the sort of features you'd expect nowadays - like single-use CSRF tokens, plenty of JavaScript and the like. And what that means is, unlike a lot of other deliberately vulnerable websites, Gin and Juice Shop provides a realistic challenge for a scanner to navigate, for real.

Look at these jokers.

Naturally, Carlos being Carlos, Gin and Juice Shop is also riddled with serious vulnerabilities. You'll find everything from classics like XSS and SQLi, to tricky external service interactions (using OAST testing).

The easiest way to find this stuff is to fire up a scanner. And Burp Scanner, being the OG that it is, will rip through sites like this.

Burp Scanner (seen here in Burp Suite Professional) will find a whole bunch of vulnerabilities in Gin and Juice Shop, for real.

You can find Burp Scanner in either Burp Suite Professional or Burp Suite Enterprise Edition - just paste in the URL https://ginandjuice.shop/ , pour yourself a drink, and off you go.

If you're new to Burp Scanner, then check out our guides, below. Now go get scanning - and don't forget to let us know what you think. Peace.

Burp Scanner guides

Running your first scan with Burp Suite Professional.

Running your first scan with Burp Suite Enterprise Edition.

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
