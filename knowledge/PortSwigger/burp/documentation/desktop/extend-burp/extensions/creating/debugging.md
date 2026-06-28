# Setting up remote debugging for Burp extensions

Source: https://portswigger.net/burp/documentation/desktop/extend-burp/extensions/creating/debugging
Fetched: 2026-06-28T09:15:47.454624+00:00

Support Center

Documentation

Desktop editions

Extending Burp

Extensions

Creating

Setting up remote debugging

ProfessionalCommunity Edition

Setting up remote debugging for Burp extensions

Last updated:

June 18, 2026

Read time:

3 Minutes

Remote debugging involves attaching your IDE's debugger to a separate running instance of Burp Suite. This enables you to inspect your extension's execution within Burp in real time, making it easier to diagnose issues and refine your extension's behavior.

This guide explains how to attach a debugger to Burp Suite's Java Virtual Machine (JVM) from your IDE.

Prerequisites

Before you begin, make sure you have set up the following:

A Burp extension project that is ready to be loaded into Burp.

A Java IDE that supports remote debugging. We recommend using IntelliJ IDEA (Community Edition), a free Java IDE, but these instructions work with other Java IDEs.

Note

We recommend running Burp and your IDE on the same machine for remote debugging.

Step 1: Configure a remote debugging session

To configure a remote debugging session in your IDE:

Open your Burp extension project in your IDE.

Create a new remote debugging configuration. Depending on your IDE, this may be labeled as something like Remote JVM Debug, SocketAttach, or Remote Java Application.

Configure the following connection details:

Port: Use 5005 by default. If another process is using this port, select an alternative, for example 5006. Make sure you use this port when launching Burp.

Host: Use localhost by default. If your IDE and Burp are running on different machines, change this to the IP address of the machine running Burp.

Save the configuration.

Your IDE is ready to connect to Burp's running JVM.

Step 2: Start Burp with remote debugging enabled

Launch Burp with remote debugging enabled by running the following command in a terminal:

java -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address="*:5005" -jar "FILE_PATH.jar"

Modify the command as follows:

FILE_PATH.jar - Replace with the actual path to Burp's JAR file. To find your file path:

In Burp, go to Help > Diagnostics. The Burp Suite diagnostics dialog opens.

Locate the java.class.path property. The value of this property is the file path.

5005 - This should be 5005 by default, but if you specified a different port in your IDE's debug configuration, update this value.

After running this command, Burp will start as usual but will listen for debugger connections.

Step 3: Attach your debugger to Burp

Now that Burp is running with remote debugging enabled, attach your IDE's debugger to it:

In your IDE, select the remote debugging configuration you created earlier.

Start the debugger to attach it to Burp.

Build and load your extension in Burp. If your extension is already loaded in Burp, rebuild and reload it. This ensures that the code in your IDE matches the compiled code Burp is running. For instructions on loading your extension in Burp, see Loading your extension in Burp.

The debugger is now attached to Burp. You can begin debugging your extension. To learn how to set breakpoints and debug your extension, see

Debugging extensions with a remote debugger.

Note

We recommend disabling all other installed extensions so that you can test this extension in isolation. This helps prevent unexpected behavior caused by interactions with other extensions.

Troubleshooting

If the debugger fails to attach, try the following:

Make sure that port 5005 (or your selected port) is not blocked or already in use by another process. If it is, select another port and update both your startup command and debug configuration.

Make sure that you started Burp with remote debugging enabled before attempting to attach your debugger to Burp.

If execution doesn't pause at your breakpoints, rebuild and reload your extension to make sure that the source code in your IDE matches the compiled code Burp is running. For more troubleshooting steps, see Debugging Burp extensions with a remote debugger.
