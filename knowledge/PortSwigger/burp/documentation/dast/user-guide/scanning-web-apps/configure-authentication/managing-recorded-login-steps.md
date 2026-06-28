# Managing steps in a recorded login

Source: https://portswigger.net/burp/documentation/dast/user-guide/scanning-web-apps/configure-authentication/managing-recorded-login-steps
Fetched: 2026-06-28T09:15:40.995663+00:00

DAST

Managing steps in a recorded login

Last updated:

June 18, 2026

Read time:

5 Minutes

Cloud

Self-hosted

You can view and manage individual steps in your recorded login sequences. This is useful when you want to modify specific actions without editing the entire JSON script.

Note

To manage steps in a recorded login sequence, you need permissions for the site to View site application login details and Edit site application logins. For more information, see Role-based access control.

Viewing steps

When you edit a recorded login, you can view the individual steps in your login sequence on the Steps tab. This gives you a visual list of all the actions in the sequence.

To view the steps in a recorded login:

In the site's Details tab, click Edit.

In Scan settings > Authentication, click the pencil icon next to the recorded login sequence.

In the Steps tab, the list shows all the steps in your recorded login sequence.

Each step shows the action type and a summary of what it does. You can switch to the Script tab to view the JSON-based script.

Step types

Your recorded login sequence can include the following step types:

Navigate: Goes to a specified URL.

Click: Clicks an element on the page.

Type: Types text into an element on the page.

Wait: Pauses for a specified duration.

Key press: Presses a keyboard key.

TOTP: Generates a Time-based One-Time Password and types it into a specified field. For more information, see Configuring TOTP MFA.

WebAuthn configuration: Indicates that your login contains WebAuthn passkeys. Appears as the first step, regardless of where the passkey step occurs in your login sequence. Cannot be edited. For more information, see WebAuthn passkeys in recorded logins.

Selector types

When you add a Click or Type step, you need to tell the scanner how to find the element on the page. You do this by choosing a selector type and entering a value.

The selector type determines how the scanner locates elements on the page:

ID: Finds an element by its unique ID attribute. This is the most reliable option if the element has an ID.

Link href: Finds an element by its href attribute. This is best for links and buttons.

Name: Finds an element by its name attribute. This is commonly used for form fields.

Aria label: Finds an element by its aria-label attribute. This is useful for accessible web apps.

Class name: Finds an element by its CSS class. Use this when the element has a unique class name.

Text content: Finds an element by its visible text. This is useful for buttons.

Text nodes: Finds an element by the text of elements inside it. Use this when the element you're clicking doesn't have text, but an element inside it does.

XPath: Finds an element using an XPath expression. Use this when other selector types don't work.

In most cases, you can use ID or Name. If these don't work, try Link href for links and buttons, Text content or Text nodes for buttons, or XPath for more complex scenarios.

You can add multiple selectors for a single step, with a maximum of one selector for each type. When you add multiple selectors, the scanner uses them in priority order. The order shown above is the priority order, with ID having the highest priority and XPath the lowest.

Advanced settings

When you add a Click, Type, or Key press step, you can configure advanced settings to control how the scanner interacts with your application. Make sure you understand the relevant web technologies before editing these settings.

Browser settings

Browser settings tell the scanner how your web app responds to a step. Configure these settings to match your application's behavior:

Opens new tab: Select this if the step opens a new browser tab.

Closes tab: Select this if the step closes the current browser tab.

Causes navigation: Select this if the step navigates to a different URL.

You can select multiple options if needed. For example, a button might both cause navigation and open a new tab.

Shadow parent

Some modern web applications use shadow DOM to encapsulate parts of the page. If an element is inside a shadow DOM, the scanner needs to know where to look for it.

Enable the Shadow parent setting if:

Your application uses web components (custom HTML elements like <login-form> or <app-input>).

The scanner can't find the element during replay, even though your selector is correct.

You can leave this setting disabled for most standard login forms.

Adding a step

To add a new step to your recorded login sequence:

In the Edit recorded login dialog, go to the Steps tab.

Click More next to the step where you want to insert a new step.

Select Insert above or Insert below.

In the Step type dropdown, select the type of action you want to add.

Configure the step based on its type:

Navigate: Enter the URL you want to go to in the URL field.

Click:

Choose a Selector type: ID, Link href, Name, Aria label, Class name, Text content, Text nodes, or XPath.

Enter a value for the chosen type of selector.

Optional: Expand Advanced settings to configure Browser settings or Shadow parent options.

Type:

Select a Selector type, such as ID, Link href, Name, Aria label, Class name, Text content, Text nodes, or XPath.

Enter the selector value in the field next to the dropdown.

In the Typed value field, enter the text you want to type into the element.

Optional: Expand Advanced settings to configure Browser settings or Shadow parent options.

Wait: In the Duration field, enter the number of milliseconds to wait.

Key press:

In the Key to press dropdown, select the keyboard key, such as Tab, Enter, Alt, or Shift.

Optional: Expand Advanced settings to configure Browser settings.

TOTP:

Click Upload QR code to upload your saved image of the QR code, or click Set up TOTP manually to enter the TOTP secret and settings.

Choose a Selector type and enter a value to tell Burp how to find the TOTP input field on the page.

Optional: Expand Advanced settings to configure Browser settings or Shadow parent options.

For more information, see Configuring TOTP MFA.

Click Save to add the step to your sequence.

Editing a step

To edit an existing step in your recorded login sequence:

In the Edit recorded login dialog, in the Steps tab, click More next to the step you want to edit.

Select Edit.

Update the step settings as needed.

Click Save to apply your changes.

Deleting a step

To delete a step from your recorded login sequence:

In the Edit recorded login dialog, in the Steps tab, click More next to the step you want to delete.

Select Delete.

Related pages

Using recorded logins.

Configuring TOTP MFA.

Recording login sequences (Scanner).

Best practice for recording login sequences in Burp Suite DAST.
