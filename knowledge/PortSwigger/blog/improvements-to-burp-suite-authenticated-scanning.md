# Improvements to Burp Suite authenticated scanning

Source: https://portswigger.net/blog/improvements-to-burp-suite-authenticated-scanning
Fetched: 2026-06-28T09:15:19.779110+00:00

Improvements to Burp Suite authenticated scanning

Matt Atkinson |

Friday, 29 October 2021 at 12:22 UTC

Burp Suite

Burp Suite's authenticated scanning feature enables users to scan privileged areas of target web applications even when a complex login sequence is required. This leverages Burp's browser - using the included Burp Suite Navigation Recorder extension to store a record of your login actions in JSON. This can then be passed to Burp Scanner for use in automated testing. Authenticated scanning is available in both Burp Suite Enterprise Edition and Burp Suite Professional, and enables efficient testing of modern web apps.

Burp Suite 2021.9.1 brought in some powerful new developments - including a number of behind-the-scenes improvements to the way authenticated scanning works. You can now record login sequences in a number of new contexts - helping you to test today's ever more complex web applications. In this post, we're going to take a closer look at the authenticated scanning features Burp Scanner gained in version 2021.9.1.

You might also like to see the latest Burp Suite release notes.

New - iframes

Nowadays, it's fairly common for a web application to utilize iframe elements during the login process. Although they are used by many systems, iframes can be problematic for a scanner - given that they are essentially a page embedded within another page (right down to having separate URLs).

As of release 2021.9.1, Burp Suite is able to record and replay interactions within iframes - logging the sequence you input. The keen-eyed among you may have noticed a new property in the Navigation Recorder's JSON output called frameId, which is key to this capability - uniquely identifying iframes.

New - animated elements

When Burp Scanner needs to click on an element in order to replay a login, it initiates a sequence of events which culminates in Burp's Chromium browser providing a set of coordinates to send a click event to. But with animated elements, this is slightly trickier. In the time taken to complete the identification and location process, the element may have moved to a different location.

This used to mean that Burp Scanner could run into problems when dealing with animated elements (used by systems including Microsoft SSO) during a recorded login. As of release 2021.9.1, Burp Scanner now waits for such animations to finish animating before it sends actions - fixing this issue.

For more information on how the Navigation Recorder and Burp Scanner work together, check out our scanner team's recent blog post on how Burp Suite records logins.

New - DOM-based redirections

From a scanning perspective, one problem with JavaScript is that it's not always straightforward to see when it will execute. For instance, a page's body element might contain an onload event handler which (as soon as the page is fully loaded) redirects the user to a login page. An example of this would be when a page displays an informational message for a set period of time, before redirecting the user to a login screen.

Burp Scanner is now able to better handle such redirections during authenticated scanning - adding further utility when testing modern web apps. Changes have also been made under the hood, to give Burp Scanner a much better idea of when a page has finished loading / settled. This in itself is a tricky task, given the extremely dynamic nature of much modern web content.

New - SVG elements

Speaking to our users, we became aware of a problem with Burp Suite's authenticated scanning feature, where Burp Scanner could be confused by buttons containing a nested SVG image (such as an icon). This could cause the scanner to click on the image, rather than the button.

Release 2021.9.1 fixes this issue, by changing the way Burp Suite identifies SVG elements. Previously, Burp Suite was unable to record information about where SVGs were located in the DOM, but now it can - including the XPath. XPath is important, because it allows elements to be located in the DOM. Since 2021.9.1, Burp Suite will use the SVG namespace to correctly identify an image - fixing this problem.

New - multi-select

Although it admittedly represents a somewhat niche use-case, Burp Suite 2021.9.1 also added capability for dealing with situations where users can select one or more options from a list. This is commonly known as a multi-select (a select element where the multiple attribute has been set). Burp Suite's ability to handle such elements through authenticated scanning will make testing much more efficient, should you happen to encounter one in the wild.

Until next time

As you can see, modern web application login sequences can be far more complex than the simple HTML forms of yore. But Burp Suite's continuous development is helping it meet the needs of today's web security professionals.

Whether you're testing traditional login functionality using the old-style Burp Suite application login option, or using the authenticated scanning feature to test modern functionality, we've got you covered.

Don't forget - stay in the loop with the latest goings-on, and keep up with the latest Burp Suite releases by following PortSwigger on Twitter.

Burp Suite

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
