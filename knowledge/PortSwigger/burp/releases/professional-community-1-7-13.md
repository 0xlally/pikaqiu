# Professional / Community 1.7.13

Source: https://portswigger.net/burp/releases/professional-community-1-7-13
Fetched: 2026-06-28T09:16:30.982846+00:00

This release adds various enhancements and bugfixes.

Burp Infiltrator has been enhanced with a large number of new API sink definitions, for both the Java and .NET platforms. This dramatically increases the coverage of existing vulnerabilities, such as OS command injection and file path traversal.

You can export the updated Infiltrator installers from the "Burp" menu in Burp Suite Professional. If you have already installed an earlier version of Infiltrator in an application, you can just run the new installer to update the instrumentation with the new API sink definitions.

The BurpInfiltrator.dll .NET assembly is now signed, and all instrumented assemblies refer to it by its strong name. This change will address some issues that can arise with usage of signed assemblies.

The manual Burp Collaborator client has been enhanced to give full details of Infiltrator interactions. This can greatly assist manual testing and exploitation of vulnerabilities, for example by showing the full SQL query that is executed when some particular input is submitted. Also, the Collaborator client UI now shows the Collaborator payload in the table of interactions, and supports user comments and highlights:

The IBurpCollaboratorClientContext API now supports separate retrieval of regular Collaborator interactions and Infiltrator-driven interactions.

The following bugs have been fixed:

A bug in the "copy as curl command" function which could enable a malicious website to generate an HTTP request which, if the Burp user uses the "copy as curl command" function and executes the output in a shell context, will cause arbitrary commands to be executed. There is no exposure to users who do not use the "copy as curl command" function, but it is recommended that all users upgrade to the latest version. This issue was discovered through an internal security review, rather than a user report.

A bug in the Burp Collaborator health check which caused SMTP/S connections made by the health check not to honor the configured SOCKS proxy settings.

A bug which caused Proxy match/replace rules to display as type "regex" even if they are not.

A bug where use of a partial/incomplete configuration file at project startup caused any undefined configuration options to have blank values. Now, any undefined options are assigned their default values.

A bug which caused Burp to leave temporary files on disk if the user cancels out of the project startup wizard.

A bug which caused items in the active scan queue in the "waiting to cancel" state to display in that state indefinitely if the project is closed and reopened.
