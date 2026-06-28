# Installing extensions from the BApp Store

Source: https://portswigger.net/burp/documentation/desktop/extend-burp/extensions/installing/bapp-store
Fetched: 2026-06-28T09:15:48.590151+00:00

Support Center

Documentation

Desktop editions

Extending Burp

Extensions

Installing extensions

BApp Store

ProfessionalCommunity Edition

Installing extensions from the BApp Store

Last updated:

June 18, 2026

Read time:

3 Minutes

The BApp Store contains community-created extensions that you can install directly from Extensions > BApp

Store in Burp with a single click.

We review all extensions submitted to the BApp Store, but as they are written by third parties, we can't guarantee their quality or security. We recommend that you review the code yourself before installing. To view the source code for an extension, visit our GitHub page.

For more information about how we protect your data when you use AI-powered extensions, see the Burp AI trust and compliance FAQ.

Note

If you're working offline in Burp, you won't be able to access the BApp Store. In this situation, you can use a separate browser to download extensions from our website and install them manually. For more information, see Installing extensions manually.

If you can't access the BApp Store for any other reason, see our troubleshooting guide.

Finding extensions

To find the right extension in the BApp store, you can filter the Extensions > BApp Store table:

Search the table - Click Search and enter a keyword or phrase.

Filter the table - Use the buttons to filter based on the following categories:

Featured - Extensions that we recommend. These offer stand out functionality that we find particularly interesting.

Recently updated - Extensions that have been added or updated in the last three months.

PortSwigger created - Extensions developed by our team at PortSwigger.

You can also customize and sort the table contents. For more information, see Customizing Burp's tables.

Evaluating extensions

Each extension in the BApp Store includes the following information:

A description of what the extension does and how to use it.

Author - The community member who contributed the extension.

Version - The author's version number.

Source - A link to PortSwigger's fork of the author's GitHub repository, which contains the extension's source code. It may also contain additional usage information.

Updated - The date the extension was added or last updated.

Rating - A community rating based on user feedback.

Popularity - An indication of how widely used the extension is.

Estimated system impact - Ratings estimating the extension's performance potential impact:

Memory - Potential impact on Burp's memory usage.

CPU - Additional processing load on the CPU.

Time - Impact on Burp's overall speed. This includes the responsiveness of the interface and how long tools take to complete tasks.

Scanner - Potential increase in scan duration.

Overall - The highest impact rating among all categories.

Warning

The system impact ratings are estimates only and may not fully reflect real-world performance. For example, we are unable to fully test extensions that add custom tabs or context menu options.

Installing extensions

To install an extension from the BApp Store:

In Burp, go to Extensions > BApp Store.

Select an extension from the list.

Click Install.

The extension is automatically enabled and added to the bottom of the list in Extensions > Installed. Extensions process traffic in list order, so you may want to adjust their position. For instructions, see Managing extensions.

Note

See our troubleshooting guide in the following situations:

You can't install an extension.

You notice performance issues after installing the extension.

The extension isn't working as expected.

Related pages

For information on how to manage your extensions, including how to uninstall extensions, see Managing extensions.

If you can't find an extension that meets your needs, you might want to create your own. For more information, see Creating extensions. You could also consider using one of our other extensibility options. For more information, see Extending Burp.
