# [MoBP] Improved memory handling

Source: https://portswigger.net/blog/mobp-improved-memory-handling
Fetched: 2026-06-28T09:15:20.227336+00:00

[MoBP] Improved memory handling

Dafydd Stuttard |

Friday, 28 November 2008 at 07:37 UTC

MoBP

memory

burp

A significant implementation challenge in the creation of software like Burp concerns efficient memory handling, and resilience in the face of low memory conditions. As the software becomes more functional, this challenge grows in importance.

If you use Burp in anger for a few hours, it will typically generate thousands of HTTP requests and responses, and sometimes many times more. Keeping track of this raw data, and the associated information that is analysed from it, requires a huge amount of storage. The current release of Burp already makes extensive use of temporary files for persisting raw HTTP messages, and in-memory structures are designed to be as lean and non-duplicative as possible. However, the new release grows up a little in its memory handling, providing you with feedback about actual or potential memory problems, and recovering from memory allocation failures wherever possible.

If you start Burp by double-clicking the JAR file, the Java runtime will allocate a relatively modest memory heap, which is usually way smaller than your computer is capable of supporting. In future, Burp will alert you of this fact, and remind you of the command line switches which you can use to allocate a larger heap:

As well as encouraging you to use more memory in the first place, Burp also alerts you to any memory problems that arise at runtime, enabling you to save* your work while you are still able to:

Now, you might suppose that memory allocation failures are a pretty fatal condition, indicating an imminent crash or loss of functionality. But they needn't be. Many web applications include a few downloadable resources that are huge relative to a typical response - things like flash movies, ZIP archives, office documents, etc. If you cause Burp to request and process these (for example, by requesting them via the proxy, or spidering them), then Burp will ask the Java runtime for large amounts of memory. If you do this enough in close succession, then the runtime will start to reject these requests. When this happens, Burp's handling of the affected item will obviously fail. But other, more modestly sized, memory requests will normally succeed, and so other items can still be processed as normal. In the new release, Burp is much more defensive in catching failed memory allocations, keeping alive the affected thread to see another day. Whereas in the past, a critical component like the proxy request queue might have crashed on memory failure, leaving behind only a command line stack trace, in future only individual requests will be lost, triggering an alert that memory is low, and allowing you to take appropriate action.

*See tomorrow's post.

MoBP

memory

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
