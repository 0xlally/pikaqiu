# Using disk-based projects with OpenJDK

Source: https://portswigger.net/blog/using-disk-based-projects-with-openjdk
Fetched: 2026-06-28T09:15:26.859891+00:00

Using disk-based projects with OpenJDK

Liam Tai-Hogan |

Friday, 20 May 2016 at 13:44 UTC

Since the introduction of Burp projects in Burp Suite 1.7 we've had some reports of native crashes in the OpenJDK JVM when using disk-based projects.

Disk-based projects use memory-mapped files, which have been a core part of the Java API spec for a very long time. Because memory-mapped files need to be implemented in native code, there is inherently more potential for compatibility issues, both with the core OS and with disk drivers.

It appears that a bug in OpenJDK may cause the JVM process to crash when using memory-mapped files. This appears to affect only certain platforms, notably Kali Linux.

The easiest way to resolve this issue is to use Oracle Java, which does not contain the bug.

We appreciate that in some instances using Oracle Java may not be practical. We have received reports that this bug has been patched in JDK 9, and it may be possible to backport this patch to Java 7 or 8.

Liam Tai-Hogan

@MetalF0X

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
