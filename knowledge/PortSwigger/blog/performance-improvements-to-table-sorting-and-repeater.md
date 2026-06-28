# Performance Improvements to table sorting and Repeater

Source: https://portswigger.net/blog/performance-improvements-to-table-sorting-and-repeater
Fetched: 2026-06-28T09:15:23.052633+00:00

Performance Improvements to table sorting and Repeater

Daniel Allen |

Wednesday, 11 September 2024 at 06:53 UTC

Performance is a critical factor in the usability and efficiency of any software, and Burp Suite is no exception. We've recently focused on enhancing Burp Suite's performance across several key areas and have made significant strides in reducing processing times, minimizing memory usage, and ensuring a smoother user experience. Read on for a deep dive into a couple of the performance issues we tackled in recent releases.

Table Sorting

Tables are a core component of Burp Suite. Most of the data produced in Burp is presented in table format. Being able to manipulate this data through sorting is key to many users’ workflows. This section details our approach to the problem and the measurable improvements in performance.

The Problem

The main issue with table sorting stemmed from how data retrieval and sorting operations were handled. Sorting a table on a large project file caused numerous slow and repetitive disk retrievals, significantly hindering performance. When multiple column sorts were applied, it required up to two to three times more data retrievals, exacerbating the problem.

One of the most frustrating issues was the user interface (UI) freezing during these operations. Since the sorting was happening on the UI thread, Burp would become unresponsive. This would also occur on almost all table operations such as inserts and removes since the new values needed to be sorted too. This led to a poor experience, as users could be left unsure whether Burp Suite had crashed or if it was still processing.

The Solution

To address these issues, we undertook a series of technical improvements focused on optimizing data retrieval, offloading processing from the UI thread, and enhancing visual feedback.

Snapshot and In-Memory Cache: We took a snapshot of the table data and sorted it on a separate thread. This approach involved retrieving all necessary data into an in-memory cache before sorting. By doing this, we reduced the need for repeated data retrievals (sometimes of the same object) from disk.

Background Thread Sorting: By moving the bulk of the processing for sorting operations to a different thread, we were able to maintain a responsive user interface. Once the sorting is complete, we pass back the result to the UI thread to update the table. One major consideration during development was the careful management of data integrity across the multiple threads.

UX Improvements: To improve the user experience, we added spinner animations to the headers of the columns being sorted to let users know Burp is working in the background.

Results and Performance Metrics

The changes we implemented resulted in significant improvements to table sorting performance. Here are some key results:

Sorting Time Reduction: For large datasets, sorting times were reduced dramatically. This means that sorting massive proxy histories (250,000+ entries) that previously took minutes were now completed in seconds or less.

UI Responsiveness: The transition to multi-threaded sorting eliminated noticeable UI freezes. This results in a smooth and responsive interface even during intensive sorting operations.

To monitor the results of performance improvements, we have introduced a suite of tests and dashboards that reflect how changes in the codebase affect typical workflows across Burp. This not only allows us to quantify the value of the improvements made but also helps us prevent regressions in performance.

Our performance tests demonstrated these gains, which showed the drastic reduction in sorting times and the improved responsiveness of the UI. These results underscore the effectiveness of our approach and the tangible benefits to our users.

Single Repeater

Repeater is a core part of Burp Suite used for manually modifying and re-sending HTTP requests – it's often key to a pentester's workflow. And, just like a web browser over time, users can (accidentally or otherwise) end up with a lot of Repeater tabs, which we weren't handling the best.

The Problem

When loading Burp Suite, we would previously load one set of UI (user interface) components for each Repeater tab you had. Unfortunately, this meant if you had a lot of Repeater tabs in your project file, then memory usage and the time taken to load up Burp would be significantly impacted, as each set of components would eat up a bit of memory.

It could also lead to general UI lag in the background too, even if you weren't actively using Repeater, which can lead to understandable frustration when using Burp.

The Solution

We've carried out work to try to fix the problem by changing how Repeater tabs are represented internally. Now, we only use one set of UI components, with each Repeater tab only holding onto its individual tab state, such as your selected text, selected editor views, and edit history. This means that there are significant memory savings if you have a large number of tabs. We're now also a bit cleverer about making sure a tab uses no resources until it is clicked on for the first time.

There should be no changes to how Repeater appears to function on the outside, hopefully the only thing you'll notice is the performance improvements!

Results and Performance Metrics

Like with the table sorting work, we've set up automated regression tests to notify us if performance ever degrades. These track both the time taken and memory used when starting a project file with 300 Repeater tabs. We've noticed dramatic improvements in tab operations generally too, such as duplicating or closing group tabs.

We've seen significant improvements on both the memory and performance fronts, and we've also made our thresholds for performance much stricter here, meaning we should never go back to where we were before.

We've done a lot more work on the way for performance. In particular, we've also made improvements to rendering large response bodies within the message editor, the speed of site map filtering, and the memory usage of simple word lists in Intruder.

Release Schedule

2024.5

Table sorting

Lazy load extension tabs

2024.6

Site map filtering speed

2024.7

Single repeater

Message analyzer improvements to speed and memory usage

2024.8 and beyond

Intruder simple list memory improvements

Further message analyzer improvements

Daniel Allen

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
