# Improved detection of stored input

Source: https://portswigger.net/blog/improved-detection-of-stored-input
Fetched: 2026-06-28T09:15:17.731486+00:00

Improved detection of stored input

Dafydd Stuttard |

Thursday, 9 August 2018 at 16:29 UTC

MoBP

Burp Suite

Burp Scanner is already capable of detecting when applications store input from one request and return it in the response to another request. When storage and retrieval of input is detected, Burp then checks for a number of second-order issues, such as SQL injection and cross-site scripting.

However, Burp's current capability has two key limitations:

The order in which items are scanned is critical. You need to scan the submission point before the retrieval point. This arises because Burp makes a single pass through the scan queue, processing each item in isolation. So input that is submitted in one request and returned from another will only be detected if the two requests are scanned in the right order.

Input that has been stored within the application can easily be overwritten by other activity carried out by the Scanner, before the stored data is observed. This again arises because Burp carries out all of its audit work on each item in a single operation. Huge numbers of requests might take place between submitting some input and scanning the retrieval point, during which time the input is highly vulnerable to being overwritten.

The new multi-phase scanning model largely removes these limitations and greatly improves Burp's detection of stored input. Active scanning is split into the following distinct phases, and each phase is completed for all items before starting the next phase:

Perform first-order checks.

Submit test strings for stored inputs everywhere.

Fetch all responses one more time looking for stored inputs.

Follow-up on observed stored inputs with second-order checks.

This phased delivery of the different audit tasks removes the dependency on the order in which items are scanned, and reduces the likelihood that stored data is overwritten by other activity before it is observed.

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
