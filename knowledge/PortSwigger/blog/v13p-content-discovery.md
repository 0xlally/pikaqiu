# [V13P] Content discovery

Source: https://portswigger.net/blog/v13p-content-discovery
Fetched: 2026-06-28T09:15:26.929280+00:00

[V13P] Content discovery

Dafydd Stuttard |

Monday, 23 November 2009 at 09:49 UTC

V13P

Burp now includes a content discovery function, similar in concept to OWASP's DirtBuster. You can access this feature by selecting a request or URL anywhere within Burp, and using the context menu to start content discovery.

Burp uses various techniques to discover content, including name guessing, web spidering, and extrapolation from naming conventions observed in use within the application. The feature is highly configurable, as shown by the available options which are explained below:

Target - These options control which directory to begin discovery from. Only items within this path and its subdirectories will be requested during the session. You can choose to discover files or directories or both, and how deep to recurse into discovered subdirectories.

Test case generation - These options control which file and directory names Burp will use when making requests to discover content. As well as built-in lists, Burp can harvest names used elsewhere within an application, and retry them at other locations, and can construct names based on discovered items, for example by cycling values in filenames containing numbers.

File extensions - You can specify a list of file extensions with which to test each possible filename. Burp can harvest file extensions observed in use within the application, and test these with every filename. When a file has been confirmed, Burp can also try a specific list of variant extensions with that filename, for example to check for old or backup versions of the same file.

Discovery engine - You can control how many threads are used for content discovery and spidering, whether file names are handled case sensitively, and how the discovery session interacts with Burp's main site map (in the target tab of the suite).

When you have configured your discovery session, you can start it from the control tab, which also provides runtime information about the actions being performed. The work is divided into numerous discrete tasks, which are prioritised according to their likelihood of quickly discovering new content, and new tasks are generated recursively as content is confirmed:

The discovery session employs its own site map, showing all of the content which has been discovered within the defined scope. If you have configured Burp to do so, newly discovered items will also be added to Burp's main site map.

V13P

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
