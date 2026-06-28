# Why it's time for AppSec to embrace AI: How PortSwigger is leading the charge

Source: https://portswigger.net/blog/why-its-time-for-appsec-to-embrace-ai-how-portswigger-is-leading-the-charge
Fetched: 2026-06-28T09:15:28.790548+00:00

Why it's time for AppSec to embrace AI: How PortSwigger is leading the charge

Dafydd Stuttard |

Friday, 14 February 2025 at 14:23 UTC

AI is rapidly gaining traction in virtually every industry. But in AppSec, it's often met with a healthy skepticism, viewed by some as a useless gimmick at best or, at the other end of the scale, a major security concern.

This skepticism is understandable. We’ve all been subjected to an onslaught of AI-powered features over the past year that offer little value beyond providing clickbait fodder for marketing departments. Security testing also inherently relies on interacting with potentially destructive functionality and highly sensitive data. As a result, some organizations are hesitant to allow the use of AI tools in pentesting engagements, fearing a loss of control or accidental exposure of this sensitive information.

But avoiding AI altogether isn’t the answer. In fact, it’s a risk in itself.

At PortSwigger, we believe AI has the power to transform penetration testing—not by replacing human testers, but by augmenting them. That’s why we’ve recently released Burp AI, the first AI-enhanced functionality for Burp Suite, not as a gimmick or a response to hype, but to pave the way for creating the power tools that will make pentesters even better at what they do.

A familiar pattern of innovation

We’ve seen this story play out countless times before.

A hundred years ago, for example, carpenters relied on hand tools. The introduction of power tools didn’t make carpenters obsolete—it made them faster, more accurate, and more efficient. Today, no one questions whether a carpenter should use a drill instead of a hand auger; power tools are simply part of the job.

That’s the future we envision for AI in AppSec. AI assistance will become an ordinary, everyday part of the pentester’s toolkit. It won’t replace human expertise, but it will amplify it, helping you work smarter, faster, and with greater precision.

Evolution, not revolution

This isn’t a revolution that eliminates pentesters, it’s an evolution that empowers them.

For decades, pentesters have automated parts of their workflow to improve efficiency. When I first created Burp Suite, it was because I was a lazy pentester. Just like everyone else, I found doing things manually was tedious, repetitive, and inherently error prone.

Burp Intruder was the first tool I built to augment my own workflow, allowing me to scale my testing exponentially, without spending hours scripting each test case I wanted to run. Today, it remains the ultimate power tool for custom, automated attacks and is relied on daily by over 80,000 web app pentesters in 17,000+ organizations across the globe.

I see AI as the next evolution of this idea.

Invest your time and expertise where it matters most

Historically, the received wisdom in the industry was that around 50% of pentesting tasks could eventually be automated, while the other 50% required human intuition.

With the almost unprecedented advances in AI technology in recent years, we believe that number can climb much higher—potentially up to 80%, allowing you to offload the most monotonous work, while keeping expert, human testers in control.

Burp AI will help pentesters:

Find vulnerabilities faster thanks to the efficiency and accuracy provided by AI assistance.

Improve their accuracy by reducing human error in complex, repetitive tasks.

Spend more time on creative problem-solving, applying their time and expertise where it matters most—on the elements of a pentest that AI can’t reliably reproduce.

We're not into gimmicks

We’ve made a conscious effort to try and avoid the mistakes we’ve seen in AI adoption elsewhere.

We’re not cashing in on the hype. If we'd wanted to, we could have released superficial AI features a year ago, but they wouldn’t have delivered real value.

We’re not here to automate pentesting entirely. Today's technology doesn't enable a fully autonomous hacking machine running on autopilot. It’s a human-AI partnership that enhances, rather than replaces, human intuition.

We’re not building an AI black box. Instead of a disconnected engine that does "magic AI stuff” in the background, we’re integrating AI seamlessly into the workflows that testers already use.

We see this much like the introduction of driver assistance in modern vehicles—incremental improvements that make driving safer and more efficient. Assisted steering, adaptive cruise control, and parking aids all help the driver without fundamentally changing how they interact with the vehicle.

Burp AI will follow a similar pattern, providing incremental, practical integrations that seamlessly enhance your existing workflow, rather than forcing you into unfamiliar or disruptive ways of working.

