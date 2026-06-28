# Troubleshooting scripts

Source: https://portswigger.net/burp/documentation/desktop/extend-burp/bambdas/creating/troubleshooting
Fetched: 2026-06-28T09:15:45.465909+00:00

Support Center

Documentation

Desktop editions

Extending Burp

Bambdas

Creating scripts

Troubleshooting

ProfessionalCommunity Edition

Troubleshooting scripts

Last updated:

June 18, 2026

Read time:

2 Minutes

This guide helps you troubleshoot issues while writing scripts.

Compilation errors

When you're creating a script, Burp highlights any compilation errors in real time. You must resolve these errors before you can apply your script.

You can view compilation errors in the following ways:

Hover over the red underline in the script editor.

From the Bambda library editor, click Save. Error details are shown in the Compilation errors tab.

From a tool-specific script editor, click Apply. Error details are shown in the Compilation errors tab.

Note

Compilation errors are detected based on the function and location of the script. For example, if you're writing a view filter WebSockets script, Burp checks that the code complies with the specific requirements for a WebSockets view filter.

Runtime errors

Runtime errors occur after a script has been applied. If Burp detects any runtime errors, a warning appears in the relevant Burp tool.

To resolve a runtime error, edit the script to view the error details. You can then make changes to the code, or debug the script using the Logging interface.

Debugging scripts

From tool-specific script editors, you can use the logging interface to debug your script by printing messages to the console. This can help you resolve runtime errors or issues in your code.

You can access the following functions:

logging.logToOutput - Adds standard debug messages to the console.

logging.logToError - Adds error messages to the console in red text.

To view messages generated using logToOutput and logToError from a tool-specific script editor, click Apply. Messages are shown in the Console tab.

Note

The logging interface is not available from the Bambda library editor.
