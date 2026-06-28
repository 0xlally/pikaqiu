# Debugging Burp extensions with a remote debugger

Source: https://portswigger.net/burp/documentation/desktop/extend-burp/extensions/creating/debugging/using-debugger
Fetched: 2026-06-28T09:15:46.976360+00:00

Support Center

Documentation

Desktop editions

Extending Burp

Extensions

Creating

Setting up remote debugging

Using a remote debugger

ProfessionalCommunity Edition

Debugging Burp extensions with a remote debugger

Last updated:

June 18, 2026

Read time:

4 Minutes

A remote debugger enables you to inspect your Burp extension as it runs in Burp Suite. This makes it easier to diagnose issues and refine your extension's behavior.

This guide provides an overview of key remote debugging techniques. It covers the following:

Setting breakpoints.

Examining call stacks and variables.

Modifying your code.

Prerequisites

Before you begin, make sure you have set up the following:

Your IDE's debugger must be attached to Burp Suite. If you haven't set this up yet, follow the instructions in Setting up remote debugging for Burp extensions.

Your extension is built and loaded in Burp. To make sure breakpoints trigger correctly, rebuild and reload your extension so that the source code in your IDE matches the compiled code Burp is running. For instructions, see Loading your extension in Burp.

Step 1: Set breakpoints

Breakpoints are markers that pause your extension's execution at specified lines, so you can inspect variable values and control flow.

To set breakpoints in most IDEs, click the left margin next to the line number. Start with one or two breakpoints, then add more as required.

The placement of breakpoints depends on the code you're trying to debug. Consider setting breakpoints at key execution points in your extension's logic, for example:

Code entry points - Set breakpoints inside key methods near the start of the logic you're interested in. If execution pauses at the breakpoint it confirms the method is being executed as expected. For example, set a breakpoint in the initialize() method to verify that your extension loads correctly and the Montoya API is available.

Processing steps - Set breakpoints before and after major processing tasks, such as handling HTTP requests or modifying data. This enables you to observe how data is transformed and passed through your code.

Exception handling - Set breakpoints on lines that are likely to throw exceptions, to inspect the inputs and state leading up to the error. You can also set breakpoints to pause automatically when a specific type of extension is thrown.

Setting conditional breakpoints

Conditional breakpoints enable you to pause execution only when specific criteria are met, reducing unnecessary interruptions when debugging. To set a conditional breakpoint in most IDEs:

Right-click an existing breakpoint.

Add a condition, such as requestBody.contains("example").

The debugger only pauses execution when the specified condition is true.

Setting logging breakpoints

Logging breakpoints enable you to log information without pausing execution. They're useful when debugging loops or repetitive logic where traditional breakpoints would cause too many interruptions.

To add a logging breakpoint:

Right-click an existing breakpoint.

Choose the logging option. Depending on your IDE, this may be labeled as Evaluate and log or Log message to console, for example.

Enter the expression you want to output, for example responseBody.length().

Step 2: Trigger your extension in Burp

After setting breakpoints in your IDE, trigger your extension's functionality in Burp. When Burp reaches a breakpoint in your extension's code, execution pauses. This allows you to inspect the program state.

Troubleshooting

If execution doesn't pause at your breakpoints, try the following:

Make sure that the breakpoint isn't a logging breakpoint, or a conditional breakpoint that doesn't meet its condition.

Check that the breakpoint hasn't been muted or disabled in your IDE.

Rebuild and reload your extension to ensure you are debugging the latest compiled version. For instructions, see Loading your extension in Burp.

Add a breakpoint earlier in execution to confirm that the debugger is attached. For example, add a breakpoint at the start of the initialize() method.

If the debugger isn't attached, follow the instructions in Setting up remote debugging for Burp extensions.

Step 3: Inspect stack frames and variables

In your IDE, review the current variable values and stack frames in the debugger console, to verify if your code is running as expected.

Note

This section is intended to help you start debugging your extension using your IDE's debugging functionality. For more comprehensive guidance, refer to your IDE provider's documentation.

Review the call stack

The call stack shows the sequence of method calls leading to the current execution point. Each stack frame represents an individual method call. The top frame is the currently executing method, while lower frames represent previous calls in the chain. Check that the sequence aligns with your expected logic and look for anomalies that might suggest skipped method calls.

Inspect variable values

Review the variables in each frame. Make sure that key variables hold expected values.

Step through the code

Use your IDE's stepping actions to execute the extension step-by-step. As you move through each line, check that conditional logic and data mutations occur correctly to pinpoint issues.

View errors in the terminal

Check the terminal for additional error messages and logs. Because you started Burp from the command line when you attached the debugger, Burp may output useful debugging information to the terminal, such as:

Stack traces for unhandled exceptions.

Warnings and error messages.

Step 4: Modify your extension and repeat

After you identify issues, modify your extension and repeat testing:

Modify your extension's code as required.

Remove any unnecessary breakpoints.

Add new breakpoints as required.

Rebuild your project and reload it in Burp. To do this quickly, in the Extensions > Installed tab, hold Ctrl or Cmnd and select the

Loaded checkbox next to your extension.

Step 5: Finish the debug session

When you've finished testing:

Stop the debug session.

Remove breakpoints from your code. Active breakpoints in your code can impact your extension's performance.

Sharing your extension

Share your extension on our PortSwigger Discord #extensions channel to get feedback, showcase your work, and connect with other developers.

You can submit your extension to the BApp store, and make it available to the community of 80,000+ testers worldwide. For guidance on the submission process, see Submitting extensions to the BApp store.
