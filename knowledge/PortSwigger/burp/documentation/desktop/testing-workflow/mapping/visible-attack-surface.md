# Mapping the visible attack surface with Burp Suite

Source: https://portswigger.net/burp/documentation/desktop/testing-workflow/mapping/visible-attack-surface
Fetched: 2026-06-28T09:15:58.081236+00:00

Support Center

Documentation

Desktop editions

Testing workflow

Mapping the website

Mapping the visible surface

ProfessionalCommunity Edition

Mapping the visible attack surface with Burp Suite

Last updated:

June 18, 2026

Read time:

2 Minutes

To discover locations that are available to audit, you need to map the target application's visible attack surface. This refers to the endpoints that are explicitly used by the domains you're testing. Make sure you map the entire application thoroughly, so that you don't miss anything interesting.

Before you start

We recommend that you set an initial test scope before you start mapping the application. For more information, see

Setting the initial test scope.

Steps

You can follow along with the process below using ginandjuice.shop, our deliberately vulnerable demonstration site. To map the visible attack surface:

Open Burp's browser and go to your target application.

Without closing the browser, go to Target > Site map. Notice that a node has been automatically added to represent the target domain. If no node is present, go to the Dashboard and make sure that the default Live passive crawl from Proxy task is running. This task adds items to the site map as traffic is proxied through Burp.

If you're using Burp Suite Professional, start an automated crawl of the website. Right-click the root node for the domain, then select Scan. The

New scan dialog opens:

If you have any application login credentials, select Application login and enter the credentials. For more information, see Application login options.

Under Scan type, select Crawl.

Click OK to start the scan. Burp Scanner crawls the application. Notice that the site map

automatically populates as Burp Scanner discovers content.

While the scan runs, go back to Burp's browser. Explore the website to familiarize yourself with it and identify high-risk functionality.

If you're using Burp Suite Community Edition, make sure you fully explore the application:

If you have any application login credentials, or are able to create your own user, log in and explore the authenticated areas of the site.

In the site map, notice that some endpoints that are grayed out. These are locations that are explicitly referenced in a response, but have not been requested.

To discover additional content, select any interesting grayed out endpoint. Right-click and select Request in browser > In original session. A dialog opens with a URL for the request.

To open the request, copy the URL, then paste it into Burp's browser.

Continue to browse the application.

Continue to populate the site map until you have requested all visible locations that are interesting and within your scope.

Related pages

Burp's browser.

Site map.

Scanning web applications.

Site map workflow tools - Request in browser.

After identifying the visible attack surface, it's a good idea to browse for hidden content. For more information, see the

Discovering hidden content tutorials.

For a tutorial on using Burp to identify high-risk functionality as you browse the website, see Identifying

high-risk functionality with Burp Suite.
