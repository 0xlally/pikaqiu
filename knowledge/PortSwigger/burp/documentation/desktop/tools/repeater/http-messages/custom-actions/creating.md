# Creating custom actions

Source: https://portswigger.net/burp/documentation/desktop/tools/repeater/http-messages/custom-actions/creating
Fetched: 2026-06-28T09:16:07.560764+00:00

Support Center

Documentation

Desktop editions

Tools

Repeater

Working with HTTP messages

Custom actions

Creating custom actions

Professional

Creating custom actions

Last updated:

June 18, 2026

Read time:

3 Minutes

Custom actions are scripts that run directly from Burp Repeater to extract, transform, and analyze data. You can write your own custom actions to tailor Burp Repeater to your specific testing requirements.

Custom actions are built with Java and can be simple to write, even for beginners. Useful scripts may be as simple as a few lines of code. To help you get started, we provide:

Built-in starter templates in the editor.

Inline suggestions and error highlighting in the editor.

A range of community and reference resources.

Related pages

Custom action worked example - Write your first custom action.

Custom actions writing guide - Useful code snippets and building block examples of custom actions.

Developing AI features in custom actions - Add AI-features to your custom actions.

Bambdas GitHub repository - Examples of custom actions that have been created by the community.

To create a new custom action:

[Optional] Make sure the Repeater tab contains a request / response pair that you've sent and want to test the custom action against. For more information, see

How Burp selects test data.

In Repeater, click Custom actions. The Custom actions side panel opens.

Click New and select either Blank or From template. The Custom actions editor dialog opens.

If you selected From template, select a Custom action template from the list, then click Create using this template.

Write your custom action script using Java. For more information, see Writing custom actions.

Test the custom action using the built-in test function. For more information, see Testing custom actions.

[Optional] Click Save to library > Save. The custom action is saved to your Bambda library for future use across Burp.

Click OK.

If the custom action is error-free, it's added to the Custom actions side panel.

If errors exist, they appear in the Compilation errors panel. You'll need to fix these before you can add the custom action to the list. For more information, see Troubleshooting scripts.

Note

To speed up your workflow, you can use the following keyboard shortcuts to save your custom action to the Bambda library:

Save to library - Ctrl + S or Cmd + S

Save copy to library - Ctrl + Shift + S or Cmd + Shift + S

Warning

Using slow running or resource-intensive custom action scripts can slow down Burp. Write your custom action carefully to minimize performance impact.

Testing custom actions

When adding or editing a custom action, you can test its behavior using the built-in test function. This enables you to confirm that the action performs as expected.

To test a custom action in the Custom actions editor:

Review the sample message under Request. Optionally, replace it with the specific request you'd like to test the rule against.

Click Test. Burp runs the custom action on the sample message.

Review any output in the Console tab.

Adjust the custom action as necessary.

To restore the sample message, click .

How Burp selects test data

The test function automatically uses the open request, response, and HTTP service from the current Repeater tab when you open the Custom actions editor.

The HTTP service is the destination host, port and protocol. For example, https://example.com:443. If this information isn't available, Burp uses a null HTTP service instead. This can impact how your custom action behaves during testing, especially if it:

Makes follow-up requests.

Logs information about the target service.

Processes messages based on host or protocol.

Related pages

To get feedback, showcase your work, and connect with other developers, share your custom action on our PortSwigger Discord #bambdas channel.

To share your custom actions with the community, add them to our ever-growing GitHub repository. For more information, see Submitting Bambdas to our GitHub repository.
