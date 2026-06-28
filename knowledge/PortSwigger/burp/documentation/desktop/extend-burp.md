# Extending Burp

Source: https://portswigger.net/burp/documentation/desktop/extend-burp
Fetched: 2026-06-28T09:15:45.799362+00:00

Support Center

Documentation

Desktop editions

Extending Burp

ProfessionalCommunity Edition

Extending Burp

Last updated:

June 18, 2026

Read time:

2 Minutes

Burp Suite offers powerful options for customizing and extending its functionality. These options enable you to adapt Burp to your unique testing workflow - from lightweight enhancements to full-featured automation. You can combine the different extensibility options to meet your unique testing needs.

Bambdas

Bambdas are snippets of code that run directly from Burp Suite's interface.

You can use Bambdas to:

Customize match-and-replace rules.

Add custom table columns.

Filter tables.

Add custom actions for extracting, transforming, or analyzing data in HTTP messages in Burp Repeater.

You can import and use Bambdas that others have created or write your own. Because Bambdas are embedded in Burp, they're often quick and simple to write - there's no need to set up a project or import the Montoya API.

Related pages

Bambdas

Importing Bambdas

Creating scripts

Custom scan checks

Custom scan checks enable you to extend Burp Scanner with your own vulnerability detection logic. Burp Scanner runs custom checks alongside its built-in scan checks, enabling you to extend scanning without writing a full extension.

You can import and use custom scan checks that others have created or write your own using Java or our easy-to-learn BCheck language.

Related pages

Custom scan checks

Creating custom scan checks

BCheck definitions

Extensions

Extensions are flexible and powerful plugins. They're best for complex functionality as they give you more control over Burp's behavior and interface.

You can use extensions to, for example:

Modify traffic handling.

Integrate external tools.

Interact with Burp's internal tools.

Extend Burp's user interface.

You can install community-created extensions from the BApp Store with a single click, or manually install custom extensions that have been shared with you.

You can also create your own extensions. To help you get started, we've created a starter project with everything you need to begin developing your own extensions, including dependencies and starter code.

Related pages

Extensions

Installing extensions

Creating extensions
