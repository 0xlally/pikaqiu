# Automated content discovery with Burp Suite

Source: https://portswigger.net/burp/documentation/desktop/testing-workflow/mapping/hidden-content/automated-discovery
Fetched: 2026-06-28T09:15:58.172398+00:00

Support Center

Documentation

Desktop editions

Testing workflow

Mapping the website

Discovering hidden content

Automated discovery

Professional

Automated content discovery with Burp Suite

Last updated:

June 18, 2026

Read time:

1 Minute

You can use Burp Suite Professional's automated content discovery tool to discover hidden directories, files, and other endpoints. The tool uses lists of common file and directory names to guess the names of hidden functionality. It also derives a naming scheme from the resources already identified and uses this to search for similarly named items. This enables you to discover additional attack surface.

Before you start

You need to populate the site map with some content before you use the content discovery tool. For a tutorial on how to map the target website, see

Mapping the visible attack surface.

Steps

You can follow along with the process below using ginandjuice.shop, our deliberately vulnerable demonstration site. To scan for hidden content:

Go to Target > Site map.

Right-click on the root node for the domain.

Click Engagement tools > Discover content. The Content discovery dialog opens.

Click Session is not running to start the discovery session with default settings.

By default, the tool adds discovered content to the Target site map. You can also view the site map that the content discovery tool builds in the dialog's

Site map tab.

Note

You can alternatively use Burp Intruder to discover hidden directories, files, and other endpoints. This gives you more manual control over the process.

Related pages

Content discovery.

Site map.

Typical uses for Burp Intruder.
