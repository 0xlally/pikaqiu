# How FloQast are streamlining testing workflows and  providing actionable reporting for their  developers.

Source: https://portswigger.net/customer-stories/floqast-case-study
Fetched: 2026-06-28T09:17:02.793875+00:00

How FloQast are streamlining testing workflows and

providing actionable reporting for their

developers.

In this story

IntroductionKey highlightsOwen's workflowMapping attack surface and API request structuresOrganizing and prioritizing findingsProbing for vulnerabilitiesUnrivalled featuresFuzzing at scaleOut-of-the-box detectionCustomizable extensibilityAutomated report generationComprehensive toolkit

Burp Suite is my go to.

Owen McCarthy, Application Security Engineer,

FloQast

Software providers face the challenge of

rapidly getting new features and

improvements in the hands of their users,

while ensuring that this agility doesn't

result in vulnerable code slipping through

the net. As such, it's crucial that

Application Security Engineers like FloQast’s

Owen McCarthy are able to find

vulnerabilities and help development teams

patch them effectively before they hit

production.

FloQast offers accounting software to

provide workflow automation and close

management. We caught up with Owen about his

pains when pentesting, and how Burp helps

streamline his workflow.

Key highlights

Using Burp to map an application’s full

attack surface.

Supercharging testing workflows with Burp’s

community-powered extensibility.

Providing valuable, actionable insight for

developers with Burp’s custom issue

creation.

Owen’s workflow in Burp Suite

Professional

Owen's main challenge as a pentester is

effectively securing a broad portfolio of

applications, comprising a diverse and

complex range of technologies.

Throughout the Discovery, Attack, and

Reporting phases of his pentesting workflow,

Owen regularly uses a range of Burp Suite Professional’s built-in features and community-created extensions

to help overcome these challenges.

Mapping attack surface and API request

structures

While Owen utilizes external CLI tools and

scripts for initial subdomain enumeration,

he feeds the results of his external recon

into Burp Suite. Burp provides several tools

that help him to automate this process. He

then uses the content discovery tool and Intruder

to enumerate more attack surface.

The content discovery tool is pretty helpful

at this point. I'll also run Intruder attacks

where the payload position is the subdomain or

end of the link.

Once he's enumerated additional subdomains,

he uses Burp Scanner

to automate the process of crawling the

website to map out the application’s

structure.

We gather a list of known subdomains and then

just pass those to the crawler. We can have

that running in the background to crawl

more.

This automation frees him up to do some

manual discovery and analysis. He uses Proxy

to intercept and analyze the traffic between

his browser and the target app, providing

insights into the application's

functionality and clues that indicate

potential vulnerabilities.

While the crawl is running in the background,

I can also say 'this request looks really

interesting' and start manually testing.

This centralized approach streamlines the

discovery process by balancing automation with

detailed manual analysis.

Organizing and prioritizing findings for

further investigation

Owen uses the site map to help him

structure his testing. This provides a

visual representation of the application's

structure and offers advanced filtering

based on various criteria, facilitating

quick identification of interesting

endpoints. When he identifies areas of the

app to prioritize first, he then sends the

relevant requests to Organizer and Repeater for further analysis.

He takes advantage of the built-in

note-taking functionality to record what it

is he wants to look into so that he can come

back to it later, without needing to

context-switch from what he's doing

currently.

It's really helpful to be able to add a

little note saying what I thought was weird

about the request.

This structured approach prevents losing

track of important observations during the

discovery process.

Speeding up the process of probing for

vulnerabilities and catching low-hanging

fruit

Owen runs targeted scans on specific

requests, or even individual parameters, that

he suspects may be vulnerable. This maximizes

his efficiency as it's much quicker than

manually probing each request for every

potential vulnerability.

I usually run a lot of targeted scans of

requests that I think look kind of sketchy.

For example, if there's a search parameter,

I'll select the value and then right-click and

choose to scan that specific spot. That way, I

can get quick results.

He then uses the results of the scans to

drive the rest of his manual testing

workflow.

Unrivalled features for performing detailed

manual analysis

He then experiments with the request in

Repeater to try to get a deeper understanding

of how the application behaves.

The Repeater is definitely my number one

tool. It lets me take a request and test what

happens if I modify it in a particular way.

This helps me to almost see under the hood of

the application. That's pretty huge.

The Inspector also simplifies this process by

helping Owen work with encoded data in

requests and responses without having to

switch to another tool.

Fuzzing at scale, without writing a single

line of code

Once Owen feels that he might be onto

something, he likes using Intruder to

perform this kind of probing at scale,

resending the request over and over, fuzzing

controllable inputs to detect interesting

behavior and trying lots of variations of

potential payloads to see how the

application responds.

Intruder is really helpful for this because

it means I don't have to spend hours setting

up a whole Python script, which may not even

find anything. It's really nice to just be

able to go 'Here is a list of 100 things to

try' and just run through them real quick

without having to worry about it too

much.

This combination enables Owen to efficiently

test different attack vectors and approaches

for bypassing security mechanisms and confirm

the exploitability of potential

weaknesses.

Out-of-the-box detection of otherwise

'invisible' vulnerabilities

Owen uses Burp Collaborator, an out-of-the-box solution for hunting

for asynchronous or 'invisible'

vulnerabilities. Developed in conjunction

with the world-class PortSwigger Research

team, Collaborator provides a client and

server that enable you to easily detect

these vulnerabilities by inducing the target

to make unintended outbound interactions

with an arbitrary external system.

Collaborator is a huge one. I use it a lot.

It's super helpful to be able to quickly see

if there's an SSRF vulnerability in the

background, where the app will make a request

to any URL you provide.

He combines this with James Kettle's Collaborator Everywhere

extension, which automatically injects

Collaborator payloads into a variety of

headers and other inputs.

It tosses a payload into practically every

input and then I can just see what comes

back.

Customizable extensibility, powered by the

community

Owen uses a number of community-created

extensions to add support when working with

specific technologies or testing for

specialist attack vectors.

The customizability and extensibility is

really helpful if you're testing a target that

has a different tech stack, there are

extensions you can grab that are specific to

that. Burp doesn't make it cumbersome like a

lot of other software.

He also loves being able to quickly create

custom scan checks, known as BChecks, to search for specific vulnerabilities,

enhancing the effectiveness and accuracy of

scans:

There's a ton of BChecks that I use. They're

my go-to if I need to quickly come up with

passive or active scan checks. They're really

helpful.

Overall, he loves that Burp simplifies this

workflow, while still providing enough

granular control for when you need it.

It kind of hides the difficult stuff but

still makes it available if you want to get

into something really advanced.

Automated report generation to help present

findings to development teams

Although Owen and his team manually craft

reports, they still take advantage of Burp's

automated reporting features to save time and

provide a consistent reporting format.

It's super useful to grab the example

requests from the scan report. These contain

the payload used and mean I don't have to go

to Repeater and make an example request

myself.

The ability to manually create an issue in

Burp Suite, providing your own detailed

description and remediation advice, helps Owen

provide valuable context for developers and

improves the efficiency of remediation.

A comprehensive toolkit designed to work

with complex applications

For Owen and the team at FloQast, Burp

Suite simplifies otherwise complex tasks and

provides a comprehensive platform for web

application penetration testing. Its

customizable nature, extensibility, and

powerful features like Repeater, Intruder,

and targeted scanning significantly improve

their efficiency and mitigate the pains they

experience during various stages of

pentesting.

80,000 pentesters worldwide, like Owen, are

currently using Burp Suite Professional to

optimize their security testing. Join them

by requesting a fully-featured free trial of

the web security tester's toolkit of

choice.

TRY FOR FREE
