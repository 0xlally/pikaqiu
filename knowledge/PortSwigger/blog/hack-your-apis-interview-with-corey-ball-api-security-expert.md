# Hack your APIs: interview with Corey Ball - API security expert

Source: https://portswigger.net/blog/hack-your-apis-interview-with-corey-ball-api-security-expert
Fetched: 2026-06-28T09:15:15.993376+00:00

Hack your APIs: interview with Corey Ball - API security expert

Matt Atkinson |

Monday, 4 January 2021 at 16:52 UTC

Interviews

Corey Ball is a Cybersecurity Consulting Manager, and author of the forthcoming book Hacking APIs (working title - No Starch Press). As well as being a long-time API hacking enthusiast, Corey’s role gives him a great vantage point onto cybersecurity industry trends - allowing him to see the bigger picture where issues like API security are concerned. This blog post is based on a conversation we had with Corey in November 2020.

Background: the state of play in API security

APIs have been around for a long time - and this mature infrastructure is only growing more interesting to hackers. The rise of microservices in recent years has led to the API ecosystem becoming increasingly complex. This, combined with time-honored issues such as broken object level authorization, directory traversal, SQL injection, and stolen credentials, has led to a plethora of vulnerabilities cropping up. In 2019, OWASP even revealed a version of its Top 10, just for APIs.

In early 2020, Starbucks awarded a critical bug bounty payout to a researcher who found a flaw in its API systems. The bug potentially exposed the records of up to 100 million customers - with the researcher in question describing the bug as “well known, but under researched”. Similarly, in 2018, an issue with a USPS application allowed anyone with an account to view, and in some cases modify the details held for around 60 million users. Again, poor API implementation was at fault.

“You can design an API you think is ultra-secure, but if you don’t test it, then a cybercriminal somewhere is going to do it for you”.

APIs represent a huge attack surface for most organizations. To put it in perspective, Okta recently cited Gartner in predicting that by 2022, API abuses will be the most frequent attack vector resulting in data breaches for enterprise applications. Furthermore, in 2018, Akamai found that API calls alone represented around 83% of web traffic.

In November 2020, Burp Scanner gained the ability to parse API definitions to identify hidden endpoints, as well as their supported methods and parameters. This allows enhanced scanning of APIs with definitions written in both JSON and YAML - in both Burp Suite Enterprise Edition and Burp Suite Professional. While this release supports scanning for a fairly limited range of REST APIs, we’ll expand this to support more APIs in coming releases.

Don’t overlook your APIs

In Corey’s opinion, because most APIs are primarily used/consumed by developers and machines they often get overlooked during security assessments. Compounding this problem, many organizations would struggle to actually list all the APIs they have on their systems.

Worse still, because APIs are so varied, they’re difficult to scan. Even within a single organization, similar-looking endpoints could have completely different specifications from one another. Corey points out that many vulnerability scanners lack the features to properly test APIs, and are consequently bad at detecting API vulnerabilities. If your API security testing is limited to running one of these scanners, and it comes back with no results, then you run the risk of accepting false negative results.

You can see the results of this in the news. The 2018 USPS incident (above) happened because security was simply not taken into consideration during an API’s design. A researcher was able to compromise the USPS application’s security using trivial methods, despite a vulnerability assessment having been carried out a month beforehand. The assessment had failed to spot the glaring issue.

PortSwigger’s view: Vulnerability scans are best used as part of a balanced security program. While some web vulnerability scanners struggle with APIs, Burp Scanner’s new ability to parse API definitions mean its capabilities in this area are growing ever stronger.

But aren’t APIs standardized now? Shouldn’t they be secure by design?

We’re making progress. You’ve got things like the switch from Swagger to OpenAPI which have meant that APIs are increasingly standardized. This is generally a good thing - and it certainly makes certain aspects of testing easier. But just because something is standardized doesn’t mean it’s implemented correctly - and that’s the situation organizations often find themselves in.

There are still many pitfalls out there when you’re implementing an API. Has everything been included in the definition? Has an update been made? Maybe you’ve got some kind of asset management problem where a previous version is still available? These are the sorts of things you have to consider when you’re doing this.

If you could give one piece of advice to organizations looking to secure their APIs, what would it be?

When we put this question to Corey, he laughed. API security is - after all - a huge subject. But, on thinking about it, Corey’s face straightened up. His response? “Hack them”. “You can design an API you think is ultra-secure, but if you don’t test it, then a cybercriminal somewhere is going to do it for you”.

Scanning your APIs for vulnerabilities is a great start, but this alone isn’t enough. APIs are somewhere that serious business logic vulnerabilities can easily materialize - and scanners will generally struggle to find these. You always need the lateral thinking and adversarial mindset that comes with penetration testing in order to be truly confident in your security.

What are some examples of common API business logic vulnerabilities?

You can define business logic vulnerabilities as “deliberately designed application functionality that can be used against the application to compromise its security”. Take the example of a high-level planning discussion about app functionality. Generally speaking, that conversation probably involves user convenience before it does security.

Corey gave a great example of this from his experience as a cybersecurity consultant. A business he was working with wanted to give app administrators the ability to easily search for the account information of any of the app’s users. But the business in question hadn’t thought to secure this feature - instead trusting that the average user would simply not discover or use its functionality.

The main takeaway from all this is that if you’re going to have truly effective cybersecurity, then conversations about security really need to happen at a strategic level. Cybersecurity professionals need a seat at the table right from the planning stages, so that effective security can be designed in.

For more information on logic flaws, check out the Web Security Academy’s section on business logic vulnerabilities.

PortSwigger’s view on API security

Like any other aspect of web application security, effectively securing your APIs requires an holistic approach. This should involve everything from vulnerability scanning to manual pentesting - and it’s important that a degree of adversarial thinking is built in from the design stages onwards.

Burp Scanner’s new ability to parse API definitions is included in both Burp Suite Enterprise Edition and Burp Suite Professional. Use this to gain visibility of your API attack surface, and to free up time for your pentesters - allowing them to use their testing skills to greater effect. And of course Burp Suite Professional includes a range of tools that testers will find useful for manually testing API security - as well as giving access to specialized extensions through the BApp Store.

To further educate yourself about API security, keep an eye out for Corey’s upcoming book Hacking APIs (working title - No Starch Press). You can also learn more about specific web security vulnerabilities in the Web Security Academy.

Interviews

Matt Atkinson

@mattatkinson42

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
