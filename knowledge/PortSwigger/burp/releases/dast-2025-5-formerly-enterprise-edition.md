# DAST 2025.5 (formerly Enterprise Edition)

Source: https://portswigger.net/burp/releases/dast-2025-5-formerly-enterprise-edition
Fetched: 2026-06-28T09:16:13.720244+00:00

This release renames Burp Suite Enterprise Edition to Burp Suite DAST, and enables you to add tags to your sites and folders. We also made some other improvements, and fixed a bug.

Burp Suite DAST

We've renamed Burp Suite Enterprise Edition to Burp Suite DAST, a clearer name for the industry’s most accurate and scalable dynamic application security testing (DAST) solution.

This change helps eliminate confusion between Burp Suite Professional and our enterprise-grade DAST product. But rest assured, nothing about your experience is changing.

Learn why we made the change and what’s next for Burp Suite DAST in our latest blog post.

Tags for sites and folders

You can now add tags to your sites and folders. Tags are a really useful way to organize your sites:

Filter your sites and folders by tags.

Add descriptions to your tags, such as region, owner, or importance.

To learn more about using tags, see Adding tags to sites.

Crawl and audit now run in parallel during scans

Burp Scanner now begins auditing as soon as the first audit item is identified during the crawl. As additional items are discovered, Burp continuously reprioritizes the audit queue to ensure that the most valuable items are audited first.

This improves scan efficiency and enables earlier issue detection, especially in larger or more complex applications.

Click all pointer clickable elements

We've added a new custom crawling configuration setting that enables Burp Scanner to click all elements that are styled with a pointer cursor (for example, using cursor: pointer). This can help identify interactive elements that are not standard links or buttons.

Bug fix

For API users, we fixed a bug where change_history wasn't populated if GetScanIssues was requested without false_positive_username.

Java update

We updated Java Runtime to 21.0.7, and Azul Zulu to 21.42.19.
