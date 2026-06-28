# Professional 1.6.39

Source: https://portswigger.net/burp/releases/professional-1-6-39
Fetched: 2026-06-28T09:16:27.934453+00:00

This release improves the logic of some scan checks that depend upon the content type of responses.

Burp has previously reported content type incorrectly stated on any occasion where the stated content type of a response differs from the actual content (as determined by Burp). This has frequently led to a lot of noise because (a) Burp's own content type sniffing has not been perfect; and (b) many content type mismatches have no security implications. Hence, many users got accustomed to just ignoring this issue, despite the fact that, in some rare situations, it can lead to high-severity issues like cross-site scripting.

The cases where this issue matters occur when a response is intended to actually contain non-HTML content such as an image, but a browser may attempt to interpret the response as HTML based on the stated content type. This can lead to XSS if the content is dynamically generated, uploaded by a user, or otherwise contains user input.

In the real world, browsers' actual sniffing of responses depends on several factors, including:

The stated content type

The presence of the header X-content-type-options: nosniff

The file extension of the request URL

The browser type and version

The Burp research team have generated every possible permutation of these factors and identified all of the permutations that might lead to a browser attempting to interpret a response as HTML. This knowledge is now baked into Burp, so that Burp only reports the issue when a suitable combination of the above factors is observed. Further, the Burp advisory identifies precisely which browsers may be affected by an issue:

The other type of issue where the situation arises is cross-site scripting. In the past, Burp applied XSS checks to all responses that were either stated or appeared to contain HTML. The scan logic has now been tightened to be more accurate and informative in cases where exploitability of the issue depends upon browser sniffing:

Burp now uses its knowledge of actual browser behavior (based on the factors listed above) to determine whether any browser might attempt to interpret a response as HTML.

If content sniffing depends on the request URL having a different file extension, Burp will attempt to manipulate the extension so as to trigger this.

Any relevant details about specific browsers' behavior is included in the issue detail.

Seemingly unexploitable issues are still reported as informational, because a manual tester might nonetheless be able to find a way to exploit them.

Unrelatedly, the configuration of client SSL protocols and ciphers has been modified to include a master toggle specifying whether to use the default protocols and ciphers of the Java installation. This is the new default option, and can be overridden to allow configuration of specific protocols and ciphers. This change simplifies the configuration UI and makes it easier to share Burp configurations between different machines.
