# Enterprise Edition 2022.3

Source: https://portswigger.net/burp/releases/enterprise-edition-2022-3
Fetched: 2026-06-28T09:16:18.687110+00:00

Deploy to any Kubernetes cluster using our new Helm chart

You can now deploy Burp Suite Enterprise Edition to any Kubernetes cluster that meets a few simple prerequisites, using a Helm chart.

This enables auto-scaling of scanning resources, which can help to reduce infrastructure costs and maintenance effort - especially for larger deployments. It also makes it much easier to run Burp Suite Enterprise Edition on your existing Kubernetes infrastructure.

For information on how to deploy Burp Suite Enterprise Edition to Kubernetes, see the documentation.

Migrating from an existing cloud deployment

The new Kubernetes deployment option replaces our existing AWS and Azure cloud deployment templates.

Although deployments built using our AWS and Azure templates will continue to work for the immediate future, we strongly recommend that you migrate to the new infrastructure when possible. Future versions of Burp Suite Enterprise Edition will not support legacy cloud deployments.

For migration details, see the documentation.

Simplified terminology

Due to past confusion, we've changed the way we refer to some components of Burp Suite Enterprise Edition. We're now using more descriptive names instead of jargon.

Most significantly, we no longer refer to "agents", as we found that the word "agent" was used both internally and among users to mean different things depending on context. For example, both the logical entity that performs scans and the machine on which the scan runs on were sometimes both referred to as an agent.

We now refer to the machine that runs scans as a "scanning machine". Likewise, we now talk about the number of "concurrent scans" covered by your license, rather than a number of agents.

Minor improvements and bug fixes

We have also made several minor improvements in this release, including:

We have fixed an issue that was preventing quick scans from running on the Site page.

We have amended the site tree navigation so that any expanded folders remain expanded if you select a site outside of that folder.

We have officially ended support for Internet Explorer 11.

All sites created via the CSV bulk upload feature now have a default scope protocol of Scan using HTTP & HTTPS. This is the same default scope protocol used when creating sites manually in the UI.
