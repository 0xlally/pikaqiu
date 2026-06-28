# Intruder bugfix - nonstandard charsets

Source: https://portswigger.net/blog/intruder-bugfix-nonstandard-charsets
Fetched: 2026-06-28T09:15:18.978736+00:00

Intruder bugfix - nonstandard charsets

Dafydd Stuttard |

Saturday, 15 September 2007 at 09:42 UTC

burp

Just to placate the salivating hordes who accost me on a daily basis demanding to know when the next release of burp will be available, here is some more evidence that I'm not bluffing and work is actually well underway on the new release.

One annoying bug in Intruder is that the payload positioning marker doesn't work when the JRE is set to use some unusual character sets. Instead of the § character, the payload marker appears as a red box or some other character altogether, which doesn't get recognised when you try to launch an attack. This affected Japanese, some Linux users and other subversives whose character set wasn't set to en-US:

Well, the good news is that this has been fixed in the next release. I'd be most grateful if anyone who experienced this problem could try it out and let me know whether it works for you. If this bug didn't affect you, don't bother with the download as it contains nothing else that differs from the current release version.

burp

Dafydd Stuttard

@DafyddStuttard

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
