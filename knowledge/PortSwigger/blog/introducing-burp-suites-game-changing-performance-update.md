# Introducing Burp Suite’s game-changing performance update ⚡🏎️

Source: https://portswigger.net/blog/introducing-burp-suites-game-changing-performance-update
Fetched: 2026-06-28T09:15:17.828816+00:00

Introducing Burp Suite’s game-changing performance update ⚡🏎️

Amelia Coen |

Thursday, 12 September 2024 at 11:55 UTC

Hands-on security testers need the best tools for the job. Tools you have faith in, and enjoy using all day long. Burp Suite has long been that tool, and now, it's faster than ever.

We’ve listened to your feedback and introduced key performance updates to ensure the core tools you rely on are faster, more efficient, and use less memory.

A more efficient Burp Suite

Drastically reduced sorting time for tables

Tables are a core component of Burp Suite. Most of the data produced in Burp is presented in table format. Being able to manipulate this data through sorting is key to your workflow.

Tables which previously would take minutes to sort, are now sorted in a matter of seconds, increasing responsiveness and reducing UI freezes.

I was surprised when a very large table sorted in one second. If that’s due to the new performance stuff, I’m really happy about it! Nice stuff!

- t0xodile, Burp Suite Professional user.

Reduced UI lag and load times

In Burp Suite, your large project files now load faster, even if you’ve got a large number of Repeater tabs. These new changes have significantly reduced memory usage, and will noticeably reduce UI lagging.

Improved loading times in the HTTP history

Multiple changes have been introduced to improve loading times when viewing requests and responses in the HTTP history to prevent the UI from freezing.

Faster site map filtering

Similarly, sitemap filtering time has been significantly minimized. Large sitemaps, which potentially may have taken hours to filter, can now be filtered in a matter of minutes.

Reduced Intruder memory usage

Memory usage in Intruder has been significantly reduced, improving loading times and minimizing the possibility of UI freezes.

If you're interested in more technical details about how we've achieved these improvements, check out this blog post from one of our software engineers.

Optimizing your workflow with Burp

An easy-to-use Proxy Intercept View

The new and improved Proxy Intercept view allows you to have better control when working with websites and functionality that trigger a large number of requests, helping you work more efficiently and at pace.

This new update now allows you to…

View multiple queued requests in a table and manage them in bulk.

View requests and responses in a single view.

Forward all requests.

Highlight and comment on requests and responses.

Pull through any highlights or comments to the HTTP history.

Coming soon…

New UI improvements to Intruder

Intruder is one of the core tools you will use when manual testing, so we’re streamlining the UI to help make your workflow as efficient as possible.

This includes…

Tabs being easier to access on the right side of the screen.

Side by side view of the results table and tabs, making it easier to add columns.

The ability to replace section characters more easily within the request template editor.

Proxy Match and Replace

We’re adding a match and replace tab directly within the Proxy, making it more discoverable and easier to access. Additionally, we’re implementing a test capability within the HTTP match and replace dialog to make writing match and replace rules easier.

Soon, you’ll also be able to write HTTP match and replace Bambdas, enabling more powerful match and replace rules to be utilized.

Burp’s future, driven by performance

Performance is not a one-time fix. We’re making an on-going commitment to improve performance in Burp Suite, ensuring that efficiency, accuracy, and thoroughness are at the forefront of every new update and feature.

As Burp Suite evolves, this performance-first mindset will continue to inform the product decisions of today and tomorrow. Our team is actively using telemetry and regression testing to help identify issues, including those that may previously have been invisible to us, allowing us to act quickly to improve your experience with Burp.

Ready to unleash the power of these new updates?

Say goodbye to frustrating performance blockers - update to the latest version of Burp Suite Professional and conduct your manual testing with increased efficiency and confidence.

Have any suggestions of where else you want to see performance enhancements in Burp?

You can join the official PortSwigger Discord to chat about Burp performance with fellow users and Burp Suite developers.

Amelia Coen

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
