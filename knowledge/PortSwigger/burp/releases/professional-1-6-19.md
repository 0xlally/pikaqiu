# Professional 1.6.19

Source: https://portswigger.net/burp/releases/professional-1-6-19
Fetched: 2026-06-28T09:16:27.199478+00:00

This release introduces some major enhancements to the Target site map.

The site map now includes both the contents of the target application and discovered Scanner issues. The Results tab that appeared within the Scanner tool has now been removed, and all Scanner results reside within the site map.

You can choose to view site map contents and issues within separate tabs:

or side-by-side:

This best option may depend on the size of your screen, and can be made via the site map context menu:

Within the tree view of the site structure, the icons now include an indication of the most significant issue that has been found within each branch or node of the tree, so you can quickly identify the parts of the application where vulnerabilities exist:

You can open additional site map windows, via the context menu:

Each window provides a separate view into the same underlying data. You can use this feature to easily keep an eye on different selected portions of a target application while you are working:

Or you can define different view filters on each site map window:

The new single integrated view of contents and issues should make it easy to track all relevant information capture about a target, and simplify typical testing workflows. Over time, we will be adding some more capabilities to the site map, to help drive common testing actions.

Two consequences of the change to the site map are worth noting:

In terms of saving and loading Burp's state, issues reported by the Scanner now reside within the Target tool. So if you want to save or reload a state file that includes your Scanner issues, be sure to leave the box checked for the Target tool.

The global search function no longer has an option to include the Scanner tool. Searches of the Target tool will include results for matching Scanner issues within the site map.

Some bugs were also fixed in this release:

A bug affecting reporting of XXE issues in certain very unusual situations.

A bug affecting synchronized selection of tree nodes within the compare site maps function.

A bug which prevented global hotkeys from working in detached tool windows.
