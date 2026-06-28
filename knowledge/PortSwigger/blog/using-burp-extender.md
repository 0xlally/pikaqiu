# Using Burp Extender

Source: https://portswigger.net/blog/using-burp-extender
Fetched: 2026-06-28T09:15:26.788117+00:00

Using Burp Extender

Dafydd Stuttard |

Wednesday, 8 April 2009 at 20:08 UTC

burp extender

From time to time, people ask me for help getting their code working with Burp Extender, so here is a quick worked example of how to do this. The example is based on a plugin written by Daniele Costa, which extracts HTML comments from HTTP responses, and writes these to file and to the command line.

The core of the plugin code is simple. It implements the processProxyMessage method in IBurpExtender, to get a handle to all requests and responses passing through Burp Proxy. For response messages, it checks whether the requested URL is in scope, and if so uses a regular expression to match any HTML comments within the response. Anyone with some basic Java skills can create code like this. What may be less familiar is actually getting your code to load and run within Burp.

The steps to compile and run the plugin are as follows:

If you don't already have it, download and install the Java Development Kit (JDK) from Sun.

Create a directory to work in, and cd into it from the command line.

Copy the plugin source file (BurpExtender.java) into your working directory.

Create a subdirectory called "burp", and copy the IBurpExtenderCallbacks.java file into this directory. You will need this file in the correct relative path, because the plugin code makes use of the IBurpExtenderCallbacks interface.

In your working directory, compile the BurpExtender.java source file into a .class file using javac, the Java compiler. The exact command will depend on the location of your JDK - for example, on Windows, you might type: "\Program Files\Java\jdk1.6.0_04\bin\javac.exe" BurpExtender.java

Confirm that the file BurpExtender.class has appeared in your working directory.

Build a Java archive (JAR) file containing your .class file. Depending again on your JDK location, you might type: "\Program Files\Java\jdk1.6.0_04\bin\jar.exe" -cf burpextender.jar BurpExtender.class

Confirm that the file burpextender.jar has appeared in your working directory.

Copy your normal Burp JAR file into your working directory.

Using the actual name of your Burp JAR file, start Burp using the command: java -Xmx512m -classpath burpextender.jar;burp.jar burp.StartBurp

If everything works, Burp should launch with a number of entries in the alerts tab, confirming which IBurpExtender methods were successfully loaded from your plugin (in this case, processProxyMessage and registerExtenderCallbacks):

To make use of the actual functionality of this plugin, you simply need to add the domains that interest you to Burp's Target Scope, and then browse to them via Burp Proxy. Any HTML comments contained within in-scope responses will be printed to the command line, and saved to a file in your working directory.

burp extender

Dafydd Stuttard

@DafyddStuttard

Latest Posts

Burp Extensibility 2026: Awards, Talks, and Highlights

19 June 2026

Burp Extensibility 2026: Awards, Talks, and Highlights

The beast needs a cage: What's next for AppSec post-Mythos

12 May 2026

The beast needs a cage: What's next for AppSec post-Mythos

3 ways custom scan checks turn practitioner knowledge into scalable automation

01 May 2026

3 ways custom scan checks turn practitioner knowledge into scalable automation

Senior pentesters have a deeply refined intuition about what is vulnerable in an environment. The problem? That expertise is often siloed with an individual and trapped in their notes or Python scripts.
