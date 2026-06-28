# Writing your first Burp Suite extension

Source: https://portswigger.net/blog/writing-your-first-burp-suite-extension
Fetched: 2026-06-28T09:15:28.657565+00:00

Writing your first Burp Suite extension

Dafydd Stuttard |

Thursday, 13 December 2012 at 11:08 UTC

burp extender

The new Burp Suite extensibility makes it much easier for non-programmers to create and use Burp extensions. This post explains the basics, and we'll soon be releasing a series of examples of Burp's extensibility in action.

You can create Burp extensions using Java or Python. For your first extension, you should choose the language that is most familiar to you. If you've used other compiled languages like C# or Visual Basic, then Java is probably the best place to start. If you've used other interpreted languages like Perl or Ruby, then start with Python.

Java

If you don't have one already, download and install an IDE that supports Java, such as Netbeans or Eclipse.

Create a new empty project, with whatever name you like.

Within the project, create a package called "burp".

Use Burp Suite to export the latest Burp Extender interface files. You can do this at Extender / APIs / Save interface files. Save the interface files into the folder that was created for the burp package.

Within the burp package, create a new Java class called "BurpExtender". Copy the following into the source code file:

package burp;

public class BurpExtender implements IBurpExtender

{

public void registerExtenderCallbacks(

IBurpExtenderCallbacks callbacks)

{

// your extension code here

}

}

This empty extension does absolutely nothing at all, but you can still compile it and load it into Burp, just to see how things work.

Build the project, and find the location of the JAR file that was created by the IDE (usually in a folder called "dist").

In Burp (v1.5.01 or later), go to the Extender tool, and the Extensions tab, and add a new extension. Select the extension type "Java", and specify the location of your JAR file.

If all is well, the empty extension will load into Burp with no error messages.

If you wish, you can download a Netbeans project containing all of the code for the empty extension.

Python

You can create Python extensions using a Python-capable IDE, or you can use any text editor, such as Notepad on Windows.

Create a file, with whatever name you like, using the ".py" file extension. Copy the following into the source code file:

from burp import IBurpExtender

class BurpExtender(IBurpExtender):

def registerExtenderCallbacks(self, callbacks):

# your extension code here

return

This empty extension does absolutely nothing at all, but you can still load it into Burp, just to see how things work.

Before running a Python extension, you will need to download Jython (the standalone JAR version), and configure Burp with its location (at Extender / Options / Python environment).

Then, go to the Extensions tab, and add a new extension. Select the extension type "Python", and specify the location of your file.

If all is well, the empty extension will load into Burp with no error messages.

Note: Because of the way in which Jython dynamically generates Java classes, you may encounter memory problems if you load several different Python extensions, or if you unload and reload a Python extension multiple times. If this happens, you will see an error like:

java.lang.OutOfMemoryError: PermGen space

You can avoid this problem by configuring Java to allocate more PermGen storage, by adding a XX:MaxPermSizeoption to the command line when starting Burp. For example:

java -XX:MaxPermSize=1G -jar burp.jar

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
