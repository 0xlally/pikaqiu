# Burp Suite Professional is the cornerstone of  Microsoft’s pentesting toolkit

Source: https://portswigger.net/customer-stories/microsoft-case-study
Fetched: 2026-06-28T09:17:02.991043+00:00

Burp Suite Professional is the cornerstone of

Microsoft’s pentesting toolkit

Discover why Burp Suite Professional is indispensable

for Microsoft Azure's security engineers, helping them

navigate complex attack surfaces, streamline workflows,

and secure thousands of applications and APIs.

In this story

IntroductionKey highlightsGaining visibilityActionable insightsDetecting vulnerabilitiesPower of the communityImpact and remediationIndispensable toolkit

At Microsoft, Burp Suite is what you use.

It’s not up for consideration.

Taylor O'Dell, Security Engineer,

Microsoft

Security teams at Microsoft work with

multiple complex environments, and with

thousands of applications and APIs to

secure, keeping on top of this large

portfolio is not easy.

We caught up with Microsoft Azure's

Taylor O'Dell as he shares his insights on

how Burp Suite Professional

has become an indispensable tool in

identifying and mitigating vulnerabilities

in their web applications.

Key highlights

Using Burp Suite to help identify an

application's endpoints and decide what is,

and isn’t, in scope for testing.

Extending Burp Suite’s capabilities with

community-created BApp extensions.

The prevalence of Burp Suite amongst

Microsoft Azure’s Security Engineers.

Gaining visibility over complex attack

surface

Due to the number of complex environments the

Microsoft Azure team are working with, Taylor

often needs to conduct thorough testing on

applications he’s not familiar with. Here,

Taylor’s goal is to map out the full attack

surface, and understand what the scope is.

Unfortunately, this proves a tedious and time

consuming task, particularly as one single

application might involve multiple different

domains and APIs.

It takes days to figure out what traffic you

need to actually care about… we have a million

different domains and the application that

you're testing may use 20 different domains

easily.

Taylor describes how he likes to maximize

his efficiency by leveraging Burp Suite's

automation features to supplement his own

expertise. This proves invaluable in this

initial Discovery phase, where he uses

Burp's automated content discovery tool

to enumerate additional, unlinked attack

surface. Burp Scanner

also forms an integral part of his workflow,

as he typically runs a full crawl and audit

across his entire scope, to ensure maximum

coverage.

I always kick off with a content discovery

session on the targets within scope and then

run Burp’s automated web app scan across all

of my targets. I do a full crawl and audit,

always with the deepest setting.

Not only does this help to optimize the

otherwise tedious process of mapping out the

full attack surface, the initial findings

serve as a useful starting point for

prioritizing areas to focus on first.

At this stage, features such as the

advanced filtering options and global search

help him remove some of the inevitable noise

that comes from testing complex

applications.

Turning scan results into actionable

insights

Taylor starts the Attack phase by reviewing

the scan results on Burp's dashboard. Taylor is able to start working through

this list, sending the ‘juiciest’ results to

Intruder for fuzzing or to Repeater

to manually validate the reported issue. By

doing this, Taylor is also able to quickly

catch any low-hanging fruit and rule out any

false positives, further eliminating

noise.

I start with the dashboard, look for whatever

looks the juiciest, and then work my way

through, validating. Usually my workflow is to

identify anything suspicious, and send it to

Repeater. I'll switch over to Repeater and

start looking one by one, asking myself, ‘what

can I actually do with this request?’, ‘am I

finding the same thing as the scanner?’, ‘is

this a false positive?'.

Detecting invisible, asynchronous

vulnerabilities

Burp Suite's Collaborator is also an

invaluable tool in Taylor's arsenal,

providing an out-of-the-box solution for out-of-band testing (OAST) techniques. By inducing the target to

interact with external network services,

he's able to easily find clues that

otherwise invisible vulnerabilities may be

present, especially blind SSRF.

I do use Burp Collaborator quite a bit for

testing those external service interactions or

SSRF issues. We use the public Collaborator

server most of the time.

Harnessing the power of the community

Taylor also describes how the team at

Microsoft benefit from Burp Suite’s extensibility. The thriving community of extension

developers means they're able to further

enhance Burp's already powerful features.

For example, Taylor often uses ActiveScan++

to extend Burp’s active and passive scanning

capabilities, along with Autorize to do some

of the heavy lifting when testing for broken

access controls.

The library of community-created extensions

also allows him to add specific

functionality to Burp that simplifies

testing specific technologies. For example,

he uses the JSON Web Tokens

extension when testing applications that use

JWTs as part of an authentication flow or

session management mechanism. This enables

him to more easily spot when the server

issues JWTs and provides additional Repeater

views for manipulating tokens without having

to manually decode and re-encode them.

Demonstrating impact and enabling

remediation

After conducting testing on Microsoft’s

Azure applications, it’s crucial for Taylor

to effectively communicate his findings to

both internal stakeholders and development

teams. Taylor often has to explain the

impact of vulnerabilities, and make this

information more digestible for even the

least technical team member.

Burp Suite provides details for any issues

identified during scanning, along with

evidence for the issue in the form of the

request/response sequence that forms the

attack vector. Taylor uses these, along with

the free content on PortSwigger's Web Security Academy, to help him document his findings and

create clear and detailed tickets for the

developers charged with remediating the

issue.

An indispensable toolkit for real-world

testing

Taylor’s reliance on Burp Suite highlights

its versatility and effectiveness in

real-world, enterprise-grade security

operations.

I would be surprised if all penetration

testers are not exclusively using Burp Suite…

[at Microsoft] it’s not even up for

consideration. Burp Suite is what you

use.

Burp Suite’s flexibility as an intercepting

proxy, unrivaled vulnerability scanner, and

toolkit of out-of-the-box solutions for

performing testing of all kinds of

technologies, allows Microsoft’s pentesters to

navigate complex infrastructure, validate

vulnerabilities, and streamline their

workflows.

Ready to implement Burp Suite into your own

pentesting work flow?

Request a free trial of Burp Suite

Professional, or find out more about how

Burp Suite Professional can help you find,

and inspect, the vulnerabilities that matter

the most here.

TRY FOR FREE
