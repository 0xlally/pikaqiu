# onwebkitplaybacktargetavailabilitychanged?! New exotic events in the XSS cheat sheet

Source: https://portswigger.net/research/new-exotic-events-in-the-xss-cheat-sheet
Fetched: 2026-06-28T09:17:27.513383+00:00

onwebkitplaybacktargetavailabilitychanged?! New exotic events in the XSS cheat sheet

Gareth Heyes

Researcher

@garethheyes

Published: Tuesday, 11 June 2024 at 14:58 UTC

Updated: Tuesday, 11 June 2024 at 14:58 UTC

The power of our

XSS cheat sheet

is we get fantastic contributions from the web security community and this update is no exception. We had valuable contributions from Mozilla to remove events that no longer work with the marquee tag on Firefox.

There was a wonderfully obscure Safari only vector that used the event

onwebkitplaybacktargetavailabilitychanged

from

@amirmsafari

that works on audio and video tags:

We had a submission from

@Wcraft-log

with the

onpointercancel

event that requires heavy user interaction:

<xss onpointercancel=alert(1)>XSS</xss>

@Filipnyquist

pointed out that we didn't document that pretty much every element can now use the

autofocus attribute. This was discovered earlier by

@RenwaX23

and

@lbherrera_

.

<xss onfocus=alert(1) autofocus tabindex=1>

Finally we had a submission from

@zhenwarx

that showed there are a bunch of webkit events we missed that require user interaction with the trackpad.

<xss onwebkitmouseforceup=alert(1)>XSS</xss>

<xss onwebkitmouseforcewillbegin=alert(1)>XSS</xss>

<xss onwebkitmouseforceup=alert(1)>XSS</xss>

<xss onwebkitmouseforcedown=alert(1)>XSS</xss>

<xss onwebkitmouseforcechanged=alert(1)>XSS</xss>

Big thanks to the web security community for keeping the

XSS cheat sheet

up to date with the latest XSS vectors. If you would like to contribute please

raise an issue

or a

PR

.

Note: If you are wondering what we use to generate code snippet images. We use the excellent online tool

Ray.so

.

Back to all articles

Related Research

05 February 2026

06 January 2026

The Fragile Lock:

Novel Bypasses For SAML Authentication

10 December 2025

The Fragile Lock:

Novel Bypasses For SAML Authentication

Introducing HTTP Anomaly Rank

11 November 2025

Introducing HTTP Anomaly Rank
