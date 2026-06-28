# Site map comparison results

Source: https://portswigger.net/burp/documentation/desktop/tools/target/site-map/comparison-results
Fetched: 2026-06-28T09:16:09.228693+00:00

Support Center

Documentation

Desktop editions

Tools

Target

Site map

Comparison results

ProfessionalCommunity Edition

Site map comparison results

Last updated:

June 18, 2026

Read time:

3 Minutes

The comparison results highlight differences in the tree and table views of both site maps.

Viewing comparison results

Added, deleted, or modified items are color-coded.

You can view the minimum number of text edits required to convert the response in Map 1 to match the response in Map 2. This is shown in the Diff count column.

When you select a branch or table item in one map, the other map updates to show the same selection. To change this behavior, deselect Sync selection.

You can view the full requests and responses for the selected items in the request / response viewers. Burp highlights relevant differences within the responses.

The display filter applies to both maps. All items are shown by default.

Interpreting comparison results

To interpret the results of a site map comparison, you need to understand the meaning and context of specific application functions. For example:

Some differences between responses are security neutral. For example, the application home page of two different users may contain different display names, links, and other user-specific content. These differences are expected and do not indicate access control issues, as they only concern the user interface.

Some differences indicate that access controls are working as designed. For example, an administrative user may be able to access a privileged function, while a low privileged user sees a "Not authorized" message.

In some cases, if the same response is returned for two different users it indicates a security issue. For example, an administrator might have a link to a page that contains sensitive user information. A low privileged user who knows the URL may be able to view the same page.

In other cases, the same response being returned to two users is security neutral. For example, a public search function in an application might be designed to return the same results for all users.

Per-user UI customization, such as display names and links, can cause differences on many pages. In this case, look for other similarities and differences that could be relevant to access control.

Any combination of these scenarios can occur in the same application. This makes it more difficult to identify genuine access control problems. The only way to do this is to manually review the comparison results. Burp has several ways to make this process easier:

Use the display filter to filter items that contain specific expressions. For example, if most admin functions return a "Not authorized" message when requested by a low privileged user, you can hide these responses from the map. This enables you to focus on other items that may reveal oversights in the application's privilege model.

Use the Diff count column to identify unusual responses. For example, if per-user UI customization causes most pages of an application to contain two differences, sort the responses by diff count to look for pages with a different value. Also, if you find one access control vulnerability that has a particular diff count, look for other responses with a similar count. This may represent similar vulnerabilities.

The results may reveal that some comparisons of response headers or form field values are not relevant. To exclude these from the comparison, change the response comparison or request matching settings and re-run the comparison. You don't need to re-request the site maps when you change these settings.

The results may show that some requests are incorrectly matched, based on query string or body parameters. If this happens, change the response comparison or request matching settings and re-run the comparison. You don't need to re-request the site maps when you change these settings.

There are many challenges when you evaluate access controls, which means fully automated tools struggle to find access control vulnerabilities. These automated tools generate lots of noise and are very prone to false positives and negatives. Burp does not attempt to automatically examine the application's functionality, or evaluate how access controls are applied. Instead, the site map automates as much of the process as possible. It presents the information clearly and enables you to apply your knowledge more efficiently, to identify any actual vulnerabilities.
