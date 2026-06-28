# Burp v1.4 preview - Testing access controls using your browser

Source: https://portswigger.net/blog/burp-v1-4-preview-testing-access-controls-using-your-browser
Fetched: 2026-06-28T09:15:11.928871+00:00

Burp v1.4 preview - Testing access controls using your browser

Dafydd Stuttard |

Tuesday, 22 March 2011 at 09:45 UTC

burp

In the previous post, we described how the "compare site maps" feature can be used to automate much of the laborious work involved in testing access controls. In some situations, however, performing a wholesale comparison like this may not meet your needs. It may be that you prefer to work in a more piecemeal way, individually testing the controls over a small number of key requests. Further, where a sensitive action is performed using a multi-stage process, simply re-requesting an entire site map in a different user context many be ineffective. In this situation, to perform an action, the user must typically make several requests in the correct sequence, with the application building up some state about the user’s actions as they do so. Simply re-requesting each of the items in a site map may fail to replicate the process correctly, and so the attempted action may fail for reasons other than the use of access controls.

For example, consider an administrative function to add a new application user. This may involve several steps, including loading the form to add a user, submitting the form with details of the new user, reviewing these details, and confirming the action. In some cases, the application may enforce access controls over some of these steps but not others. For example, the application may protect access to the initial form, but fail to protect the page that handles the form submission, or the confirmation page. The overall process may involve numerous requests, including redirections, with parameters submitted at earlier stages being retransmitted later via the client side. Each step of this process needs to be tested individually, to confirm whether access controls are being correctly applied.

The new version of Burp contains several features to facilitate this kind of testing. Firstly, when you are testing multi-stage functions in different user contexts, it is often helpful to review side-by-side the sequences of requests that are made by different users, in order to identify subtle differences that may merit further investigation. Burp now lets you:

Filter the proxy history based on the local proxy listener.

Open additional proxy history windows, each with its own filter.

To use these features to help test access controls, you need to use a separate browser for each user context you are testing, and create a separate proxy listener in Burp for use by each browser (you will need to update your proxy configuration in each browser to point to the relevant listener). For each browser, you can then open a separate proxy history window in Burp, and set the filter to show only requests from the relevant proxy listener. As you use the application in each browser, each history window will show only the items for the associated user context.

To open a new proxy history window, use the context menu on the main proxy history tab:

You can then use the filter bar on each window to show requests from different proxy listeners:

So far, this just gives you a way of separating the series of requests made by different user contexts. To actually evaluate access controls over a multi-stage process, you need to test each stage individually, reissuing the request in a different user context, and determining how this is handled by the application. This can often be a laborious process, and involves walking through the multi-stage process repeatedly using your browser, intercepting requests using the proxy, and updating the cookie in one or more requests so that they are issued in a different user context.

A further feature in the new version of Burp takes away some of this pain. It lets you select a request anywhere within Burp, and reissue the identical request from within your browser, within the browser's current session with the application. Using this feature, you can test access controls over a multi-stage process in the following way:

In your Burp proxy history, find the series of requests that are made when a higher privileged user performs the multi-stage process.

For each request, select the "request in browser in current session" option from the context menu. This gives you a unique URL to paste into your browser.

Paste the URL into the address bar of a browser that is logged in to the application as a lower privileged user who should not be able to perform the action. (This browser must be configured to use Burp as its proxy.)

If the application lets you, follow through the remainder of the multi-stage process in the normal way, using your browser.

Review the results to determine whether the lower privileged user was successful in performing the action.

This methodology, of manually pasting a series of URLs from Burp into your browser, is normally a lot easier than repeating a multi-stage process over and over, and modifying cookies manually using the proxy. In general, the new feature provides a highly efficient means of grabbing a request from the site map, or proxy history, or anywhere else, and repeating the request within your current browser session, to see how it is handled.

For people who are interested, the new feature is implemented as follows. When your browser requests the unique URL provided by Burp, Burp returns a redirection to the URL in the original request that you selected. When your browser follows the redirection, Burp replaces the outgoing request with the full request that you originally selected (headers and body), with the exception of the Cookie header, which is unmodified. When the browser receives the application's response to this request, it processes it in the context of the original URL, so all relative links, DOM access, etc. work correctly. Neat, huh?

burp

Dafydd Stuttard

@DafyddStuttard

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
