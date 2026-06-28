# [MoBP] Windows socket exhaustion

Source: https://portswigger.net/blog/mobp-windows-socket-exhaustion
Fetched: 2026-06-28T09:15:21.848946+00:00

[MoBP] Windows socket exhaustion

Dafydd Stuttard |

Sunday, 23 November 2008 at 10:38 UTC

MoBP

burp

sockets

If you've used Burp Sequencer or Intruder much on Windows, the chances are you've encountered this problem:

It happens when you are issuing a large number of requests in quick succession, as Sequencer and Intruder are designed to do. Windows seems to be running out of sockets for you to connect with, resulting in connection failures. The cause is that when you call close() on a Windows socket, the OS leaves it in an open state for a short period. If you open and close a huge number of sockets, even in a single thread, then you can exhaust the pool of available sockets, because they are all in an open state waiting to close. If you run the command netstat -an you will see something like this:

Now, you can apparently tweak the Registry to prevent this behaviour, but I bet hardly anyone does so. The good news is that in the new release, Burp detects the problem and deals with it for you, by rapidly throttling back its requests. When normal network service is resumed, usually in under a minute, Burp reissues the requests that failed and picks up where it left off. This is particularly beneficial in Intruder - for example, if you are performing a lengthy data harvesting exercise, you don't want to worry about large chunks of your attack getting lost because of network problems. In future, you won't have to.

MoBP

burp

sockets

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
