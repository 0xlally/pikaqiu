# ViewState snooping

Source: https://portswigger.net/blog/viewstate-snooping
Fetched: 2026-06-28T09:15:27.626038+00:00

ViewState snooping

Dafydd Stuttard |

Wednesday, 13 June 2007 at 20:18 UTC

viewstate

burp

Pen Testing

I've been taking a look at the ASP.NET ViewState recently, and have done a (rather unscientific) survey of the way it is currently used on Internet-facing web applications. Here are a few statistics, based on a sample of more than 10,000 applications:

version 1.1 - 54%

version 2.0 - 46%

MAC-enabled (v1.1) - 93%

MAC-enabled (v2.0) - 89%

encrypted - 4%

average size - 16.8Kb

The largest ViewState I discovered was a whopping 3.8Mb in size, which appeared in a government web application displaying tables of statistics. Given that the ViewState is posted back to the server with each request, this application is seriously sluggish to use, even with a relatively fast connection.

I was surprised at the number of applications not using the EnableViewStateMac option, given that this is now set by default in ASP.NET. Without this option, the contents of the ViewState can be modified by the user, potentially affecting the application's processing in nefarious ways.

Even with EnableViewStateMac set, users can still decode and read the contents of the ViewState if it has not been encrypted. Application developers may use the ViewState to store arbitrary data, beyond the default serialisation of UI controls. I wonder how many attackers bother to decode and inspect the ViewState to check whether it contains anything of interest. The next version of Burp Suite will include a utility to deserialise and render the ViewState contents, to make this task trivial. A sneak preview is shown below:

viewstate

burp

Pen Testing

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
