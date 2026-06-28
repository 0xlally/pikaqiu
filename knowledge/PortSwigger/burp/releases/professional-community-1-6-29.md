# Professional / Community 1.6.29

Source: https://portswigger.net/burp/releases/professional-community-1-6-29
Fetched: 2026-06-28T09:16:30.328804+00:00

This release updates Burp to include a security fix in the BlazeDS library that Burp uses for parsing AMF messages, and disables AMF support by default:

AMF messages can contain embedded XML content, and this is processed by the BlazeDS library when it parses AMF messages. BlazeDS has been found to contain an XXE vulnerability in its processing of XML embedded within AMF messages. In the context of Burp, the potential impact of the vulnerability is that a malicious target application could read the contents of files from the Burp user's computer, provided it knows the names of those files. A malicious application could perform this attack if it generates a suitable AMF message and the user browses via Burp to a response containing the AMF message. The latest version of BlazeDS contains a fix for the XXE vulnerability, and Burp has been updated to use the new version of the library. Thanks are due to David Klein from Context Information Security for drawing our attention to this issue.

It is well known that XML parsing is fraught with problems, as is demonstrated by Burp Scanner's XML checks. To reduce the impact of any further issues within BlazeDS, Burp has been updated so that by default it disables the AMF tab within the HTTP message editor, and disables AMF insertion points in the Scanner. Users can turn on these options if they are testing a trusted application that uses AMF messages. It is recommended that users do not enable AMF processing when accessing any untrusted application functionality or content.

Burp's cookie jar has been updated to support the cookie path attribute. The cookie jar is now able to track multiple cookies from the same domain with the same name, but which are scoped to different application paths. Burp's session handling rules now correctly update cookies in requests based on the path attribute.

The functions to save and restore state now include options for handling the unique identifier that Burp uses to track interactions with Burp Collaborator. Each Burp project/session generates a unique identifier that is used to track any Burp Collaborator interactions that are associated with the project. If two users share a state file, and each continues testing from that point, there is the potential for interference in Collaborator interactions, causing some Collaborator-based issues to be missed or incorrectly reported. When saving state, you can now choose whether to include the identifier within the state file, so that you or someone else can resume the testing later. When loading a state file that was saved using a different installation of Burp and which contains a Collaborator identifier, you can now choose whether to take full ownership of the project and receive details of any ongoing Collaborator interactions that are associated with the project.

(Note that each fresh Burp project/session generates a new random Collaborator identifier, so there is no risk of permanent cross-talk between different Burp instances, regardless of the options chosen when sharing a specific state file.)

A bug affecting the importing of some custom CA certificates in PKCS#12 format has been fixed.
