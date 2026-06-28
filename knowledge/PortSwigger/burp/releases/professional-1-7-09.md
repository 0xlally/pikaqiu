# Professional 1.7.09

Source: https://portswigger.net/burp/releases/professional-1-7-09
Fetched: 2026-06-28T09:16:28.294387+00:00

This release adds a new Burp Collaborator client for use in manual testing, some new APIs for using Burp Collaborator capabilities within Burp extensions, and a new Burp extension that demonstrates usage of the APIs.

Burp Collaborator client is a tool for making use of Burp Collaborator during manual testing. You can use the Collaborator client to generate payloads for use in manual testing, and poll the Collaborator server for any network interactions that result from using those payloads.

To run Burp Collaborator client, go to the Burp menu and select "Burp Collaborator client".

The following functions are available:

You can generate a specified number of Collaborator payloads and copy these to the clipboard. You can use these in manual testing, for example using Burp Intruder or Repeater.

You can choose whether the generated payloads include the full Collaborator server location, or only the unique interaction ID.

You can poll the Collaborator server to retrieve details of any network interactions resulting from your payloads, either at a regular interval or on demand.

Some new APIs have been added for using Burp Collaborator capabilities within Burp extensions. There is a new method on IBurpExtenderCallbacks:

IBurpCollaboratorClientContext createBurpCollaboratorClientContext();

This creates an IBurpCollaboratorClientContext object that can be used to generate Burp Collaborator payloads and poll the Collaborator server for any network interactions that result from using those payloads.

To demonstrate usage of the new APIs, we have today released to the BApp Store a new extension that can detect the HTTPoxy vulnerability via Burp Collaborator.

The source code to the HTTPoxy Scanner extension is available here.
