# Burp problems after Windows update

Source: https://portswigger.net/blog/burp-problems-after-windows-update
Fetched: 2026-06-28T09:15:08.961134+00:00

Burp problems after Windows update

Dafydd Stuttard |

Thursday, 9 April 2009 at 20:18 UTC

Windows

burp

If you use Windows, you may have encountered a problem following March's security update, in that Burp Proxy listeners running on the loopback interface stopped working. This was caused by Microsoft changing the "localhost" entry in the Windows hosts file from:

127.0.0.1 localhost

to:

::1 localhost

Manually reverting to the old entry fixes the problem for a while, but Windows will silently update to the new entry periodically. (Note that if you are running Windows Defender, you may need to dismiss some alerts in order to modify your hosts file.)

The latest versions of Burp (both free and Pro editions) have been updated to work with the new hosts entry. If you were having problems, please download the latest release and things should start working again.

Windows

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
