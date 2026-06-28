# Maintaining extensions on the BApp Store

Source: https://portswigger.net/burp/documentation/desktop/extend-burp/extensions/creating/bapp-store-maintaining-extensions
Fetched: 2026-06-28T09:15:46.967926+00:00

Support Center

Documentation

Desktop editions

Extending Burp

Extensions

Creating

Maintaining extensions on the BApp Store

ProfessionalCommunity Edition

Maintaining extensions on the BApp Store

Last updated:

June 18, 2026

Read time:

2 Minutes

Once your extension has been accepted into the BApp store, it may require occasional updates to maintain its quality and improve its functionality. To support this, please monitor your GitHub repository for any issues or feedback submitted by the community.

Note

We only accept pull requests from the extension's original repository. If you want to fix a bug in someone else's extension, submit a pull request to their fork first. They'll then need to raise a pull request to PortSwigger. For full instructions, see Troubleshooting extensions - Suggest a fix.

To update your extension:

Make changes to your extension's code in your original repository.

Create a pull request against PortSwigger's fork of your repository.

Raise an Update for existing extension issue on the extension-portal repository.

We'll review your changes. If they're approved we'll merge them into the PortSwigger fork. We'll then test the updated extension to make sure it works correctly before publishing it to the BApp Store.

If we have feedback, we'll provide it directly on the raised issue.

Using AI to support extension maintenance

You can use an LLM to help you make changes to your extension more efficiently. To support this, we provide a CLAUDE.md file that includes essential context on how Burp extensions are structured for the model.

Before you start, install or access your preferred LLM. These instructions use Claude Code, but you can adapt them for use with other models. For more information on Claude Code, see the Anthropic documentation.

To use Claude Code to update your extension

Download our CLAUDE.md file and

supporting documentation from GitHub.

Add the CLAUDE.md file to the root of your extension project folder.

Create a docs folder in your extension project and add the supporting documentation inside it.

Open a terminal and navigate to your extension's project folder.

Run Claude Code using the following command: claude

Prompt Claude to update your extension as required.

Review and test the AI-suggested updates.

Claude should automatically read the contents of the ExtensionTemplateProject folder, including the CLAUDE.md file, then create draft code for you to review. If you think it hasn't read the CLAUDE.md file, directly prompt it to read the file before continuing.

To use the CLAUDE.md file with an LLM other than Claude Code, prompt the LLM to read the file and supporting documentation, or provide their contents as part of your context window.

Note

Make sure to review and test any code suggested by the LLM before submitting it, as it may not always produce correct or secure output.
