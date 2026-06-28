# Setting up your extension development environment manually

Source: https://portswigger.net/burp/documentation/desktop/extend-burp/extensions/creating/set-up/manual-setup
Fetched: 2026-06-28T09:15:47.241449+00:00

Support Center

Documentation

Desktop editions

Extending Burp

Extensions

Creating

Development environment setup

Manual setup

ProfessionalCommunity Edition

Setting up your extension development environment manually

Last updated:

June 18, 2026

Read time:

4 Minutes

You can set up your extension development environment to suit your preferences. This page covers the setup requirements and steps.

Note

If you want a faster setup, try our starter project. The project provides a ready-to-use template, so you can skip these steps and start coding immediately. For more information, see Setting up your extension development environment using the starter project.

Prerequisites

Before you begin:

Download a Java Integrated Development Environment (IDE). An IDE provides features like auto-completion and syntax highlighting to help streamline development. We recommend using IntelliJ IDEA (Community Edition), a free Java IDE.

To use an LLM to help you write your extension, install or access your preferred model. This tutorial uses Claude Code, as we provide a

CLAUDE.md file designed specifically for it. You can easily adapt the instructions for use with other LLMs. For more information on Claude Code, see the

Anthropic documentation.

Step 1: Create a new project

Set up a new project in your IDE with the following details:

Project type: Select Gradle or Maven. These build systems manage dependencies, simplifying project setup. If your IDE doesn't let you create a Maven or Gradle project directly, create a Java project and configure it to use Maven or Gradle as the build system.

Language: Java.

Gradle DSL: If you're prompted to choose a Gradle DSL, you can select either Groovy or Kotlin. This only impacts how you configure Gradle - not your Java extension code.

Java version: Use version 21. Depending on your IDE, this configuration option may be labeled as something like

JDK, SDK or JRE. Burp only supports extensions written in Java 21 or lower.

Step 2: Add the Montoya API dependency

Once your project is set up, add the Montoya API to your project's dependencies.

Gradle configuration

To add the Montoya API in a Gradle project:

Go to the Gradle build file.

Add the following inside the dependencies section:

For a Gradle DSL build.gradle file:

compileOnly "net.portswigger.burp.extensions:montoya-api:LATEST-VERSION"

For a Kotlin DSL build.gradle.kts file:

compileOnly("net.portswigger.burp.extensions:montoya-api:LATEST-VERSION")

Update LATEST-VERSION with the latest Montoya API version number, available from the releases page on GitHub.

Sync the Gradle changes.

Maven configuration

To add the Montoya API in a Maven project:

Go to the pom.xml file.

Add the following inside the dependency block:

<dependency>

<groupId>net.portswigger.burp.extensions</groupId>

<artifactId>montoya-api</artifactId>

<version>LATEST-VERSION</version>

</dependency>

Update LATEST-VERSION with the latest Montoya API version number, available from the releases page on GitHub.

Update your Maven dependencies.

Step 3: Create your extension class

Create a Java class. This file will contain your extension code.

To create a new class file in your IDE:

Right-click the folder where you want to keep your code, typically src > main > java.

Select the option to create a new Java class. Depending on your IDE, this may be labeled as New > Java class or similar.

Enter a name for the class. For example, Extension.

Step 4: Confirm correct setup

To check that the project is correctly configured, attempt to build a JAR file. If the build is successful, you're ready to start writing.

For instructions, see Building a JAR file.

[Optional] Step 5: Enable LLM support

You can use an LLM to help you write your extension. To support this, we provide a CLAUDE.md file that includes essential context for the model. You can use this file with Claude Code or any other LLM.

Note

Make sure to review and test any code suggested by your LLM, as it may not always produce correct or secure output.

Claude Code support

To use Claude Code to help you write your extension:

Download our CLAUDE.md file and

supporting documentation from GitHub.

Add the CLAUDE.md file to the root of your extension project folder.

Create a docs folder in your extension project and add the supporting documentation inside it.

Open a terminal and navigate to your extension project folder.

Run Claude Code using the following command: claude.

Prompt Claude to create some code for your extension.

Claude should automatically read the contents of the ExtensionTemplateProject folder, including the CLAUDE.md file, then create draft code for you to review. If you think it hasn't read the CLAUDE.md file, directly prompt it to do so before continuing.

Other LLM support

To use an LLM other than Claude Code to help you write your extension, directly prompt the LLM to read the CLAUDE.md file and supporting documentation in the docs folder, or provide their contents as part of your context window.

Next steps

You're ready to start writing your extension. For a tutorial, see Writing your first extension.
