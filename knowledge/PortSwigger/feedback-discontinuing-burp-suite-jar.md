# Discontinuing the Burp Suite JAR to improve security  and performance

Source: https://portswigger.net/feedback-discontinuing-burp-suite-jar
Fetched: 2026-06-28T09:17:04.616008+00:00

Feedback wanted:

Discontinuing the Burp Suite JAR to improve security

and performance

We're considering removing the option to download

each version of Burp Suite as a standalone JAR file.

We're aware that some users may be impacted by this

change. To ensure that you have a chance to share any

concerns, we're reaching out to those who we think may

be affected.

We'll explore the reasons why we're looking into this

and explain why you might not need to use the JAR

after all. We'll also share workarounds for common JAR

use cases, including how to deploy a private

Collaborator server.

Finally, we'd like to give you the opportunity to

share your thoughts on whether this will work for you

so that we can take steps to mitigate the impact this

might have.

Why are we considering this change?

The following are some of the key reasons why we're

considering removing the JAR option from the

website.

Exposure through missed security updates

As every security professional knows, timely updates

are crucial for application security. Without them,

users run the risk of attackers using known

vulnerabilities to exploit them.

In particular, Burp's embedded Chromium browser

represents a significant attack surface and frequently

needs critical security updates. That's why we aim to

include the most recent stable version of Chromium

with each release of Burp, and even fast-track

releases just to update Chromium when necessary.

While analyzing the versions of Burp Suite in active

use, we noticed that the majority of versions with

unpatched vulnerabilities were running Burp from a

JAR. We suspect that this is largely due to the JAR

version lacking the auto-update functionality, meaning

you have to manually download a new JAR every time we

release.

If you use one of the standard, package-based

installations we provide for Linux, macOS, and Windows

respectively, you benefit from auto-updates, ensuring

that you never miss a security patch.

Use of insecure, outdated runtime environments

Our platform-specific installations include their own

Java Runtime Environment (JRE).

If you run Burp from a JAR file, you need to maintain

your own environment, which in practice means that

many JAR users are relying on older JREs. Not only is

this a common source of bugs and performance issues - a topic that we know is close to your heart

- it introduces another security weakness as you may

be exposed to known vulnerabilities in outdated JRE

versions.

Just like Burp Suite itself, if you use one of the

platform-specific installers and auto-updates, we keep

the JRE up to date on your behalf, ensuring the most

stable and secure experience.

Bloated file size

In addition to potential security and performance

issues, the JAR file also takes up excessive disk

space. Although the app itself runs on the

platform-agnostic JVM, the built-in Chromium browser

is platform-specific, meaning the all-in-one JAR

download contains three entire browsers, one for each

OS.

Our platform-specific installers are much leaner by

comparison, and only contain what's necessary for your

environment.

Customizing JVM settings without the JAR

Users often run Burp from a JAR so that they have

more granular control of the JVM. If this applies to

you, the good news is that you can still do this with

our installer-based versions of Burp.

Some options that were previously only available as

command-line arguments, such as being able to specify

how much memory is allocated to the JVM, you can now

control from the regular settings menu (Settings > Suite > Startup behavior >

Maximum Java memory usage).

Alternatively, you can pass all of the same arguments

to the JVM by creating an options file in the

installation directory. To do this:

Either download the relevant Burp Suite installer and run it, or go to your existing Burp Suite

installation directory. By default, you can find this

in the following location:

- Linux:  /home/<user>/BurpSuite

- macOS: /Users/<user>/Applications/Burp Suite

Professional

- Windows: C:\Program Files\BurpSuitePro

In the installation directory, locate the JAR

file.

In the same directory as the JAR, create a file

called user.vmoptions

In the user.vmoptions file, list all of the arguments that you normally

pass via the command line, separating each with a

newline.

From now on, when you launch the installed version of

Burp, it runs on the JVM using your specified

configuration.

Example

If you normally run:

java -Xmx4g -Xms128m

-Dsun.java2d.uiScale.enable=false -jar

