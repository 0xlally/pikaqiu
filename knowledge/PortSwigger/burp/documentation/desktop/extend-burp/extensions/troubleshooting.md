# Troubleshooting Burp extensions

Source: https://portswigger.net/burp/documentation/desktop/extend-burp/extensions/troubleshooting
Fetched: 2026-06-28T09:15:48.625241+00:00

Support Center

Documentation

Desktop editions

Extending Burp

Extensions

Troubleshooting

ProfessionalCommunity Edition

Troubleshooting Burp extensions

Last updated:

June 18, 2026

Read time:

9 Minutes

This guide helps you resolve common issues when using Burp extensions.

If the troubleshooting steps in this guide don't resolve your issue, please contact our support team at support@portswigger.net.

Installing extensions

You can't access the BApp Store in Burp

To access extensions from the BApp Store in Burp, your device must be able to access portswigger.net. You might not be able to access extensions because:

You're offline.

Your network requires an upstream proxy.

An intercepting proxy is intercepting and resigning traffic with its own certificate. Burp doesn't trust self-signed certificates by default, so it blocks the connection.

If you're working offline in Burp, you can use a separate browser to download extensions from our website, then install them manually. For more information, see Installing extensions manually.

Step 1: Check your internet connection

Make sure your computer is connected to the internet. To verify this, open an external browser and try visiting https://portswigger.net. If you can't access the site, check your network settings or contact your administrator.

Step 2: Configure an upstream proxy

Some networks require an upstream proxy for internet access. If your network requires one, configure Burp to use it:

In Burp, click Settings. The Settings dialog opens.

Go to Network > Connections.

Under Upstream proxy servers, click Add. The Add upstream proxy rule dialog opens.

Enter the details of the upstream proxy. For more information, see Connections settings - Upstream proxy servers.

Click OK.

The upstream proxy rule is added to the table.

Step 3: Identify and resolve an intercepting proxy

Some networks use intercepting proxies, such as ZScaler, to inspect and decrypt encrypted traffic. These proxies intercept HTTPS connections and re-sign certificates, which means Burp won't trust the connection.

To check if an intercepting proxy is impacting your connection:

In Burp's browser, go to https://portswigger.net/bappstore.

In Burp, go to Settings > Network > TLS.

Under Server TLS certificates, find the entry for portswigger.net.

Check the issuer of the certificate:

If the issuer is a well-known CA provider such as Amazon, it's unlikely that an intercepting proxy is interfering with the connection.

If the certificate is issued by an intercepting proxy (such as ZScaler), or your company's security system, then your traffic is being intercepted.

If your traffic is being intercepted by a proxy, Burp might not trust the proxy's certificate. This can prevent access to the BApp Store.

To fix this, add the proxy's certificate authority (CA) to Burp's trusted certificates:

Find the path to the proxy's certificate. If you're unsure, check your system settings or ask a network administrator.

In Burp, go to Settings > Network > TLS.

Under Custom CA certificates, click Add.

Select the certificate file.

Restart Burp, then check whether you can access the BApp Store.

You can't install extensions from the BApp Store in Burp

If you can't install an extension from the BApp Store, the Install button is grayed out. This may be because:

You need to update Burp.

You need to install Jython or JRuby.

You need to upgrade to Burp Suite Professional.

You need to update Burp

Some extensions require features or API methods that were introduced in newer versions of Burp. To update Burp:

Click the Help top-level menu.

Select Check for updates. A dialog opens with details of the latest Burp version.

Click Update now.

Wait for Burp to prepare the update. When it's ready, you'll be prompted to restart. Click Update and restart to complete the process.

When Burp restarts, return to Extensions > BApp store to download your extension.

You need to configure Jython or JRuby

To use an extension that is written in Python or Ruby, you'll need to configure Jython or JRuby. Burp is a Java application and requires Java-compatible implementations of these languages to run the extension code.

To configure Jython or JRuby:

Download the Jython standalone JAR file or the

Ruby JAR file.

In Burp Suite, click Settings to open the

Settings dialog.

Go to Extensions.

Under Python Environment or Ruby Environment, click Select file.

Select the downloaded JAR file and click Open.

Once configured, return to Extensions > BApp Store, click , select Refresh list, then download your extension.

Related pages

Extensions settings.

You need to upgrade to Burp Suite Professional

Some extensions require Burp Suite Professional features. If you're using Burp Suite Community edition, you must upgrade to install these extensions.

For more information, see Upgrade to Burp Suite Professional.

An extension isn't working as expected

If an extension is installed but not working properly, try the following steps to investigate the issue.

Step 1: Update Burp

It's best practice to run extensions on the latest version of Burp. If an extension requires features that were introduced in a newer version than the one you're using, it may not function correctly.

To update Burp:

Click the Help top-level menu.

Select Check for updates. A dialog opens with details of the latest Burp version.

Click Update now.

Wait for Burp to prepare the update. When prompted, click Update and restart to finish.

When Burp restarts, check that your extension is working as expected.

Step 2: Visit the extension's repository

All extensions in the BApp Store include a link to PortSwigger's fork of the author's GitHub repository. This may include additional documentation and troubleshooting information.

To access the author's GitHub repository:

In Burp, go to Extensions > BApp Store.

Select the extension you want to investigate.

In the description panel, scroll to Source and click the repository link.

Review the README file and any other resources in the repository.

Step 3: Use AI to review the extension's code

You can use an LLM to help you understand how the extension works and identify any bugs. To support this, we provide a CLAUDE.md file that includes essential context on how Burp extensions are structured for the model.

Before you start, you'll need to install or access your preferred LLM. These instructions use Claude Code, but you can adapt them for use with other LLMs. For more information on Claude Code, see the

