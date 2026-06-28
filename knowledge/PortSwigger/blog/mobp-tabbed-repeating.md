# [MoBP] Tabbed repeating

Source: https://portswigger.net/blog/mobp-tabbed-repeating
Fetched: 2026-06-28T09:15:21.033699+00:00

[MoBP] Tabbed repeating

Dafydd Stuttard |

Saturday, 8 November 2008 at 10:13 UTC

MoBP

burp

Now that every browser has jumped on the tabs bandwaggon, it was about time that Burp caught up.

Burp Repeater was always intended to be a very simple tool for performing manual attacks, providing the facility to reissue a single request over and over, manually editing its contents, and keeping a history of the requests made and responses received. And in most situations, this is all that a skilled hacker needs to fine-tune a manual attack.

Occasionally, however, being restricted to a single request window and history is an annoying limitation. Sometimes, your attack involves more than one step, and you need to issue multiple manual requests in sequence. Other times, you need to submit a payload in one request, then issue a different request to establish its impact. Trying to manage two manual requests in the same repeater window, constantly clicking backwards and forwards through the history, is a real pain.

Enter tabbed repeating. In the new version, when you send a request to Repeater from another tool, that request gets its own tab. Each tab has its own request and response windows, and its own history. You can rename tabs to help you keep track of what is where. And you can manually add new tabs or delete old ones, as required. Other than the tabs, Repeater is unchanged:

MoBP

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
