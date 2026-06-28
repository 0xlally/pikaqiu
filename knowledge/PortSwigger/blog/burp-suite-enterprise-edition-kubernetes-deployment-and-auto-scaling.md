# Burp Suite Enterprise Edition Kubernetes deployment and auto-scaling

Source: https://portswigger.net/blog/burp-suite-enterprise-edition-kubernetes-deployment-and-auto-scaling
Fetched: 2026-06-28T09:15:09.369129+00:00

Burp Suite Enterprise Edition Kubernetes deployment and auto-scaling

Matt Atkinson |

Tuesday, 5 April 2022 at 14:59 UTC

Burp Suite

Enterprise Edition

Burp Suite Enterprise Edition is the dynamic vulnerability scanner that can help you to secure your whole web portfolio. And with release 2022.3, we've taken those same flexible Burp scans and made them even better. The all-new way to deploy Burp Suite Enterprise Edition to Kubernetes has now arrived - bringing powerful new auto-scaling capabilities with it.

The new Kubernetes deployment brings two huge benefits to Burp Suite Enterprise Edition:

It enables auto-scaling - which in many cases can dramatically reduce cloud infrastructure costs.

You can now deploy Burp Suite Enterprise Edition to an existing Kubernetes cluster much more easily - using a Helm chart.

Click the button below to see the documentation for the new Kubernetes deployment of Burp Suite Enterprise Edition:

Find out more

Scan your web portfolio more economically

Auto-scaling is a game-changer for cloud deployments of Burp Suite Enterprise Edition. If your scanning requirements are large, or "bursty" (requiring sudden bursts of scanning capacity), then it is particularly likely to save you money on resource costs.

Imagine you have a large number of web apps to scan. You need to scan them once per week, but can only do this on Sundays. In order to complete the scans during the window available, you'll need to run a fairly large number of concurrent scans. But you only want to pay for the scanning machines to run these scans while they are working - not while they sit idle in a data center …

Good news - because auto-scaling harnesses the power of Kubernetes to allow Burp Suite Enterprise Edition to spin up scanning machines only when they are needed. And these machines will then "disappear" when the need for them is over. Depending on your requirements, this could provide you with dramatic cost savings.

Fast, seamless integration with your Kubernetes infrastructure

In the past, if you wanted to deploy Burp Suite Enterprise Edition in the cloud, you'd probably have used one of our cloud templates (AWS CloudFormation or Azure Resource Manager). But these templates were delivered as full infrastructure stacks - meaning that you were limited to a prescribed setup. The new Kubernetes deployment changes all that.

As of release 2022.3, if you want to deploy Burp Suite Enterprise Edition to an existing Kubernetes cluster, it's as simple as downloading our Helm chart and running a Helm install command. This takes a matter of minutes. If you need to create a new Kubernetes cluster for Burp Suite Enterprise Edition, then this will add around 30 minutes on top.

As much as possible, the new Kubernetes deployment is designed to be agnostic about what infrastructure it is running on. This means you can quickly deploy to any x86-based Kubernetes cluster that meets the prerequisites for installation.

Migrating from a legacy cloud template deployment

If you already deployed Burp Suite Enterprise Edition on AWS or Azure using one of our legacy cloud deployment templates, then you will need to migrate to the new Kubernetes deployment in order to benefit from auto-scaling and to continue receiving updates. Note that Burp Scanner will continue to receive updates for the immediate future, but these updates will eventually be phased out for legacy cloud template deployments.

Although legacy cloud deployments will continue to work for the time-being, we strongly recommend that you migrate to the new infrastructure when possible. Future versions of Burp Suite Enterprise Edition will not support legacy cloud deployments.

We're here to help

If you need any support with adopting, deploying, or migrating Burp Suite Enterprise Edition (or any of our other products), then our team is here to help. Talk to us, and we'll help you find the solution.

In the meantime, don't forget to follow us on Twitter to keep up with the latest news - and check out the Burp Suite roadmap for 2022 to get a glimpse of some powerful new features we'll be adding to Burp Suite Enterprise Edition very soon.

Burp Suite

Enterprise Edition

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
