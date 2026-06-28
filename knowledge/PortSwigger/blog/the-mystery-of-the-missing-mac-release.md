# The mystery of the missing Mac release

Source: https://portswigger.net/blog/the-mystery-of-the-missing-mac-release
Fetched: 2026-06-28T09:15:25.959471+00:00

The mystery of the missing Mac release

Dafydd Stuttard |

Thursday, 2 December 2021 at 16:23 UTC

Burp Suite

Sherlock Holmes

Some eagle-eyed users of Burp Suite have noticed that there is no Mac release of Burp Suite 2021.10.2.

Why is this release missing in action? Well, the true story is rather mundane, and unfortunate.

For a long time, Burp has been distributed via platform-specific installers. We finally got around to using the modern archive-based process on Macs, and 2021.10.2 was the first release to use this system.

As well as making up-front installation smoother, archive distributions work a bit differently when an update happens. Whereas an installer-based update replaces specific files within the application folder, an archive-based update replaces the whole folder and everything in it.

As it happened, the problem turned out to be really rather elementary. We hadn’t anticipated that some users were actually saving Burp project files within their application folder. This didn’t cause any problems when updates were installer-based, because only the relevant Burp files were updated. But when we changed to using archives … boom! The application folder and everything in it got replaced, including your project files.

Fortunately, this issue didn’t affect too many people, but when we heard about the problem we decided to immediately pull the Mac distribution of 2021.10.2 while we worked on a fix. The latest 2021.10.3 release goes back to being installer-based, checks for Burp project files within your application folder, and will refuse to update again if any project files are present. In future, we’ll switch back to an archive-based distribution on Macs.

So, with the mystery of the missing Mac release solved, we have a call to action for you. If you use a Mac and are in the habit of saving your project files within the application folder, now is the time to move these elsewhere.

Burp Suite

Sherlock Holmes

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
