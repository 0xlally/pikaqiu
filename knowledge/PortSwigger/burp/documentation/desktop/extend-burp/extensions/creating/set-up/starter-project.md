# Setting up your extension development environment using the starter project

Source: https://portswigger.net/burp/documentation/desktop/extend-burp/extensions/creating/set-up/starter-project
Fetched: 2026-06-28T09:15:48.141366+00:00

Support Center

Documentation

Desktop editions

Extending Burp

Extensions

Creating

Development environment setup

Using the starter project

ProfessionalCommunity Edition

Setting up your extension development environment using the starter project

Last updated:

June 18, 2026

Read time:

3 Minutes

The starter project simplifies extension development using the Montoya API. Instead of setting up your development environment manually, you can download the ready-to-use template, open it in an IDE, and start coding immediately.

Prerequisites

Before you begin:

Download a Java Integrated Development Environment (IDE). An IDE provides features like auto-completion and syntax highlighting to help streamline development. We recommend using IntelliJ IDEA (Community Edition), a free Java IDE.

To use an LLM to help you write your extension, install or access your preferred model. This tutorial uses Claude Code, as the starter project includes a

CLAUDE.md file designed specifically for it. You can easily adapt the instructions for use with other LLMs. For more information on Claude Code, see the

Anthropic documentation.

Step 1: Download the template

To download the starter project:

In Burp, go to Extensions > APIs.

Click Download starter project.

Choose a location, then click Save.

The project is saved in a folder called ExtensionTemplateProject.

Step 2: Open the project

To open the project:

Open or import the ExtensionTemplateProject folder that you just saved in your IDE.

If prompted, follow any set up instructions. This may not be necessary as many IDEs automatically detect Gradle and configure the project.

Set the project Java version to 21. Depending on your IDE, this configuration option may be labeled as something like

JDK, SDK or JRE. Burp only supports extensions written in Java 21 or lower.

[Optional] Step 3: Rename the project

To rename the project:

Open settings.gradle.kts.

Change rootProject.name = "extension-template-project" to your preferred name.

Sync the Gradle changes.

[Optional] Step 4: Confirm correct setup

To check that the project is correctly configured, attempt to build a JAR file. If the build is successful, you're ready to start coding.

For instructions, see Building a JAR file.

[Optional] Step 5: Enable LLM support

You can use an LLM to help you write your extension. To support this, the starter project includes a CLAUDE.md file that provides essential context for the model.

To use this file with an LLM other than Claude Code, prompt the LLM to read the file and supporting documentation in the docs folder, or provide their contents as part of your context window.

To use the CLAUDE.md file with Claude Code:

Open a terminal and navigate to the ExtensionTemplateProject folder.

Run Claude Code using the following command: claude

Prompt Claude to create some code for your extension.

Claude should automatically read the contents of the ExtensionTemplateProject folder, including the CLAUDE.md file, then create draft code for you to review. If it doesn't, directly prompt it to read the file before continuing.

Note

Make sure to review and test any code suggested by the LLM, as it may not always produce correct or secure output.

Next steps

You're ready to start writing your extension. For a tutorial, see Writing your first extension.

Understanding the starter project

The project includes configuration and source files to help with extension development. The key file is Extension.java, where you implement your extension's functionality. This section breaks down its key components.

import burp.api.montoya.BurpExtension;

import burp.api.montoya.MontoyaApi;

public class Extension implements BurpExtension

{

@Override

public void initialize(MontoyaApi montoyaApi) {

montoyaApi.extension().setName("My Extension");

// Add your code here

}

}

The file contains the following essential components:

Imports

import burp.api.montoya.BurpExtension;

import burp.api.montoya.MontoyaApi;

These imports bring in two classes from the Montoya API, enabling your extension to communicate with Burp:

BurpExtension - Allows Burp to recognize your extension.

MontoyaApi - Gives access to Burp's features.

Main class

public class Extension implements BurpExtension

This defines the Extension class. It implements BurpExtension, which tells Burp this file contains an extension that it should load.

Initialize method

@Override

public void initialize(MontoyaApi montoyaApi) {

montoyaApi.extension().setName("My Extension");

// Add your code here

}

This method runs when Burp loads your extension. The montoyaApi argument provides access to Burp's functionality.

The line setName("My Extension") sets the name of your extension, as it appears in Burp's Extensions > Installed tab.

The @Override annotation ensures that initialize correctly implements the BurpExtension interface. This means that if you accidentally use an incorrect method name or argument, Java gives an error instead of failing silently.
