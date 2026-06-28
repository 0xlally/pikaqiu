# Enterprise Edition architecture

Source: https://portswigger.net/blog/enterprise-edition-architecture
Fetched: 2026-06-28T09:15:14.736153+00:00

Enterprise Edition architecture

Dafydd Stuttard |

Saturday, 25 August 2018 at 16:05 UTC

MoBP

Burp Suite

Enterprise Edition

Burp Suite Enterprise Edition comprises the following components:

Enterprise server – This coordinates between the other components, manages scan scheduling, and performs software updates.

Agents – These carry out scans using an embedded instance of Burp Scanner. Agents can be distributed across multiple machines, and the pool of agents can grow indefinitely large.

Web server – This provides the interface to users, via the web UI and REST API. The web server is installed onto the same machine as the Enterprise server.

Database – This provides persistent storage for configuration data and scan results. There is a bundled database which is suitable for evaluation purposes and many production use cases, or you can use your own external database if required.

The diagram below shows the different components of the software and the connections between them:

Burp Suite Enterprise Edition has extreme scalability. For lightweight use, you can run all of the components on a single machine, including the bundled database. On a machine with substantial resources, this set up should be able to comfortably support up to 10 concurrent scans. The diagram below shows a single-machine deployment:

At the other extreme, you can run agents on a large number of machines, and you can use your own external database for storage. This lets you scale the number of concurrent scans to be indefinitely large, and utilize any existing database infrastructure that you have. The diagram below shows a multiple-machine deployment, with an external database and agent machines:

Each agent machine, and optionally the Enterprise server machine, can be configured to run multiple logical agents. Each logical agent can be occupied carrying out a single scan at any given time.

The architecture of Burp Suite Enterprise Edition allows it to meet the needs of a small organization with a few web sites or developers, through to a huge organization with thousands of web sites and many development teams, and everything in between.

MoBP

Burp Suite

Enterprise Edition

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
