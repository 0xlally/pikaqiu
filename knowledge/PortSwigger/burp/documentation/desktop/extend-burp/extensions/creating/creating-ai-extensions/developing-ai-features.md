# Developing AI features in extensions

Source: https://portswigger.net/burp/documentation/desktop/extend-burp/extensions/creating/creating-ai-extensions/developing-ai-features
Fetched: 2026-06-28T09:15:46.949199+00:00

Support Center

Documentation

Desktop editions

Extending Burp

Extensions

Creating

Creating AI extensions

Developing AI features in extensions

Professional

Developing AI features in extensions

Last updated:

June 18, 2026

Read time:

7 Minutes

This page provides an overview of how to integrate AI-powered features into Burp Suite extensions using the Montoya API.

On this page

Checking AI availability

Sending prompts and handling responses

Handling exceptions

Setting the temperature

Note

If you'd like to explore practical examples, check out our extension repository. It contains ready-made extensions that demonstrate how to integrate AI features using the Montoya API.

Checking AI availability

Before interacting with the AI, your extension must confirm that the user's Burp Suite instance supports AI functionality. AI functionality won't be available if:

The user is running an edition of Burp Suite that doesn't support AI features.

AI features are not enabled for the extension.

Configuring the extension to enable AI

The user must select the extension's Use AI check box to enable AI features. This is located on Burp's Extensions > Installed screen, and is off by default.

To display the checkbox for your extension, override the enhancedCapabilities() method of the BurpExtension interface in your extension and return the EnhancedCapability.AI_FEATURES flag.

Note

Your extension must include this override, as if the user cannot select Use AI then they will not be able to use AI features.

Example

import burp.api.montoya.BurpExtension;

import burp.api.montoya.EnhancedCapability;

import burp.api.montoya.MontoyaApi;

import java.util.Set;

public class ExampleExtension implements BurpExtension {

@Override

public void initialize(MontoyaApi api) {

// initialize extension

}

@Override

public Set<EnhancedCapability> enhancedCapabilities() {

return Set.of(EnhancedCapability.AI_FEATURES);

}

}

Verifying AI availability

Use the Ai.isEnabled() method to check whether AI functionality is available in the user's instance of Burp Suite.

This method returns true when both of the following conditions are met:

The user is running a supported edition of Burp Suite.

The Use AI checkbox is selected on the Extensions page.

If AI is not supported, handle this gracefully by disabling AI-related functionality or notifying the user.

Example

import burp.api.montoya.BurpExtension;

import burp.api.montoya.EnhancedCapability;

import burp.api.montoya.MontoyaApi;

import burp.api.montoya.ai.Ai;

import burp.api.montoya.logging.Logging;

import java.util.Set;

public class AiEnabledExtension implements BurpExtension {

private Ai ai;

private Logging logging;

@Override

public void initialize(MontoyaApi api) {

this.ai = api.ai();

this.logging = api.logging();

// Set extension name

api.extension().setName("AI Enabled Extension");

// Log initialization message

logging.logToOutput("AI Enabled Extension initialized. Enable AI in Burp to use AI features.");

}

@Override

public Set<EnhancedCapability> enhancedCapabilities() {

// Enable the Use AI checkbox in the Extensions menu

return Set.of(EnhancedCapability.AI_FEATURES);

}

/**

* Example method that checks AI availability before execution.

* This should be called when the user triggers AI functionality.

*/

public void performAiTask() {

if (!ai.isEnabled()) {

logging.logToOutput("AI is not enabled. Enable it in Burp.");

return;

}

logging.logToOutput("AI is enabled and ready to use.");

}

}

Sending prompts and handling responses

The Prompt interface sends structured prompts to the AI. A prompt consists of one or more Message objects that define input.

Messages can have three types:

System messages: Set the AI's behavior or role (for example, "You are a web security assistant specializing in vulnerabilities").

User messages: Represent user queries (for example, "Explain how SQL Injection works").

Assistant messages: Represent AI-generated responses from previous interactions (for example, "SQL Injection is a vulnerability that allows an attacker to manipulate a database query.").

By combining these messages, you can send single-shot prompts or build conversation features that maintain context across multiple interactions.

Note

It's good practice to start every session or interaction with a system message to define the AI's role and behavior. This helps the AI provide responses aligned with your specific use case.

Single-shot prompts

A single-shot prompt is a standalone query that typically includes both a system and user message. This approach is ideal for one-off questions or analyses.

When you send a prompt, the response is returned as a PromptResponse object. Use this interface to:

Retrieve the response as a string using the content() method.

Store or use the response for further actions, such as displaying it to the user or building follow-up prompts.

Example

import burp.api.montoya.ai.chat.Message;

import burp.api.montoya.ai.chat.Prompt;

import burp.api.montoya.ai.chat.PromptResponse;

import burp.api.montoya.logging.Logging;

public class PromptResponseExample {

private final Logging logging;

// Constructor to initialize the logging instance

public PromptResponseExample(Logging logging) {

this.logging = logging;

}

public void handleResponse(Prompt prompt) {

// Define the AI's role with a system message

Message systemMessage = Message.systemMessage("You are a web security assistant.");

// Provide a user query with a user message

Message userMessage = Message.userMessage("Explain how SQL Injection works.");

// Send the prompt and get the response

PromptResponse response = prompt.execute(systemMessage, userMessage);

// Retrieve the AI's response content

String aiOutput = response.content();

// Log the response using the Montoya logging API

logging.logToOutput("AI Response: " + aiOutput);

}

}

Tip

Validate the AI's response in code to ensure the response is present and that the AI hasn't returned an error before proceeding.

Building multi-turn conversations

For more natural interactions, you can build multi-turn conversations by maintaining a sequence of Message objects. Each new query includes previous messages and responses as context.

