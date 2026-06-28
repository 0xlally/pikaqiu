# Content discovery

Source: https://portswigger.net/burp/documentation/desktop/tools/engagement-tools/content-discovery
Fetched: 2026-06-28T09:16:03.242262+00:00

Support Center

Documentation

Desktop editions

Tools

Engagement tools

Content discovery

Professional

Content discovery

Last updated:

June 18, 2026

Read time:

4 Minutes

Use this function to discover content and functionality that is not linked from visible content that you can browse to or Burp Scanner can crawl.

To use this function:

Select an HTTP request from anywhere in Burp.

Right-click and select Engagement tools > Discover content.

To start the discovery session, click Session is not running.

Burp uses several techniques to discover content, including:

Name guessing.

Web crawling.

Extrapolation from naming conventions that the application uses.

You can see the discovered content in a site map for the discovery session. You can also add this content to the main suite site map.

Control tab

The Control tab shows you the current status of the discovery session. Use the toggle button to pause and restart the session.

You can see the following information:

Requests made.

Bytes transferred in server responses.

Network errors.

Discovery tasks queued.

Spider requests queued.

Responses queued for analysis.

The Queued tasks table shows the discovery tasks that are queued. The discovery engine works recursively. When a new directory or file is discovered, the discovery engine derives further tasks, depending on the configuration. For example:

When Burp discovers a new directory, it may add tasks to look for sub-directories and files within the directory.

When Burp discovers a new file, it may add a task to check for the same base filename with different file extensions.

New tasks are prioritized by how likely they are to discover new content.

Config tab

Use the Config tab to configure the content discovery:

Target

The Target settings enable you to define the start directory for the content discovery session, and to define which files or directories are targeted. The following options are available:

Start directory - Enter the URL where Burp starts to look for content. Items are only requested within this path and its subdirectories.

Discover - Specify whether the session looks for files, directories, or both. If you look for directories, you can choose whether to look for subdirectories inside any directories that are found. You can also choose how many levels of subdirectory to look for.

Filenames

You can configure the sources that Burp uses to generate filenames to test:

Built-in short file list.

Built-in short directory list.

Built-in long file list.

Built-in long directory list.

Custom file list.

Custom directory list.

Names observed in use on target site - Enable this setting to list the directories and filename stems that Burp discovers on the target site. Burp checks for these in each new directory that it tests.

Derivations based on discovered items - Burp attempts to guess item names based on items that it discovers. For example, if Burp discovers the directory AnnualReport2018, it also checks for AnnualReport2019, AnnualReport2020, and so on.

File extensions

Use the File Extensions settings to configure how the discovery session adds file extensions to file stems. Burp uses the Filenames settings to derive the file stems. When Burp tests each file stem, it checks for different file extensions based on these settings:

Test these extensions - Configure a list of extensions that Burp always checks for. You can fine-tune the default list based on the technologies known to be in use on the target application.

Test all extensions observed in use on target site, except for: - Configure a list of extensions that you don't want to check for, even if they are found to be in use.

Test these variant extensions on discovered files - Configure a list of extensions that Burp checks for, using the stems of discovered filenames. This is useful if you want to check for backup copies of existing files.

Test file stems with no extension - Burp checks for each file stem with no extension added.

Discovery engine

Use these settings to control the engine that is used to make HTTP requests during the discovery session. You can also control how it interacts with the suite site map. The following settings are available:

Case sensitivity - Choose whether Burp handles filenames as case-sensitive. If you select Auto-detect, Burp initially treats content as case-sensitive. When it discovers the first new item, it tests the server's treatment of case variations. Burp uses the response to this treatment to decide whether to handle further filenames as case-sensitive.

Add discovered content to suite site map - Automatically add new items to the main site map as they're discovered.

Copy content from suite site map - Copy existing content from the main suite site map into the discovery site map. This may provide a stronger starting point for the discovery of new content.

Spider from discovered content - Configure the discovery session to perform conventional web crawling. The session processes the responses to discovery requests and looks for links to additional new content.

Number of discovery threads - Control the number of concurrent requests the discovery engine is able to make.

Number of spider threads - Control the number of concurrent requests the crawling function is able to make.

Site map tab

The discovery session uses its own site map, which shows all the discovered content within the defined scope. This is shown in the content discovery window Site map tab.

You can add the discovered content to the main site map. To do this, select Add discovered content to suite site map in the Discovery Engine section of the Config tab.

Related pages

To learn how to use Burp Intruder to carry out customized content discovery, see Enumerating identifiers.
