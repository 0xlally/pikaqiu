# Cracking reCAPTCHA, Turbo Intruder style

Source: https://portswigger.net/research/cracking-recaptcha-turbo-intruder-style
Fetched: 2026-06-28T09:17:23.226155+00:00

Cracking reCAPTCHA, Turbo Intruder style

James Kettle

Director of Research

@albinowax

Published: Wednesday, 20 November 2019 at 14:59 UTC

Updated: Wednesday, 20 November 2019 at 15:33 UTC

Tired of proving you're not a robot? In this post, I'll show how you can partially bypass Google reCAPTCHA by using a new Turbo Intruder feature to trigger a race condition. This vulnerability was reported to Google 8 months ago but they declined to fix it, leaving the patching burden on individual websites. As a case study, I'll target Reddit.

Background

While researching HTTP Desync Attacks, I found I needed to send a group of HTTP requests within a tiny time window, to minimize the chance of someone else's request landing in the middle of my attack and interfering. I turned to Turbo Intruder, which uses a custom HTTP stack built from scratch with speed in mind. However, Turbo Intruder was originally designed for total request throughput (requests per second), rather than making requests arrive simultaneously.

Last-byte synchronization

To address this, I added support for last-byte synchronization, where Turbo first sends the whole of every request except the last byte, then, when they're all ready, 'releases' each request by sending the last byte. This helps minimize the effect of network congestion and latency on our attempt to get multiple requests processed simultaneously. I'm not sure who invented this technique - I first saw it years ago being used to improve timing attack accuracy - but it certainly works.

To use this feature, just add a 'gate' argument when queuing your requests, and then invoke engine.openGate when you're ready to send them

engine.queue(request, gate='race1')

engine.queue(request, gate='race1')

engine.openGate('race1')

For further details, check out the example script.

While developing this strategy I wrote a benchmark to ensure it was actually having the desired effect. This repeatedly sent a batch of five requests over consumer-grade broadband to a public website and measured how close together the first and second requests hit the server.

Using the basic five-thread approach caused an average difference of 2.7ms (0.0027 seconds). Ensuring every TCP connection was fully established before sending any requests reduced that window to 1.4ms, and the last-byte technique squeezed it to a tiny 0.7ms - making it roughly twice as effective at triggering race conditions.

I also added support for per-chunk callbacks, for when you have a race condition that requires reading information from the server mid-attack like in LFI with PHPInfo Assistance.

Racing reCAPTCHA

Shortly after this, I was asked to do a security audit of PortSwigger's self-registration feature, which we were introducing just ahead of the Web Security Academy launch.

Users are supposed to be limited to registering one account per email address, which makes registration a potential target for a Time-of-check Time-of-use (TOCTOU) exploit. But there was a catch - the form was protected with reCAPTCHA, and everyone knows you can only use a valid reCAPTCHA solution once, right? Well, I tried anyway and it turned out you can use it a few times if you go fast enough.

This is particularly surprising thanks to the design of reCAPTCHA, where users don't directly connect to the server that validates the solution token. When you perform this attack, you're actually forcing the target website to trigger the race condition on your behalf:

Turbo Intruder <-> Target Website <-> Google reCAPTCHA

I considered giving this a fancy label like 'second order race condition'. However, in this age of reverse proxies and load-balancer chains most race conditions are 'second order' to some extent.

Uncoordinated Disclosure

After finding the vulnerability, we immediately deployed a workaround to patch it on our website and reported the issue to Google, with a proof of concept showing the Target Website <-> Google reCAPTCHA race condition. In the past I've had numerous great experiences with Google's security team, but this time was fated to be different.

Google requested a video, and when asked why the proof of concept wasn't sufficient replied "Please share a video Poc as we need the same while contacting the relevant team."

This wasn't a great sign, but I eventually provided a video, and restated that I found this vulnerability on a live website. Google then politely declared the issue was imaginary, saying they "don't think this attack is plausible in the wild" due to "latency between the 3rd party server, the attacker and us, while also taking into account the 3rd party's server's workload and concurrency".

Rather than waste further time and energy arguing with Google about a moderate severity finding, I opted for public disclosure. This vulnerability affects almost all websites using reCAPTCHA - for my example target I chose Reddit as it's a well known target for spammers, and the account-registration process is reCAPTCHA protected. Reddit kindly agreed I could publish a video of the attack in action:

Video tags are not supported by your browser.

The obvious impact is that you can now register three times as many spam accounts for each solved captcha, potentially tripling your spam-rate. This could easily be chained with mechanical turk style services.

The second, more interesting implication is that on other sites this may enable exploitation of race conditions in thread-unsafe code that's protected by reCAPTCHA - for example, posting reviews or voting.

Hopefully this post will help persuade someone at Google that this attack is actually plausible, and should be fixed. Till then, if you're using reCAPTCHA, you'll need to manually secure it by locking/synchronising on the g-recaptcha-response token. Depending on your own application architecture this may be impossible, and you'll have to wait for Google to fix it.

race condition

turbo intruder

Back to all articles

Related Research

Introducing HTTP Anomaly Rank

11 November 2025

Introducing HTTP Anomaly Rank

WebSocket Turbo Intruder: Unearthing the WebSocket Goldmine

17 September 2025

WebSocket Turbo Intruder: Unearthing the WebSocket Goldmine

The single-packet attack: making remote race-conditions 'local'

18 October 2023

The single-packet attack: making remote race-conditions 'local'

How to build custom scanners for web security research automation

03 October 2023

How to build custom scanners for web security research automation