Make no mistake, this is a complex domain and pentesting is so multifaceted that it's a very hard challenge to get this right. That's why we've done a huge amount of work at PortSwigger over the past year to get us to the point where we're really excited to be landing these new capabilities and sharing them with people.

AI, privacy, and control

We know that organizations have real concerns around data privacy and security. That's why we’ve designed our AI-powered features with full transparency and user control:

You're in control. Burp Suite won’t suddenly start sending your data to an AI service without you knowing. You explicitly choose when and how to engage AI assistance.

No AI model training on user data by third-party providers. The AI services we use do not store the data that they process and do not use it for model training purposes. As a result, there's no risk that any information processed by the LLM will somehow be ingested and then regurgitated at a future point to anybody else.

No disruption to existing workflows. AI will be woven throughout Burp Suite in ways that feel intuitive and non-intrusive.

We’re committed to building trust through transparency, ensuring that Burp AI meets the highest security standards. For a more technical breakdown of how we ensure security and reliability, you can read more about how your data is handled in our documentation. If you have any additional concerns, please reach out to us via this short feedback form and we'll do our best to address the most common queries.

The adoption curve

Every major technology shift follows an adoption curve.

Take cloud computing. In its early days, there was widespread hesitation. Organizations worried about data security, compliance, and control. But once they saw the efficiency and scalability advantages, the mindset shifted. Ultimately, the benefits became too obvious to ignore and today, cloud adoption is nearly universal.

AI will follow a similar trajectory. Right now, some companies are naturally cautious. But as AI-powered tools increasingly demonstrate real value, that hesitancy will fade.

We expect adoption to happen in two waves:

Bottom-up adoption: Individual pentesters will experience the efficiency gains of AI firsthand and push for its adoption in their organizations.

Top-down adoption: As businesses see the potential ROI, they’ll shift from AI skepticism to AI-first security strategies.

The cloud revolution was notably different in that it was driven by disruptors and was initially met by resistance from the incumbent players in the industry. With AI, big tech is leading the way, which is why it's already cropping up in the services, applications, and devices we all use daily. This only looks set to continue.

There’s also another elephant in the room: The bad guys aren’t waiting. Malicious actors are already leveraging AI to find vulnerabilities faster and scale their attacks. We on the defensive side of the cat-and-mouse game can’t afford to fall behind.

Experience Burp AI today

We’re proud to be leading the charge in the productive application of AI to pentesting. Our first AI enhancements are now live for Burp Suite Professional users on version 2025.2.3.

We've also given every Burp Suite Professional user a bundle of 10,000 free AI credits, so you can check out what we've been up to at no additional cost. For an overview of what's available, check out Welcome to the next generation of Burp Suite: Elevate your testing with Burp AI.

What's next?

Our mission at PortSwigger is to enable the world to secure the web and we're always working on innovative solutions to genuine, practical problems faced by our users.

Recently, we've found that by leveraging AI, we can build solutions that were previously impossible or impractical to implement. Over the coming months, we hope to release more AI assistance features. But rest assured - we're not working with AI just for the sake of it; we'll continue to develop our core tools using whatever technology gets the best results.

Some AI enhancements will help less experienced users sharpen their skills, reducing the burden on senior colleagues to provide supervision and mentoring. At the other end of the scale, we hope to enable power users to make best use of their time and expertise.

Final thoughts

The question isn’t whether AI will shape the future of penetration testing, but who will leverage it most effectively. At PortSwigger, we’re not just following the curve—we’re defining it.

With Burp AI, pentesters can work faster, smarter, and more efficiently, without compromising control, security, or trust. The best security professionals don’t fear change—they embrace the tools that give them an edge. And right now, that edge is AI.

Continue the conversation

We’d love to hear how you’re getting on with this new AI functionality. Join the conversation on the PortSwigger Discord, and let the community know how you're innovating with AI in Burp Suite in the dedicated Burp AI channel.

About the author

Dafydd Stuttard is the Chief Swig of PortSwigger and the creator of Burp Suite, the industry's go-to toolkit for web app and API security testing. A former pentester himself, he is also the author of the Web Application Hacker's Handbook and created its interactive, online successor, the Web Security Academy. Both continue to serve as invaluable resources for aspiring bug bounty hunters and experienced pentesters alike.

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
