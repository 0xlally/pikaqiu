# Professional 1.7.04

Source: https://portswigger.net/burp/releases/professional-1-7-04
Fetched: 2026-06-28T09:16:28.651067+00:00

This release introduces a new tool, called Burp Infiltrator.

Burp Infiltrator is a tool for instrumenting target web applications in order to facilitate testing using Burp Scanner. Burp Infiltrator modifies the target application so that Burp can detect cases where its input is passed to potentially unsafe APIs on the server side.

The initial release of Burp Infiltrator supports applications written in Java or other JVM-based languages such as Groovy. Java versions from 4 and upwards are supported. In future, Burp Infiltrator will support other platforms such as .NET.

For more details about how Burp Infiltrator works, how to use it, and some other important considerations, please refer to the Burp Infiltrator blog post and the Burp Infiltrator documentation.

Burp Infiltrator makes use of Burp Collaborator for its communications back to the instance of Burp Suite that is performing scans. To support this, some new capabilities have been added to Burp Collaborator. Users who have deployed a private Burp Collaborator server should upgrade to the new version.

Some minor bugs have been fixed, including:

A bug which caused the values of some project options to change when an existing Burp project is reopened.

A bug which prevented editing of macro requests when using a disk-based project.

A bug which prevented the hostname from being correctly parsed from some TLS client hello messages when Burp Proxy is running in invisible mode.
