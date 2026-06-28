# The new configuration library

Source: https://portswigger.net/blog/the-new-configuration-library
Fetched: 2026-06-28T09:15:26.240862+00:00

The new configuration library

Dafydd Stuttard |

Thursday, 16 August 2018 at 15:35 UTC

MoBP

Burp Suite

Burp's current Spider and Scanner tools have their own configuration options which apply globally to all spidering and scanning activity. You can save these options in project configuration files, which gives you a functional way of managing useful configurations and loading them on different occasions.

With the introduction of multiple parallel scans, each with their own configuration, there is a need for an improved way of managing configurations.

Enter the new configuration library:

The configuration library lets you manage your own collection of Burp configurations that are useful for different tasks. For example, you might create different configurations for different types of scans, or for working on particular client engagement.

Whereas previously Burp shipped with a single set of default settings, representing a "normal" configuration suitable for typical activities, the configuration library contains a number of built-in configurations that are useful for common purposes. You can also, of course, create your own.

Creating or editing a configuration in the library opens a configuration editor of the relevant type, where you can choose which areas will be defined, and set the options that you want:

You can export or import configurations in the same JSON format that Burp already uses for its general configuration options. This lets you easily collaborate with others and share configurations that anyone else might find useful.

MoBP

Burp Suite

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
