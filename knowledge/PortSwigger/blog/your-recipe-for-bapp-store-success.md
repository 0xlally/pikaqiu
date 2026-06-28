# Your recipe for BApp Store success

Source: https://portswigger.net/blog/your-recipe-for-bapp-store-success
Fetched: 2026-06-28T09:15:28.846756+00:00

Your recipe for BApp Store success

Paul Johnston |

Wednesday, 17 January 2018 at 14:42 UTC

BAppStore

burp extender

After using Burp’s Extender API to adapt Burp to fulfill their needs, some users choose to share their creations with the community by submitting them to the BApp Store. In this post, we’ll share some advice to help you maximize your extension’s success by turning it into a high-quality BApp that users will love.

1) Perform a novel function

The BApp store already has a lot of extensions and it’s easy to accidentally duplicate a different extension’s features, or even a core Burp feature. To maximize your chances of BApp store acceptance, ensure you implement a novel idea or at least have a good idea what sets your extension apart from its competitors. If not, you might be better off tailoring an existing Bapp to suit your purposes - they’re all open source after all.

That said, extensions range from a few dozen lines of code to several thousand. They don't need to be large or sophisticated to be invaluable! Some of our favorite extensions are under a hundred lines.

2) Have a clear descriptive name

When a user scrolls through the BApp Store, they will be drawn to extensions that solve issues they are encountering. To capture attention, the name needs to clearly describe what the extension does. While playful names like 'PsychoPATH' have been used in the past, we now encourage names to be descriptive. You can also provide a one-line summary that appears in the list (web only), as well as a more detailed description.

3) Operate securely

Users may be testing sites that they don't trust, so it's important that extensions don't expose users to attack. Treat the content of HTTP messages as untrusted. Some submissions have contained flaws like XXE that a malicious site could attack. Extensions should operate securely in expected usage, for example, an extension like 'Copy as Python Requests' needs to avoid code injection. Data entered by a user into the GUI can generally be trusted, but if there is autofill from untrusted sources, don't assume the user will check the contents.

4) Include all dependencies

A major benefit of the BApp Store is one click installation. If your extension includes all dependencies, it is much easier for users to get started. Doing this also avoids version mismatches - where an underlying tool is upgraded, but the BApp is not.

5) Use threads to maintain responsiveness

A common mistake is performing slow operations - such as HTTP requests - in the Swing Event Dispatch Thread. This causes Burp to appear unresponsive, as the whole GUI must wait until the slow operation completes.To maintain responsiveness, perform slow operations in a background thread. In addition, avoid slow operations in processProxyMessage and processHttpMessage. To avoid concurrency issues, protect shared data structures with locks, and take care to avoid deadlocks. Be aware that Burp does not catch and report exceptions in background threads. To report background exceptions, surround the full thread operation with a try/catch block and write any stack traces to the extension error stream.

6) Unload cleanly

When an extension unloads, it needs to release all resources. Burp resources, like ITab or IContextMenuFactory are released automatically. However, other resources may not be. If such resources are created, the extension needs to implement IExtensionStateListener. The most common example is background threads; it is important that background threads are terminated in extensionUnloaded.

7) Use Burp networking

When making an HTTP request - to the target, or otherwise - it's preferable to use Burp's makeHttpRequest, instead of libraries like java.net.URL. This sends the request through the Burp core, so settings like upstream proxies and session handling rules will be obeyed. Many users are on a corporate network that only allows Internet access through a proxy. In addition, avoid performing any communication to the target from within doPassiveScan.

8) Support offline working

Some Burp users need to operate from high-security networks without Internet access. To support these users, extensions that contact an online service to receive vulnerability definitions or other data should include a copy of recent definitions, as a fallback for disconnected networks.

9) Cope with large projects

Some users work with very large projects. To support such users, avoid keeping long-term references to objects passed to functions like processHttpMessage or doActiveScan. If you need to keep a long-term reference to an HTTP message, use saveBuffersToTempFiles. Also, take care with getSiteMap and getProxyHistory as these can return huge results. Some submissions have called getProxyHistory at startup which results in extremely slow startup with large projects.

10) Provide a parent for GUI elements

If an extension creates GUI elements, such as popup windows or messages, these should be children of the main Burp Frame. This is particularly important when users have multiple monitors, to make sure popups appear on the correct one. To get the Burp Frame, use Frame.getFrames to get all frames, and search for a frame with a title containing "Burp Suite".

11) Use the Extender API artifact

Extensions originally needed to include the Java interface files (IBurpExtender.java, etc.) for compilation to work, which clutters the source code. With newer build tools - Maven and Gradle - this is now unnecessary. Instead, reference the burp-extender-api artifact which is in the net.portswigger group. If you’re starting a new project we recommend using Gradle.

BAppStore

burp extender

Paul Johnston

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
