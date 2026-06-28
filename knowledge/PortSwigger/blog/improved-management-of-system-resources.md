# Improved management of system resources

Source: https://portswigger.net/blog/improved-management-of-system-resources
Fetched: 2026-06-28T09:15:17.257767+00:00

Improved management of system resources

Dafydd Stuttard |

Wednesday, 15 August 2018 at 15:37 UTC

MoBP

Burp Suite

Here are a few problems that some users regularly run into when using Burp:

It's easy to overload either the local machine, the network connection, or the application being tested, by kicking off too much parallel activity. Because each area of Burp has its own settings for thread counts and request throttling, using tools like the Spider, Scanner, and Intruder can quickly ramp up the amount of work to an excessive level.

As already discussed, Burp's current Scanner processes each item in isolation in a single operation. For each item, this involves sequentially executing passive checks, active checks, and JavaScript analysis. In some situations, this creates bottlenecks. For example, in JavaScript-heavy applications, the entire Scanner thread pool can become busy performing JavaScript analysis on multiple items. During this time, no scan requests are made, so network resources are under-utilized. And looking at the scan queue UI, the Scanner is apparently locked up, because there is no indication of ongoing progress.

In low memory conditions, the Java runtime expends increasing amounts of effort on garbage collection, trying to free up memory for reuse. This can lead to high CPU utilization for a lengthy period or even indefinitely. The result is that Burp grinds to a halt, doing nothing and maxing out CPU, with no feedback to the user as what has actually gone wrong.

The forthcoming release makes some big improvements on these issues, particularly in relation to scanning (similar treatment of Intruder and other automated tasks will come later):

There is a new task execution engine that centrally manages the resources that are assigned to running tasks. Passive processing is performed in a fixed-size thread pool, whose size depends on the number of CPU cores. Each task has a thread pool for active work, whose size adjusts dynamically based on network throughput, configured throttling settings, and the number of other running tasks.

Separate resource pools can be created with different configurations. Each task is assigned to a resource pool, and can be moved between resource pools at any time. Each resource pool is configured with its own throttling settings which control the number of requests that can be made concurrently, or the rate at which requests can be made, or both.

The new multi-phase approach to scanning divides up work into passive and active components. These can be executed in parallel to make maximum and efficient use of system resources. So active work can make network requests while passive work makes use of available processing, without either component crowding out and deadlocking the other. The new UI gives precise feedback on the progress of individual items through the different phases of scanning.

Burp continually monitors overall memory pressure, and gives you real-time feedback. In conditions of very low memory, Burp can automatically pause running tasks to reduce the ongoing pressure, stabilize the environment, and let you gracefully save your work.

This is what the new UI for managing task execution and resource pools looks like:

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
