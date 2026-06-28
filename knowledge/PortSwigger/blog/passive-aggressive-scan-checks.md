# Passive-aggressive scan checks

Source: https://portswigger.net/blog/passive-aggressive-scan-checks
Fetched: 2026-06-28T09:15:22.605598+00:00

Passive-aggressive scan checks

Tom Shelton-Lefley |

Friday, 1 April 2022 at 08:00 UTC

Burp Suite

Here at PortSwigger, our goal is to enable the world to secure the web. Our scanner sits at the core of this value - quickly surfacing issues and vulnerabilities that may be present in a web application.

However, lately we’ve become concerned that some discovered issues aren’t being taken seriously enough, particularly those found whilst passively browsing. Although these passive vulnerabilities aren’t as juicy as your RCEs or your SSRFs, we can’t sleep soundly at night until we know they’re all fixed.

To this end, we put our heads together on the scanner team and came up with a few ideas:

What if we increase the font size for the advisories of passive issues? Too small …

How about we randomly delete a system file every time a passive issue is found? Too big …

Could we make Burp Suite actually burp in the presence of passive issues? It’s been done before …

When we spoke to our marketing folks, they made it very clear that we’re not allowed to be straight up hostile with our users. In fact, they couldn’t stress this enough.. back to the drawing board again. Then it hit us: what if there’s a way to really push users towards fixing these vulnerabilities without them (or marketing) realizing that’s what we are doing.

With all of this in mind; I’m pleased to announce that, as of today, all passive checks detected by Burp Scanner will be replaced with passive-aggressive checks! Here’s a sneak preview:

Old passive checkNew passive-aggressive check

Cleartext submission of passwordSending passwords over plaintext HTTP - what could possibly go wrong?

Long redirection responseIt’s really up to you if you want to return data no-one can see.

Duplicate cookies setSetting this cookie once is probably enough isn’t it?

Vulnerable JavaScript dependencyShould you really still be using that JavaScript dependency?

Session token in URLIs the URL definitely the best place to put your session tokens?

Password returned in URL queryDidn’t you learn from the session token?

Social security numbers disclosedYou wouldn’t want someone to hack your HTML source code and find these would you?

Email addresses disclosedEveryone loves receiving spam emails. You might be helping!

Private key disclosedDefine: Private. "belonging to or for the use of one particular person or group of people only."

Content type incorrectly statedThat content type doesn’t look quite right, does it?

Unencrypted communicationshttps://letmegooglethat.com/?q=letsencrypt

We really hope our users enjoy this new update and that it encourages remediation of these important issues. It should hit Burp Suite's Stable release channel by midday today: April 1st.

Burp Suite

Tom Shelton-Lefley

@TomLefley

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
