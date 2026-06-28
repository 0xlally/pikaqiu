# The future of Bambdas

Source: https://portswigger.net/blog/the-future-of-bambdas
Fetched: 2026-06-28T09:15:25.353747+00:00

The future of Bambdas

Emma Stocks |

Thursday, 14 December 2023 at 10:13 UTC

Bambdas, a unique new way to customize Burp Suite on the fly with small snippets of code, were first introduced in the form of a custom filter for the Proxy HTTP history. This is just the first of many more Bambdas we'll be building into Burp Suite Professional and Community Edition in the coming months.

Based on how well the initial Bambdas functionality has been received by all of you, we thought this might be a good opportunity to give you a sneak preview of what the future of customization in Burp Suite looks like.

Where will Bambdas be introduced next?

After seeing how valuable you've all found being able to filter the Proxy's HTTP history, the logical next step was to enable creation of filters within some of Burp Suite's other tools. With that in mind, we'll be adding the ability to create custom filters for both the Logger view and WebSockets history.

The Burp Logger and WebSockets history filters will be available in Burp Suite Professional/Community Edition on the early adopter channel in December, and available to everyone on the main release channel in January next year.

WebSockets history filter

We've already introduced Bambdas into the Proxy's HTTP history filter, allowing you to write custom filters so that the history only displays the requests that you want to investigate further. Of course, not all traffic is HTTP - Burp Suite can proxy WebSockets as well. We've now added the ability to write a custom WebSockets history filter with a Bambda.

Pull up the WebSockets history in Burp Suite, switch to Bambda mode, and write a custom filter using your own code. By writing a Bambda to create a custom filter for the WebSockets history, you'll be able to clear down your dataset to only show you the most interesting findings.

Burp Logger view filter

The next filter we've added is in the Burp Logger. When you're running tests on an application, you want to be sure that you're getting access to all the available data. As a result you'll have hundreds of potentially interesting rows of data to trawl through, but no way of breaking that down to make it easier to spot interesting findings.

By using a Bambda to filter the data from the Logger view, you can save time by filtering out irrelevant traffic to hone in on useful and potentially interesting requests.

What's coming down the pipeline after that?

Along with all of the information that you can see in the tables throughout Burp Suite's tools, there's plenty more information that just isn't being surfaced. Given that we know this is a problem many of our users are facing, we thought we'd apply some Bambda-based creativity to try and generate a solution.

With the introduction of Bambdas, you'll be able to write snippets of code to create and add custom columns to the tables within Burp Suite. Avoid the worry of missing potentially interesting information, and surface the information you do want to see. Complete your testing workflow within one tool, customizing it as you go to surface the information you want and need.

More future Bambdas developments

Following development of the new filtering capabilities and the custom table columns, we've got a few more ideas in the pipeline. In future releases, we plan on adding Bambda functionality to enable a Suite-wide search function for Burp Suite, HTTP listeners, a filter for the Logger capture, and Bambdas to support pre-filters in Intruder that will allow you to determine what goes into the table when running an attack.

We also plan to spend some development time finding the most creative ways to get any custom Bambdas to work together, to really streamline your testing workflows and enable true customization of Burp Suite. The end goal, we hope, is that you'll be able to combine multiple simple Bambdas together to create powerful functionality that can perform complex tasks.

How have you been using Bambdas?

We've seen some amazing and creative uses for the Bambdas functionality from the community so far, and even PortSwigger Research have turned their hand to creating Bambdas. We're loving seeing all the Bambdas you're building and creating, so please do keep sharing them with us on our social channels using #Bambdas - @Burp_Suite and LinkedIn.

If you've created a Bambda that you think other people could use and work with, we'd love you to share it on our official GitHub repo.

Got any good ideas on where you think we could introduce Bambdas to next? Get in touch - we'd love to hear your thoughts.

Emma Stocks

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
