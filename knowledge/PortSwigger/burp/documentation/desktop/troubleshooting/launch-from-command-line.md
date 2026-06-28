# Launching Burp Suite from the command line

Source: https://portswigger.net/burp/documentation/desktop/troubleshooting/launch-from-command-line
Fetched: 2026-06-28T09:16:09.936985+00:00

Support Center

Documentation

Desktop editions

Troubleshooting

Launch from the command line

ProfessionalCommunity Edition

Launching Burp Suite from the command line

Last updated:

June 18, 2026

Read time:

3 Minutes

Burp Suite is a Java application and is distributed via native platform installers. However, Burp is also available as a standalone Java executable file, with the .jar extension. You can choose to download the JAR file from the same download page as the native platform installers.

The Burp JAR file can be executed using a Java Runtime Environment, and there is no need to unpack the contents of the JAR file itself. Launching Burp directly from the command line is beneficial in certain use cases because you can use command line arguments to control Burp's behavior on startup. For example, you can specify exactly how much memory your computer assigns to Burp.

Note

The native platform installers bundle Burp together with a private Java Runtime Environment, so you don't need to worry about installing or updating Java manually. However, if you choose to launch Burp from the command line, you need to manage your own Java installation and updates. The minimum Java version required to run Burp is Java 21.

Note that any extensions written in a version of Java higher than 21 may not run correctly on any installation of Burp Suite.

Checking your Java version

To check your Java version:

At a command prompt, type: java -version

If Java is installed, a message indicates which version you have. To run Burp, you need at least Java 21.

If Java is not installed, or if your version of Java is older than 21, you need to install a supported version of Java. Download the Java Runtime Environment (JRE) from Oracle and run the installer. Then open a new command prompt and start again.

Launching the Burp Suite JAR

Once you have the correct Java version installed, you can launch Burp by entering a command such as the following:

java -jar -Xmx4g /path/to/burp.jar

In this example, the argument -Xmx4g specifies that you want to assign 4GB of memory to Burp. /path/to/burp.jar is the path to the location of the JAR file on your computer.

If everything is working, a splash screen should display for a few seconds, and then the main startup wizard window should appear. If nothing happens, or if an error message appears, please refer to the troubleshooting help.

Command line arguments

Various command line arguments are available to control Burp's behavior on startup. For example, you can tell Burp to prevent reloading of extensions, open a particular Burp project file, or load a particular configuration file.

You can view a list of available options using the command line argument --help. The following arguments are currently available:

Argument

Description

--help

Print this message.

--disable-extensions

Prevent loading of extensions on startup.

--diagnostics

Print diagnostic information.

--use-defaults

Start Burp with the default settings. Warning: Setting this flag overwrites your saved settings with Burp's default settings and you will not be able to recover them.

--collaborator-server

Run in Collaborator server mode.

--collaborator-config

Specify a Collaborator server configuration file to use. By default, this will load the file collaborator.config.

--project-file

Open the specified project file. This will be created as a new project if the file does not exist.

--config-file

Load the specified project configuration file. This option may be repeated to load multiple files.

--user-config-file

Load the specified user configuration file. This option may be repeated to load multiple files.

--auto-repair

Automatically repair a corrupted project file specified by the --project-file option.

--unpause-spider-and-scanner

Do not pause the Spider or Scanner when opening an existing project.

-Djava.awt.headless=true

Open Burp in headless mode.

-Xmx4g

Limit Burp's heap size to 4GB, for example. You can change this to a different value if you want.

-50:MaxRAMPercentage

Limits the maximum RAM used by Burp, for example to 50% of the total system memory.
