# Creating Burp extensions

Source: https://portswigger.net/burp/documentation/desktop/extend-burp/extensions/creating
Fetched: 2026-06-28T09:15:46.575143+00:00

Support Center

Documentation

Desktop editions

Extending Burp

Extensions

Creating

ProfessionalCommunity Edition

Creating Burp extensions

Last updated:

June 18, 2026

Read time:

3 Minutes

Burp extensions are flexible and powerful plugins that enable you to customize Burp Suite to suit your workflow.

You can create your own extensions in Java using our Montoya API. This enables you to, for example:

Add new security testing features.

Modify traffic handling.

Integrate external tools.

Interact with internal Burp tools.

Extend Burp's user interface.

Exploring your idea

Before you begin development, refine your idea and gather inspiration:

Browse the BApp store - Check the list of BApps. You may find one that already meets your needs.

Look at example extensions - Explore example extensions in the Montoya API examples GitHub repository. These showcase different ways to extend Burp.

Join the conversation - Connect with other extension developers on the PortSwigger Discord #extensions channel.

Review our acceptance criteria - If you plan to submit your extension to the BApp store, check our BApp store acceptance criteria before you begin.

Choosing the right extensibility option

Burp offers different customization options depending on your needs:

Bambdas are best for customizing match-and-replace rules, table columns, or custom filters. Bambdas are small sections of Java-based code that run directly in Burp, making them easier to write as they don't require project setup or UI configuration. For more information, see

Creating scripts.

BChecks are best for defining custom scan checks. BChecks use an easy-to-learn, purpose-built language to create tailored checks. They provide a way to extend Burp Scanner without requiring a full extension. For more information, see Creating custom scan checks.

Extensions are best for complex functionality. They offer greater flexibility but require additional setup. To help you get started, we provide a starter project for managing dependencies and development.

Choosing a language

We strongly recommend writing Java-based extensions that use the Montoya API. This modern API gives you full access to Burp's extensibility features. It's actively maintained, well-documented, and designed to be easy to work with. All of our documentation and examples are written in Java using the Montoya API.

You can also write extensions in Kotlin, which can be compiled into a .jar file and loaded in Burp like a Java extension.

Note

You can also write extensions in Python (via Jython) or Ruby (via JRuby) using the legacy Extender API. Please be aware that the Extender API is no longer actively maintained.

For examples that use the legacy Extender API, see Extender API examples (Legacy).

Creating AI-powered extensions

The Montoya API enables you to integrate advanced AI features into your Burp Suite extensions. Your extensions can now send prompts to a Large Language Model (LLM), allowing real-time input analysis and intelligent responses.

More information

For more information, see Creating AI extensions.

Vibe coding extensions with AI

LLMs can help you create Burp extensions more quickly and easily. To support this, our extension starter project includes a

CLAUDE.md file. The file is created for use with Claude Code, but can be used with other LLMs. It provides the LLM with essential context on the Montoya API and Burp extension development.

Related pages

For setup instructions, including how to use the CLAUDE.md file, see:

Setting up your extension development environment using the starter project.

Setting up your extension development environment manually.

Handling kettled HTTP/2 requests in extensions

When issuing new requests from your extension, you're free to send kettled requests using HTTP/2 formatting. This enables you to develop extensions to test for HTTP/2-exclusive vulnerabilities.

However, it is not currently possible for extensions to modify kettled requests that were issued by Burp. This is because the API only allows them to access the normalized, HTTP/1 style request representation.

Custom editor best practice

Make sure that any ExtensionHttpRequestEditor returned does not use an HttpRequestEditor as the UI component when it registers an HttpRequestEditorProvider. This avoids a scenario where the HttpRequestEditor is created within another HttpRequestEditor, potentially creating an infinite loop of HttpRequestEditor components and causing Burp to crash.

For the same reason, avoid returning an HttpResponseEditor when registering an HttpResponseEditorProvider.

In this section

Setting up your extension development environment.

Writing your first extension

Extension tutorials

Loading your extension in Burp.

Setting up remote debugging.

Submitting extensions to the BApp store.

Maintaining extensions on the BApp Store.

BApp store acceptance criteria.

Extender API examples
