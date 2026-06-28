# Developing AI features in custom actions

Source: https://portswigger.net/burp/documentation/desktop/extend-burp/bambdas/creating/writing-custom-actions/developing-ai-features
Fetched: 2026-06-28T09:15:46.331024+00:00

Support Center

Documentation

Desktop editions

Extending Burp

Bambdas

Creating scripts

Writing custom actions

Developing AI features

Professional

Developing AI features in custom actions

Last updated:

June 18, 2026

Read time:

3 Minutes

Learn how to add AI-powered features to your custom actions using the Montoya API. For example, you could use AI to build custom actions that:

Analyze requests or responses for vulnerabilities automatically.

Generate payloads based on context.

Transform or optimize data.

Related pages

For examples of AI custom actions that have been created by our research team and the community, see our Bambdas GitHub repository - Custom actions.

For non-AI building blocks, see our Custom actions writing guide.

Best practices for writing AI custom actions

Burp AI trust and compliance FAQ

Sending prompts and handling responses

The Prompt interface sends structured prompts to the AI. A prompt consists of one or more Message objects. These can have two types:

System messages: Set the AI's behavior or role.

User messages: Represent request or response data, or user queries.

Note

It's good practice to start every session or interaction with a system message to define the AI's role and behavior. This helps the AI provide responses aligned with your specific use case.

To construct a prompt for a custom action:

Get the request or response data that you want to analyze. For more information, see Accessing request and response data.

Construct a system message that defines the AI's role.

Create a user message with the data to analyze, such as request or response data.

Send the prompt to the AI for processing using ai().prompt().execute. This returns a PromptResponse object.

Retrieve the AI's response as a string using the content() method.

Output or use the result.

The below example shows how to construct a single-shot prompt. It starts with user-selected text and generates output vector variants:

// Capture the user's selected request text as a string

var selectedText = selection.requestSelection().contents().toString();

if (selectedText.isEmpty()) {

return;

}

// Define the AI's role with a system message

var systemMessage = "You are a web security expert. Be creative. Just output vectors separated by new lines. Do not output markdown. Do not prefix with a number. Do not quote with backticks. Work out what is being tested then create 10 variants separated by new lines. The variants you create should be useful for bypassing a WAF for security testing purposes. Create 10 variants of this:";

// Send the system message and the user message with the user's selected text, then retrieve the AI's response content

var aiOutput = ai().prompt().execute(Message.systemMessage(systemMessage), Message.userMessage(selectedText)).content();

// Log the response

logging.logToOutput(aiOutput);

Setting the temperature

Temperature is a numeric value between 0 and 2. This setting controls the balance between predictable and creative responses, enabling you to tailor the AI's behavior to your specific needs:

Lower temperatures (0.0 - 0.8) produce more predictable and deterministic outputs. They are best used for technical or factual tasks.

Higher temperatures (0.8 - 2.0) produce more creative and diverse outputs. They are suitable for exploratory tasks.

As a general rule, lower temperatures produce better results for security-related applications. By default, the temperature is set to 0.5.

The below example shows how to set the temperature:

// Capture the user's selected request text as a string

var selectedText = selection.requestSelection().contents().toString();

if (selectedText.isEmpty()) {

return

}

// Set the temperature

var temperature = 1.0;

// Create a prompt for the user message, using the user's selected content

var prompt = "Guess possible meanings of this web identifier, concisely: " + selectedText;

// Send the user message with the defined temperature, then retrieve the AI's response content

var aiOutput = api.ai().prompt().execute(PromptOptions.promptOptions().withTemperature(temperature), Message.userMessage(prompt)).content();

// Log the response

logging.logToOutput(aiOutput);

Handling exceptions

Because users receive immediate feedback on errors in the Output panel, you often don't need to handle exceptions in custom actions.

However if you'd like to handle errors more cleanly, you can wrap calls to AI methods, like ai().prompt().execute(), in a try-catch block. When an error is thrown, a PromptException is thrown, which contains an error message that you can retrieve using getMessage().

The following example shows how to catch and handle errors when sending a single-shot prompt:

try {

// Capture the request body as a string

var requestBody = requestResponse.request().toString();

// Define the AI's role with a system prompt

var systemMessage = "You are a web security expert. Analyze the request and identify anything that may indicate a vulnerability.";

// Send the system message and user message with the request body, then retrieve the AI's response content

var aiOutput = ai().prompt().execute(Message.systemMessage(systemMessage), Message.userMessage(requestBody)).content();

// Log the response

logging.logToOutput(aiOutput);

} catch (PromptException e) {

// Log any errors

logging.logToError("An error occurred while processing the prompt: " + e.getMessage());

}