Anthropic documentation.

Note

While we review all extensions submitted to the BApp Store, they are written by third parties and can run arbitrary code. We therefore can't guarantee their quality or safety.

Step 1: Access the extension code file

To access the extension's code:

In Burp, go to Extensions > BApp Store.

Select the extension you want to review.

In the description panel, scroll to Source and click the repository link.

In GitHub, if the repository was forked, click the Forked from link to access the original repository.

Fork the original repository to your own GitHub account.

Clone your forked repository to your local machine.

Open or import the local clone into your IDE.

Step 2: Run your LLM to analyze the extension

To use Claude Code to review the extension:

Download our CLAUDE.md file and

supporting documentation from GitHub.

Add the CLAUDE.md file to the root of the extension's folder.

Create a docs folder in the extension's folder and add the supporting documentation inside it.

Open a terminal and navigate to the extension's folder.

Run Claude Code using the following command: claude.

Prompt Claude to review the code, explain how to use the extension, and identify any bugs.

Claude should automatically read the contents of the ExtensionTemplateProject folder, including the CLAUDE.md file, then explain how the extension works. If you think it hasn't read the CLAUDE.md file, directly prompt it to do so before continuing.

Note

To use the CLAUDE.md file with an LLM other than Claude Code, prompt the LLM to read the file and supporting documentation, or provide their contents as part of your context window.

If you identify any issues with the extension's code, you can report this to the extension's author to fix.

Step 4: Report an issue or suggest a fix to the extension's author

PortSwigger doesn't maintain the community-created extensions in the BApp Store. If you believe you've found a bug or need support for a particular extension, please contact the extension's author through their repository.

To do this, you need to access the author's original extension repository:

In Burp, go to Extensions > BApp Store.

Select the extension you want to investigate.

In the description panel, scroll to Source and click the repository link.

If the repository was forked, click the Forked from link to access the original repository.

Option 1: Report an issue

If you don't have a proposed solution, you can still report the issue to make the extension's author aware of the problem:

In the extension author's original repository, click the Issues tab.

Review existing issues to see if the problem has already been reported.

If not, click New issue and describe the problem in detail, including:

The version of Burp Suite you're using.

The operating system.

Any relevant steps to reproduce the issue.

Screenshots or logs, if applicable.

Option 2: Suggest a fix

If you've identified the cause of the issue and have a proposed solution, you can suggest a fix. This may speed up the resolution process.

Note

You can optionally use an LLM to help identify and implement appropriate code changes. Make sure to review and test any code suggested by the LLM before submitting it, as it may not always produce correct or secure output. For LLM setup instructions, see

Step 3: Use AI to review the extension's code.

To suggest a fix:

Fork the extension author's original repository.

Make changes to the extension's code.

Create a pull request. In the description, clearly describe the problem and proposed fix, including:

The version of Burp Suite you're using.

The operating system.

Any relevant steps to reproduce the issue.

A summary of the changes introduced by your fix.

Screenshots or logs that support your solution, if applicable.

Performance issues

Burp has performance issues while using extensions

Extensions can cause Burp to run slowly. Extensions on the BApp Store aren't tested by PortSwigger for performance.

If you notice performance issues while using extensions, try the following troubleshooting steps:

Step 1: Disable unused extensions

Running too many extensions can slow Burp down. To minimize resource usage:

In Burp, go to Extensions > Installed.

In the Loaded column, uncheck any extensions you're not currently using.

Restart Burp.

Test Burp's performance.

Note

To estimate the total impact of installed extensions, go to the Extensions > Installed tab and check the Total estimated system impact indicator.

Step 2: View the performance impact estimate for particular extensions

Before testing an extension manually, you can get a general idea of its impact by checking the Estimated system impact ratings in the BApp Store.

Warning

These ratings are estimates only and may not fully reflect real-world performance. For example, we are unable to fully test extensions that add custom tabs or context menu options. The most reliable way to assess performance impact is to test extensions manually in Burp.

To check the expected system impact of a specific BApp Store extension:

Go to Extensions > BApp Store.

Select the extension and scroll down the right-hand panel to Estimated system impact.

Review the estimated impact across the following categories:

Memory - Potential impact on Burp Suite's memory usage.

CPU - Additional processing load on the CPU.

Time - Impact on Burp's overall speed. This includes the responsiveness of the interface and how long tools take to complete tasks.

Scanner - Potential increase in scan duration.

Overall - The highest impact rating among all categories.

Step 3: Manually test extensions

Extensions can impact performance individually, or the combination of extensions can cause a performance issue. Follow these steps to pinpoint the cause:

Disable all extensions:

In Burp, go to Extensions > Installed.

In the Burp extensions table, click anywhere in the list and press Ctrl + A or Cmd + A to select all extensions.

Right-click then select Unload. This unloads all your installed extensions.

Test Burp's performance without any extensions enabled.

In Extensions > Installed, re-enable extensions one at a time, starting with the ones you want to use immediately.

Test Burp's performance after enabling each extension. If Burp slows down, the recently enabled extensions may be causing the issue.

If Burp slows down after enabling multiple extensions, disable them selectively to identify conflicts.

I get an error message saying java.lang.OutOfMemoryError: Metaspace

You may see this error message if you load several Python or Ruby extensions, or if you unload and reload extensions multiple times.

To avoid this issue, configure Java to allocate more Metaspace storage:

Open a terminal or command prompt.

Add -XX:MaxMetaspaceSize=1G to the command you use to launch Burp, as follows:

java -XX:MaxMetaspaceSize=1G -jar FILE_PATH.jar

Related pages

Launching Burp Suite from the command line
