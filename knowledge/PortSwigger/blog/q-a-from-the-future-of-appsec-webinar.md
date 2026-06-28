# You asked, we answered: Q&A from The Future of AppSec webinar

Source: https://portswigger.net/blog/q-a-from-the-future-of-appsec-webinar
Fetched: 2026-06-28T09:15:24.007882+00:00

You asked, we answered: Q&A from The Future of AppSec webinar

Tom Ryder |

Thursday, 10 April 2025 at 14:33 UTC

When we wrapped up our biggest-ever webinar, The Future of AppSec: PortSwigger’s Vision, the conversation was far from over.

With thousands of security professionals tuning in live, the questions came thick and fast. You asked about everything from on-prem deployments of Burp Suite DAST, to AI models, product roadmaps, and whether AppSec is becoming “a dumpster fire”.

We reviewed hundreds of questions, identified key themes, and selected specific ones to answer that reflect the majority of what people asked.

We’ll be answering some of the standout questions you raised during the session, including topics that we didn’t get time to cover during the webinar. Whether you’re curious about how Burp AI works behind the scenes, Burp Suite DAST support, or just wondering what’s next for Burp Suite, this Q&A is for you.

Thank you again for shaping the future of AppSec with us. Let’s get into the Q&A:

Burp Suite DAST

Q: When is Burp Suite DAST expected to be available for enterprise usage? Interested to get a deep dive demo.

A: You’re in luck, it already is! Burp Suite Enterprise Edition is now called Burp Suite DAST. We’ve renamed it to provide greater clarity around the product’s purpose. Burp Suite DAST continues to be trusted by leading global organizations for scalable, automated security testing and rest assured, we’ll keep innovating and adding new capabilities to make it even better.

Keep an eye out for a follow-up webinar with a live demo illustrating the value of Burp Suite DAST.

Q: If you need to follow a specific workflow in the API, could Burp Suite DAST handle it?

A: Yes. Burp Suite DAST can scan APIs defined via OpenAPI, SOAP, Postman collections, and more. If your API requires stateful workflows, you can use recorded login sequences or authenticated sessions.

Q: How does this DAST tool compare to traditional DAST solutions and API security tools?

A: Burp Suite DAST delivers deep, accurate scanning of both web apps and APIs. We currently support REST and SOAP APIs, either in isolation or as part of a broader web app scan. You just need to provide a suitable OpenAPI (Swagger) spec, WSDL, or Postman Collection.

Unlike generic tools that spread themselves thin across many areas, Burp Suite DAST focuses on delivering deep, high-quality results where it matters most. If your team is looking for a DAST solution that can also handle API security with depth and precision, not just tick a box, Burp Suite DAST is built to meet that need.

Q: Do we have 24/7 support for Burp DAST? Or does the support team work in a specific time zone?

A: Today, our support is based in the UK during business hours, but we’re actively expanding to the USA to provide more responsive, around-the-clock coverage.

Burp AI

Q: Is Burp AI a part of Burp Suite Professional or do you need to pay for it separately?

A: Burp AI is the collective term for AI-powered features included in Burp Suite Professional, along with the trusted platform that securely manages all communication with the AI services. You don't need to pay for an extra subscription, all of the features are included in Burp Suite Professional. However, using Burp AI features relies on a built-in credits system. All users will receive 10,000 free AI credits and further credits can be purchased from within my account.

Q: Will user data and methodology be used to train the AI model or is there privacy?

A: No, data and methodologies will not be used to train the AI models. We understand the concern and take data privacy extremely seriously. We have contractual zero-retention agreements in place with all of our AI providers. This ensures that none of your data is stored or used for model training purposes by the AI service.

Q: Is the AI going to be able to run airgapped and offline?

A: Not at this time. The current AI features in Burp Suite Professional rely on cloud-based large language models accessed via PortSwigger’s secure AI gateway. These models require significant compute power, far beyond what's feasible to run locally on most user machines. As such, the AI functionality cannot operate in offline or airgapped environments today.

That said, PortSwigger is actively engaging with users to understand the drivers behind this need. While there's no immediate solution, we’ve acknowledged this feedback and are considering it as part of our future roadmap.

Q: Do you plan to provide the possibility of connecting your own AI model to Burp Suite Pro?

A: Not within the official product or BApp Store extensions. Burp Suite Professional’s built-in AI features and BApp Store extensions are required to use PortSwigger’s secure AI gateway. However, you can build a private Burp extension outside the BApp Store that connects to your preferred AI backend; you won’t benefit from our integrated protections and simplified configuration.

Q: So, is it possible to NOT have AI implemented out of the box on this new update?

A: You can disable AI features altogether from the setting menu in Burp Suite Professional.

Q: Do you plan to create an AI-assisted report builder?

A: You can already generate AI-assisted reports using the ReportLM BApp - created by one of our own, Tom SL. Find it in the BApp Store to get started.

If you have feedback on any other extensions or AI features, head over to the PortSwigger community Discord and join the conversation.

General PortSwigger Q&A

Q: Will we get a copy of the recording?

A: You can get a copy of the recording of The Future of AppSec webinar here.

Q: How many of the new features in Burp Suite DAST will be available in Pro?

A: Burp Suite DAST is built using the same battle-hardened scanner in Burp Suite Professional - scaled for automation. Burp Suite DAST is built for continuous coverage, not hands-on testing and therefore the feature set is different.

Q: Will AI take over everything? Is the future of AppSec in danger?

A: We see AI as the next evolution in AppSec, helping testers, not replacing them. For more on this vision, read Dafydd Stuttard’s take on the future of human and AI collaboration in AppSec.

Q: Are you planning in the near future to switch the Burp Suite core from Java to Rust or Go?

A: This is a question that comes up every so often. While it’s occasionally popular to criticize Java, the real-world performance challenges we’ve addressed aren’t down to the language. Over the past year, we've made substantial improvements to Burp Suite’s performance, not by switching languages, but by refining how the product works.

Could we rewrite Burp Suite Professional in Rust or Go? Sure; however, a complete rewrite would take an enormous amount of time and effort, time that’s far better spent continuing to optimize and innovate within our current, battle-tested architecture. The gains from a language switch would likely be marginal in comparison.

And for most users, it’s not the language that matters, it’s what the tool can do. We’re focused on delivering the capabilities and performance you need, not rewriting millions of lines of code.

Q: Sorry, one of the most boring Software announcements ever. I'll read about it later

A: Sure, read about it here.

Q: Why are they all British?

A: You caught us, old sport! We thought putting on fake British accents would make us sound more intelligent and respected. By jove we feel like it worked.

Looking ahead

As the application security landscape continues to evolve, your questions help shape where we go next. Whether you're pushing for more integrations, asking tough questions about privacy and AI, or exploring how Burp Suite fits into your workflow, your feedback is what drives us forward.

We’re committed to building tools that not only meet the challenges of modern AppSec, but empower you to stay ahead of them. From Burp Suite DAST to Burp AI, and everything in between, we're excited about what’s next and even more excited to be building it alongside such a passionate and knowledgeable community.

Keep the questions coming, and stay tuned, the future of AppSec is only just getting started.

Watch the full webinar

Did you miss the live session? Watch it on demand now to dive deeper into our plans and product updates.

Watch the webinar now

Tom Ryder

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
