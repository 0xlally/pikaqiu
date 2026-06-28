# Burp v1.4 preview - Comparing site maps

Source: https://portswigger.net/blog/burp-v1-4-preview-comparing-site-maps
Fetched: 2026-06-28T09:15:12.071450+00:00

Burp v1.4 preview - Comparing site maps

Dafydd Stuttard |

Monday, 21 March 2011 at 13:22 UTC

burp

Somewhat later than planned, as is customary, Burp v1.4 is nearly ready, and it's time to share with you the highlights of what is coming. This release focuses on a small number of frequently requested features which, though you may not use them every day, can in some situations really make your life easier. Over the next few days, I'll be blogging about different features, to whet your appetite. Then I'll release a beta version for Pro users to play with. Everyone with a current license will receive an automatic upgrade to the new version.

The first broad area of new functionality in Burp v1.4 is various features to help test access controls. Fully automated tools generally do a terrible job of finding access control vulnerabilities, because they do not understand the meaning or context of the functionality that is being tested. For example, an application might contain two search functions - one that returns extracts from recent news articles, and another that returns sensitive details about registered users. These functions might be syntactically identical - what matters when evaluating them is the purpose of each function and the nature of the information involved. These factors are way beyond the wit of today's automated tools.

Burp does not try to identify any access control bugs by itself. Instead, it provides ways of automating much of the laborious work involved in access control testing, and presents all of the collected information in a clear form, allowing you to apply your human understanding to the question of whether any actual vulnerabilities exist.

One exciting new feature to help with access control testing is the facility to compare two site maps and highlight differences. This feature can be used in various ways to help find different types of access control vulnerabilities, and identify which areas of a large application warrant close manual inspection. Some typical use-cases for this functionality are as follows:

You can map the application using accounts with different privilege levels, and compare the results to identify functionality that is visible to one user but not the other.

You can map the application using a high-privileged account, and then re-request the entire site map using a low-privileged account, to identify whether access to privileged functions is properly controlled.

You can map the application using two different accounts of the same type, to identify cases where user-specific identifiers are used to access sensitive resources, and determine whether per-user data is properly segregated.

You can access the new feature using the context menu on the main site map:

This opens a wizard that lets you configure the details of the site maps you want to compare, and how the comparison should be done. When selecting the site maps you want to compare, the following options are available:

The current site map that appears in Burp's target tab.

A site map loaded from a Burp state file that you saved earlier.

Either of the above, re-requested in a different session context.

You can choose to include all of the site map's contents, or you can restrict only to selected or in-scope items. If you choose to re-request a site map in a different session context, it is particularly important not to include requests that might disrupt that context - for example, login, logout, user impersonation functions, etc.

To perform the comparison, Burp works through each request in the first site map, and matches this with a request in the second site map, and vice versa. The responses to matched requests are then compared to identify any differences. Any unmatched items in either site map are flagged as deleted or added, respectively. The exact process by which this is done is highly configurable, allowing you to tailor the comparison to features of the target application.

The options for configuring how Burp matches requests in the two site maps are shown below:

The default options shown will work well in most situations, and match requests based on URL file path, HTTP method and the names of parameters in the query string and message body. For some applications, you will need to modify these options to ensure that requests are correctly matched. For example, if an application uses the same base URL for various different actions, and specifies the action using the values of query string parameters, you will need to match requests on the values of these parameters as well as their names.

The options for configuring how Burp compares the responses to matched requests are shown below:

Again, the default options will work in most situations. These options ignore various common HTTP headers and form fields that have ephemeral values, and also ignore whitespace-only variations in responses. The default options are designed to reduce the noise generated by inconsequential variations in responses, allowing you to focus attention on differences that are more likely to matter.

The results of a simple site map comparison are shown below. This shows an application that has been mapped out with administrative privileges, and the resulting site map re-requested with user-level privileges. The results contain a colourised analysis of the differences between the site maps, and show items that have been added, deleted or modified between the two maps. (In this case, since the whole of the first site map was re-requested, there are no added or deleted items in the maps themselves.) For modified items, the table includes a “diff count” column, which is the number of edits required to modify the item in the first map into the item in the second map. When you select an item, the corresponding item in the other site map is also selected, and each response is highlighted to show the locations of the differences:

Interpreting the results of the site map comparison requires human intelligence, and an understanding of the meaning and context of specific application functions. For example, the screenshot above shows the responses that are returned to each user when they view their home page. The two responses show a different description of the logged-in user, and the administrative user has an additional menu item. These differences are to be expected, and they are neutral as to the effectiveness of the application’s access controls, since they only concern the user interface.

The screenshot below shows the response returned when each user requests the top-level admin page. Here, the administrative user sees a menu of available options, while the ordinary user sees a “not authorised” message. These differences indicate that access controls are being correctly applied:

The screenshot below shows the response returned when each user requests the “list users” admin function. Here, the responses are identical, indicating that the application is vulnerable, since the ordinary user should not have access to this function and does not have any link to it in their user interface:

As this example shows, simply exploring the site map tree and looking at the number of differences between items is not sufficient to evaluate the effectiveness of an application’s access controls. Two identical responses may indicate a vulnerability (for example, in an administrative function that discloses sensitive information), or may be harmless (for example, in an unprotected search function). Conversely, two different responses may still mean that a vulnerability exists (for example, in an administrative function that returns different content each time it is accessed), or may be harmless (for example, in a page showing profile information about the currently logged-in user). All of these scenarios may coexist even in the same application. This is why fully automated tools are so ineffective at identifying access control vulnerabilities.

So Burp does not relieve you of the task of closely examining the application's functionality, and evaluating whether access controls are being properly applied in each case. What the site map comparison feature does is to automate as much of the process as possible, giving you all the information you need in a clear form, and letting you apply your knowledge of the application’s functionality to identify any actual vulnerabilities.

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
