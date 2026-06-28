# Burp 2.0: How do I throttle requests?

Source: https://portswigger.net/blog/burp-2-0-how-do-i-throttle-requests
Fetched: 2026-06-28T09:15:08.631067+00:00

Burp 2.0: How do I throttle requests?

Liam Tai-Hogan |

Wednesday, 10 October 2018 at 15:04 UTC

When performing scans, you might want to limit the rate at which requests are made. Burp 1.x had settings for request throttling within the Spider and Scanner tools. These settings applied to all requests made by the applicable tool. Burp 2.x introduces the concept of resource pools, which let you apply request throttling at the task level.

Burp 1.x

In Burp 1.x, you could throttle the Spider and Scanner tools using the relevant engine settings:

Burp 2.x

You can now use Burp's resource pool options to configure throttling settings that are applied to one or more tasks.

Each resource pool can be configured with the number of requests that can be made concurrently, or the rate at which requests can be made, or both.

You can add more than one task to a resource pool. So, for example, you can create a fast resource pool for tasks that don't need to be throttled, and a slow resource pool for tasks where the rate of requests needs to be controlled.

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