/path/to/burp.jar

You can instead just create a user.vmoptions file with the following contents:

- Xmx4g

- Xms128m

- Dsun.java2d.uiScale.enable=false

Note: Do not modify the vmoptions.txt or settings.vmoptions

files. These are often overwritten during updates,

meaning any changes you make will be lost. We never

modify the user.vmoptions file.

What if I still need the JAR?

While the workarounds above remove the need for most

people to use the JAR, we're aware that there are some

specialist use cases that may be impacted.

If you do still need to use the JAR, for example, to

support custom workflows and automation, to help with

developing extensions, or to deploy a private

Collaborator server, there is a simple workaround -

the installation package also contains a JAR that you

can use instead.

Using the JAR from a Burp Suite Professional or

Community Edition installation

This method provides much of the same flexibility,

while leveraging the security and convenience of the

installer-based version. This way, you can keep the JAR

version up to date by simply launching Burp Suite and

letting the auto-update kick in.

Either download the relevant Burp Suite installer and run it, or go to your existing Burp Suite

installation directory. By default, you can find this

in the following location:

- Linux:  /home/<user>/BurpSuite

- macOS: /Users/<user>/Applications/Burp Suite

Professional

- Windows: C:\Program Files\BurpSuitePro

In the installation directory, locate the JAR

file.

Refactor your existing scripts to point to the new JAR

location, or manually invoke the JAR from the command

line as you normally would.

Note: Avoid running the JAR from the installation

directory while simultaneously running the installed

version of Burp Suite as this can cause unexpected

behavior. If you want to run both versions

concurrently, we recommend copying the JAR to a

different location outside of the installation

package. However, note that this means you won't

benefit from auto-updates to your copy of the JAR

file.

Using the JAR from a Burp Suite Enterprise Edition

installation

If you are a Burp Suite Enterprise Edition user, you

can follow the same process as Burp Suite Professional

users. However, if you don't want to or are unable to

install Burp Suite Professional, you can also use the

JAR file from your Burp Suite Enterprise Edition

installation.

From the machine on which your Enterprise server is

running, locate the JAR file in the installation

directory. By default, you can find this in the

following location:

- Linux:  /opt/burpsuite_enterprise/burp/burpsuite_pro_<build-number>.jar

- Windows: C:\ProgramFiles\burpsuite_enterprise\burp\burpsuite_pro_<build-number>.jar

Copy the JAR to a different machine or a location

outside the installation directory.

Invoke the JAR from the command line as you normally

would.

Note: Do not invoke the JAR directly from the

installation directory. This can cause unexpected

issues if your Burp Suite Enterprise Edition instance

is running simultaneously.

Deploying a private Collaborator server

Deploying a private Collaborator server requires you

to run Burp from a JAR file using the

--collaborator-server command-line flag. If we remove

the option to download the JAR from the website, you

can still deploy a private Collaborator server using

the JAR provided in either the Burp Suite Professional

or Burp Suite Enterprise Edition installation

package.

Note: This applies to Collaborator servers that you

intend to use with either Burp Suite Professional or

Burp Suite Enterprise Edition.

Locate the JAR from a Burp Suite Professional or

Enterprise Edition installation, as described above.

If you want to deploy the Collaborator server on a

different OS to your existing Burp Suite installation, download and run the relevant Burp Suite Professional

installer.

Copy the JAR to the machine on which you want to run

the Collaborator server.

(Optional) If you ran the installer purely to extract

the JAR, run the uninstaller to remove the leftover

files from your system.

Invoke the JAR using the --collaborator-server

flag as you normally would. For detailed instructions

on the rest of the process, see Deploying a private Collaborator server.

Share your thoughts

We recognize that there is no one-size-fits-all

solution, which is why we're inviting your feedback. If

none of the suggested alternatives address your specific

use case, please share your thoughts and concerns using

the following link:

SHARE YOUR THOUGHTS

Your feedback is invaluable and will help us make an

informed decision.
