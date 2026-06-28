# Breaking the chains on HTTP Request Smuggler

Source: https://portswigger.net/research/breaking-the-chains-on-http-request-smuggler
Fetched: 2026-06-28T09:17:21.165588+00:00

Breaking the chains on HTTP Request Smuggler

James Kettle

Director of Research

@albinowax

Published: Monday, 9 December 2019 at 13:53 UTC

Updated: Tuesday, 22 September 2020 at 14:45 UTC

We've all seen it - a conference presentation drops a fancy new technique, and a hot new tool is released. Then over the following months and years, the environment changes and the tool is left unmaintained until it's pretty much useless. I'm not going to let that happen to HTTP Request Smuggler, and today I'm pleased to provide further info on a major update released last week. This post will describe the key changes.

Unlocking improved accuracy

One of the major innovations in HTTP Request Smuggler is the timing-based scanning technique, which can detect potential HTTP Request Smuggling vulnerabilities with almost zero chance of false negatives. It's always had a few false-positives, but the overall false-positive rate has mostly been so low it hasn't really been a problem. However, since my research on request smuggling was publicly released, a good proportion of vulnerable websites have now patched their systems. The decrease in the number of vulnerable systems has raised the tool's the false-positive rate to annoying levels. That said, less vulnerable sites also means less potential for accidental damage...

As such, I've decided it's time to release a feature which I coded back in January to help with my research, but decided to withhold from HTTP Request Smuggler's initial public release due to its potential to cause widespread accidental damage.

This feature is the ability to automatically attempt the often non-deterministic and occasionally risky 'confirmation' stage of a request smuggling attack, rather than requiring user-interaction to launch it. As of this release, if you enable the poc:  options then when HTTP Request Smuggler thinks a target is vulnerable, it will attempt the confirmation stage and report a second issue titled HTTP Request Smuggling Confirmed if it works. If you're scanning at scale and don't have time to spend investigating findings that might be false positives, just focus on the confirmed findings. As ever, please remember the confirmation technique is unreliable, and prone to false negatives on high traffic websites - so unconfirmed findings may still be interesting.

Detecting ATS

Over the last few months, amid a deluge of emails asking me for help exploiting specific systems (please, no more), I received some genuinely insightful ideas and suggestions. This became the basis for a number of new features.

As I mentioned earlier, the real strength of the timing technique is the lack of false negatives. However, Erlend Oftedal discovered an exception - unpatched Apache Traffic Server (ATS) goes undetected. It turned out this server is internally inconsistent about whether it should prioritise content-length or chunked encoding, rendering it impossible to apply any sensible logic to whether it's actually vulnerable. The only way to detect servers with this behaviour is to simply attempt a proof of concept attack and see if it works. As such, I've added the 'skip straight to poc' option which will do that. Please note that there's a reason this isn't the default strategy - it's simply unreliable so you can expect to see a lot of false positives and negatives too. Mercifully, after a lot of scanning it appears that ATS is unique in its ability to dodge the timing-based detection strategy.

Improving payload resilience

Erlend also spotted another opportunity to improve HTTP Request Smuggler's coverage - StackOverflow contains some reports of servers 'dechunking' small requests, which could potentially break a viable desync attack. To address this, I've added the 'pad everything' option which pads all probe requests out to over 40kb.

Émile Fugulin was poking through gnunicorn's source code looking to patch a reported request smuggling vulnerability, when he spotted a new one, thanks to the following line analysing the Transfer-Encoding header:

chunked = value.lower() == "chunked"

Unfortunately, the specification supports multiple transfer-encodings, separated by commas:

The Transfer-Encoding header field lists the transfer coding names corresponding to the sequence of transfer codings – RFC 7230 #3.3.1

HTTP Request Smuggler was already taking advantage of this with the following payloads:

Transfer-Encoding: cow, chunked

Transfer-Encoding: chunked, cow

but Émile noticed some front-ends were filtering unrecognised encodings, and suggested an alternative approach using the completely legitimate (per RFC 2616) and often-whitelisted encoding 'identity':

Transfer-Encoding: identity, chunked

Update: Check out Émile's in-depth writeup on this finding for the full details.

This update should help keep the tool sailing smoothly for the time being. As ever, if you have any ideas for new desync methods, I highly recommend either trying them out yourself or sending me an email.

research tools

Request Smuggling

Back to all articles

Related Research

How to distinguish HTTP pipelining from request smuggling

19 August 2025

How to distinguish HTTP pipelining from request smuggling

06 August 2025

Repeater Strike: manual testing, amplified

15 July 2025

Repeater Strike: manual testing, amplified

Introducing SignSaboteur: forge signed web tokens with ease

22 May 2024

Introducing SignSaboteur: forge signed web tokens with ease
