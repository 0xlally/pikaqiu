# Loading your extension in Burp

Source: https://portswigger.net/burp/documentation/desktop/extend-burp/extensions/creating/loading-in-burp
Fetched: 2026-06-28T09:15:46.986601+00:00

Support Center

Documentation

Desktop editions

Extending Burp

Extensions

Creating

Loading in Burp

ProfessionalCommunity Edition

Loading your extension in Burp

Last updated:

June 18, 2026

Read time:

3 Minutes

Once your extension is ready, follow these steps to build a JAR file and load it in Burp Suite.

Note

To ensure compatibility with the latest Montoya API changes and access new features, always use the latest version of Burp.

Step 1: Build the JAR file

To begin using your extension, you first need to compile your code into a JAR file. This is the package that can be loaded into Burp.

Gradle build command

To build the JAR file using Gradle, run the following command in the root directory of your project:

For UNIX-based systems: ./gradlew jar

For Windows systems: gradlew jar

If successful, the JAR file is saved to <project_root_directory>/build/libs/<project_name>.jar.

Maven build command

To build the JAR file using Maven, run the following command in the root directory of your project: mvn clean package. This command works on all platforms.

If successful, the JAR file is saved to <project_root_directory>/target/<project_name>-<version>.jar.

Including third-party dependencies

If your extension uses third-party libraries, bundle those libraries into the JAR file. Otherwise, Burp can't find them when it loads the extension.

Note

Our starter project bundles dependencies for you by default. You only need to follow these steps if you set up your project manually. For more information about the starter project, see Setting up your extension development environment using the starter project.

To bundle dependencies using Gradle, add a tasks.jar block to your Gradle build file:

For a Kotlin DSL build.gradle.kts file:

tasks.jar {

duplicatesStrategy = DuplicatesStrategy.EXCLUDE

from(configurations.runtimeClasspath.get().filter { it.isDirectory })

from(configurations.runtimeClasspath.get().filterNot { it.isDirectory }.map { zipTree(it) })

}

For a Groovy DSL build.gradle file:

tasks.named('jar') {

duplicatesStrategy = DuplicatesStrategy.EXCLUDE

from configurations.runtimeClasspath.findAll { it.isDirectory() }

from configurations.runtimeClasspath.findAll { !it.isDirectory() }.collect { zipTree(it) }

}

After you sync the Gradle changes, the next build includes your dependencies in the output JAR.

Tip

Most Java IDEs include Gradle plugin integrations that can build the JAR for you. Check your IDE's documentation for details.

Step 2: Load the JAR file in Burp

To load the JAR file into Burp:

In Burp, go to Extensions > Installed.

Click Add.

Under Extension details, make sure that Java is selected as the Extension type.

Click Select file.

Select the JAR file you just built, then click Open.

[Optional] Select Reload extension automatically when file changes. Burp will now reload your extension whenever you rebuild the JAR file.

[Optional] Under Standard output and Standard error, choose where to save output and error messages.

Click Next to load the extension into Burp.

Review any messages displayed in the Output and Errors tabs.

Click Close.

Your extension is listed in the Burp extensions table. You can test its behavior and change the code as necessary.

Reloading your extension

When you change your extension's code, you need to reload the extension in Burp for the changes to take effect. You have two options:

Reload automatically when file rebuilt (recommended)

Reload manually

Reload automatically when file rebuilt

Burp can reload your extension automatically whenever you rebuild the JAR file. This is the easiest way to keep your extension up to date during development.

To enable automatic reload:

In Burp, go to Extensions > Installed.

Under Auto-reload, select the checkbox for your extension.

Rebuild your JAR file. For instructions, see Build the JAR file.

Burp reloads the extension automatically whenever the file changes.

Reload manually

If you prefer manual control, you can quickly reload the extension yourself:

In Burp, go to Extensions > Installed.

Hold Ctrl or Cmnd and select the Loaded checkbox next to your extension.

Sharing your extension

We'd love to see what you've created!

Share your extension on our PortSwigger Discord #extensions channel to get feedback, showcase your work, and connect with other developers.

Then take it to the next level by submitting your extension to the BApp store, making it available to the community of 80,000+ testers worldwide. For guidance on the submission process, see Submitting extensions to the BApp store.
