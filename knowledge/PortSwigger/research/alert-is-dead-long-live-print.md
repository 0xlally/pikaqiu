# alert() is dead, long live print()

Source: https://portswigger.net/research/alert-is-dead-long-live-print
Fetched: 2026-06-28T09:17:20.471159+00:00

alert() is dead, long live print()

James Kettle

Director of Research

@albinowax

Published: Friday, 2 July 2021 at 13:27 UTC

Updated: Monday, 5 July 2021 at 10:03 UTC

Cross-Site Scripting and the alert() function have gone hand in hand for decades. Want to prove you can execute arbitrary JavaScript? Pop an alert. Want to find an XSS vulnerability the lazy way? Inject alert()-invoking payloads everywhere and see if anything pops up.

However, there's trouble brewing on the horizon. Malicious adverts have been abusing our beloved alert to distract and social engineer visitors from inside their iframe. Google Chrome has decided to tackle this by disabling alert for cross-domain iframes. Cross-domain iframes are often built into websites deliberately, and are also a near-essential component of certain relatively advanced XSS attacks.

Once Chrome 92 lands on 20th July 2021, XSS vulnerabilities inside cross-domain iframes will:

No longer enable alert-based PoCs.

Be invisible to anyone using alert-based detection techniques.

What next? The obvious workaround is to use prompt or confirm, but unfortunately Chrome's mitigation blocks all dialogs. Triggering a DNS pingback to a listener, OAST-style is another potential approach, but less suitable as a PoC due to the config requirements. We also ruled out console.log() as console functions are often proxied or disabled by JavaScript obfuscators.

It's quite funny that this "protection" against showing dialogs cross domain blocks alerts and prompts but as Yosuke Hasegawa pointed out they forgot about basic authentication. This works in the current version of canary. It's likely to be blocked in future though.

We needed an alert-alternative that was:

Simple, setup-free and easy to remember

Highly visible, even when executed in an invisible iframe

After weeks of intensive research, we're thrilled to bring you...

print()

We will be updating our Web Security Academy labs to support print() based solutions shortly. The XSS cheat sheet will also be updated to reflect the new print() payloads when using cross domain iframes. We'll keep using alert when there's no iframes involved... for now.

Long live print!

- Gareth & James

XSS

Back to all articles

Related Research

Cookie Chaos: How to bypass __Host and __Secure cookie prefixes

03 September 2025

Cookie Chaos: How to bypass __Host and __Secure cookie prefixes

Stealing HttpOnly cookies with the cookie sandwich technique

22 January 2025

Stealing HttpOnly cookies with the cookie sandwich technique

Bypassing WAFs with the phantom $Version cookie

04 December 2024

Bypassing WAFs with the phantom $Version cookie

Concealing payloads in URL credentials

23 October 2024

Concealing payloads in URL credentials