A typical multi-turn workflow follows these steps:

Initialize context with messages:

Start with a Message.systemMessage to define the AI's role.

Add an initial Message.userMessage for the user query.

Process the AI's response:

Send the current context to the AI using Prompt.execute().

Retrieve the response using PromptResponse.content().

Update context with responses - Store AI responses as a Message.assistantMessage to ensure they are identified as AI-generated output.

Repeat for follow-up queries:

Add new user queries as a Message.userMessage.

Send the updated context to the AI for each interaction.

The following example shows how to maintain a conversation context using Message and PromptResponse:

Example

import burp.api.montoya.ai.chat.Message;

import burp.api.montoya.ai.chat.Prompt;

import burp.api.montoya.ai.chat.PromptResponse;

import burp.api.montoya.logging.Logging;

import java.util.ArrayList;

import java.util.List;

public class MultiTurnChatExample {

private final List<Message> context = new ArrayList><();

private final Logging logging;

// Constructor to initialize the logging instance

public MultiTurnChatExample(Logging logging) {

this.logging = logging;

initializeContext();

}

/**

* Initializes the conversation with a system message.

*/

private void initializeContext() {

if (context.isEmpty()) {

context.add(Message.systemMessage("You are a web security assistant specializing in vulnerabilities."));

}

}

/**

* Starts a conversation with the first user query.

*/

public void initializeConversation(Prompt prompt) {

initializeContext(); // Ensure system message exists

context.add(Message.userMessage("What is SQL Injection?"));

sendPrompt(prompt);

}

/**

* Adds a new user query and sends the updated context.

*/

public void addUserQuery(Prompt prompt, String userQuery) {

initializeContext(); // Ensure system message exists

context.add(Message.userMessage(userQuery));

sendPrompt(prompt);

}

/**

* Sends the prompt to the AI and updates the context.

*/

private void sendPrompt(Prompt prompt) {

try {

// Execute the prompt with the full context

PromptResponse response = prompt.execute(context.toArray(new Message[context.size()]));

// Store AI response as an assistant message

Message assistantMessage = Message.assistantMessage(response.content());

context.add(assistantMessage);

// Log AI response AFTER adding to context

logging.logToOutput("AI Response: " + assistantMessage.content());

} catch (Exception e) {

logging.logToError("Error processing AI response: " + e.getMessage());

}

}

}

Tip

Include only the most relevant and recent messages in the context to avoid overwhelming the AI or degrading performance. For example, if your conversation has ten exchanges but only the last three are relevant, include only those three messages in the next prompt.

Handling exceptions

It's important to handle errors gracefully to ensure your extension is able to continue functioning as expected for your users. The PromptException class represents errors that may occur during AI prompt execution, such as:

Null or improperly formatted messages.

Problems communicating with the AI service.

The user running out of AI credits.

Wrap calls to AI methods, like Prompt.execute(), in a try-catch block to ensure your extension can recover from errors.

The following example shows how to catch and handle a PromptException when sending a single-shot prompt:

Example

import burp.api.montoya.ai.chat.Message;

import burp.api.montoya.ai.chat.Prompt;

import burp.api.montoya.ai.chat.PromptException;

import burp.api.montoya.ai.chat.PromptResponse;

import burp.api.montoya.logging.Logging;

public class PromptExceptionExample {

private final Logging logging;

public PromptExceptionExample(Logging logging) {

this.logging = logging;

}

public void handleResponse(Prompt prompt) {

try {

// Define the AI's role with a system message

Message systemMessage = Message.systemMessage("You are a web security assistant.");

// Provide a user query with a user message

Message userMessage = Message.userMessage("Explain how SQL Injection works.");

// Send the prompt and get the response

PromptResponse response = prompt.execute(systemMessage, userMessage);

// Log the AI's response using the Montoya logging API

logging.logToOutput("AI Response: " + response.content());

} catch (PromptException e) {

// Log the exception message using the Montoya logging API

logging.logToError("An error occurred while processing the prompt: " + e.getMessage());

// Handle the error gracefully

logging.logToError("Unable to retrieve AI response. Please try again later.");

}

}

}

Tip

Log errors using api.logging().logToError() to ensure they are properly recorded in Burp Suite's log output.

Setting the temperature

You can control the creativity of the AI's responses using the temperature setting in the PromptOptions interface.

Temperature is a numeric value between 0 and 2. This setting controls the balance between predictable and creative responses, enabling you to tailor the AI's behavior to your specific needs:

Lower temperatures (0.0 - 0.8) produce more predictable and deterministic outputs. They are best used for technical or factual tasks.

Higher temperatures (0.8 - 2.0) produce more creative and diverse outputs. They are suitable for exploratory tasks.

As a general rule, lower temperatures produce better results for security-related applications. By default, the temperature is set to 0.5.

The below example shows how to set the temperature using PromptOptions.

Example

import burp.api.montoya.ai.chat.Prompt;

import burp.api.montoya.ai.chat.PromptOptions;

import burp.api.montoya.ai.chat.PromptResponse;

import burp.api.montoya.logging.Logging;

public class SettingTemperatureExample {

private final Logging logging;

// Constructor to initialize the Logging instance

public SettingTemperatureExample(Logging logging) {

this.logging = logging;

}

public void sendPromptWithTemperature(Prompt prompt) {

// Create a PromptOptions instance and set the temperature

PromptOptions options = PromptOptions.promptOptions()

.withTemperature(0.3); // Focused and deterministic response

// Send a prompt using the configured options

PromptResponse response = prompt.execute(options, "Explain how SQL Injection works.");

// Log the AI's response using the Montoya logging API

logging.logToOutput("AI Response: " + response.content());

}

}

More information

Montoya API JavaDoc

BApp store acceptance criteria

Burp AI trust and compliance FAQ
