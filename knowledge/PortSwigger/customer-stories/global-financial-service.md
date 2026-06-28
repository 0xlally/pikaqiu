# Precision meets scale: How a global payments leader  unblocked their manual pentesters with Burp Suite  DAST

Source: https://portswigger.net/customer-stories/global-financial-service
Fetched: 2026-06-28T09:17:02.656627+00:00

Customer Stories

Precision meets scale: How a global payments leader

unblocked their manual pentesters with Burp Suite

DAST

From point-in-time testing to ongoing protection -

uniting automation and expertise at enterprise

scale

In this story

Customer snapshotThe CompanyThe ChallengeThe SolutionThe ImpactThe Future

Customer snapshot

Industry: Global financial services (payments).

Size: ~20,000+ employees worldwide.

Region: Global (EMEA-led adoption).

Environment: Highly regulated, mix of on-prem and

cloud, Kubernetes deployments.

Key compliance drivers: PCI DSS, global financial data security

requirements.

The Company

This global payments organization operates

in over 200 countries and maintains a

world-class security team responsible for

protecting hundreds of web applications and

APIs. In the financial sector, robust and

mature security practices aren't just an

ideal, they're non-negotiable. The company

has relied on Burp Suite Professional for

over a decade, equipping hundreds of

pentesters and SSDLC teams with tooling that

provides the depth and precision required in

such a high-stakes domain.

The Challenge

The penetration testing team manages over

1000 manual tests each year. While this

approach is essential for high-value

applications, it created bottlenecks for

medium- and low-risk systems. The backlog of

tests slowed release cycles and left

development teams waiting for feedback on

issues that could have been uncovered

earlier.

The organization was already well-versed in

static analysis (SAST), but these tools

could not expose runtime issues such as

missed APIs or authentication flaws in

AngularJS-heavy applications. The leadership

team wanted to move routine testing into

automation, reducing the load on pentesters

while ensuring that results would be trusted

and actionable.

At the same time, they needed a deployment

that would meet strict data privacy

requirements, integrate into CI/CD

pipelines, and scale from a handful of

concurrent scans to hundreds.

The Solution

Building on their long-standing trust in

Burp Suite Professional, Burp Suite DAST was

the natural choice for extending established

manual testing practices into a powerful

automated solution that fit seamlessly into

the existing security strategy. As both

products run on the same scanning engine,

there was no question about the credibility

of results.

The rollout began in QA, where automated

“observation scans” were introduced to give

developers early feedback on their code

without adding governance overhead.

Higher-stakes “release scans” were still

managed by the central security team,

ensuring consistency and oversight.

To prepare for enterprise scale, the

automation group deployed Burp Suite DAST on

Kubernetes, adapting helm charts and

database integrations to fit tightly with

internal systems. They also built an

internal wrapper so application owners could

upload Postman collections and trigger scans

themselves. This model allowed security

teams to triage and prioritize results,

while empowering developers to test on

demand.

The Impact

By embedding Burp Suite DAST, the

organization began shifting hundreds of

medium- and low-risk applications into

automated testing, reducing reliance on

manual penetration tests and clearing the

backlog. Pentesters, once faced with the

daunting task of having to find and report

all vulnerabilities across their entire

portfolio, could now dedicate their

expertise to complex, high-risk systems

where their efforts make the most

impact.

Developers gained earlier insight through

scans they could trigger independently,

while the security team retained governance

of critical releases. After the initial

onboarding period, concurrent scans ramped

up from around 100 to over 1,000. With

confidence in their ROI, the organization is

now preparing to run DAST at a scale that

matches its existing static analysis

tools.

I want developers to be able to run DAST

alongside SAST. That way, the low-hanging

fruit gets caught automatically — and pentests

can focus on real issues.

The Future

The next phase of adoption focuses on

embedding Burp Suite DAST into CI/CD

pipelines, using a GraphQL-based wrapper to

orchestrate developer-triggered scans within

the company’s “Shift Left” automation

portal. By FY26, the program aims to scale

across more than 900 applications and

thousands of concurrently running DAST

scans.

Looking ahead, the organization also plans

to align DAST with its enterprise AI

strategy, using Burp AI to assist with

triaging and escalation. With these steps,

it is building a future in which automated

runtime testing and deep manual expertise

work hand in hand — reducing risk at scale

without slowing innovation.

Ready to strengthen your external security

coverage?

Take our interactive walkthrough to see how

Burp Suite DAST scales web application

security across large portfolios without

slowing down your teams.

TAKE THE WALKTHROUGH
