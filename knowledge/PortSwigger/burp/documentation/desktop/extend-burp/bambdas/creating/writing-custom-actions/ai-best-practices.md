# Best practices for writing AI custom actions

Source: https://portswigger.net/burp/documentation/desktop/extend-burp/bambdas/creating/writing-custom-actions/ai-best-practices
Fetched: 2026-06-28T09:15:45.426736+00:00

Support Center

Documentation

Desktop editions

Extending Burp

Bambdas

Creating scripts

Writing custom actions

AI best practices

Professional

Best practices for writing AI custom actions

Last updated:

June 18, 2026

Read time:

2 Minutes

The Montoya API enables you to integrate AI-powered functionality into your custom actions. Follow these best practices to ensure your custom action is secure, efficient, and produces high-quality results.

Note

For examples of AI-powered custom actions that have been created by our research team and the community, see our GitHub repository.

To learn how to add AI-powered features to your custom actions, see Developing AI features in custom actions.

To learn how to create your own custom actions, see Writing custom actions.

Mitigate prompt injection attacks

Treat raw output from AI models as untrusted. Escape any AI-generated content before presenting it to users. Make sure that you use proper HTML encoding to neutralize potential threats.

Optimize AI requests for efficiency and security

To ensure AI interactions are efficient, secure, and cost-effective, it's important to control what data is sent, how it's formatted, and when requests are made.

To optimize requests effectively:

Only send essential data. For example, avoid including full HTTP requests if only specific headers or parameters are needed, and only send traffic that is in-scope for the application you are testing.

Where possible, strip out sensitive data such as authentication tokens or session cookies.

Use structured data formats like JSON instead of free-text input to prevent prompt injection. Structured formats enforce a strict schema, making it harder for attackers to manipulate AI prompts. Since JSON strings are automatically escaped, they prevent unintended input injection.

Validate and encode outgoing data before sending it, to prevent prompt injection or unintended execution.

Use effective prompts

A well-structured prompt helps the AI to provide relevant and high-quality responses. We recommend that you:

Define the AI's role using a system message. This helps set the context and behavior for the AI throughout the conversation.

Provide relevant background information in the user prompt.

Clearly specify what you want the AI to do.

More information

For more information, see Developing AI features in custom actions - Sending prompts and handling responses.

Use lower temperatures for better accuracy

The temperature setting controls the balance between predictability and creativity in AI responses:

Lower temperatures (0.0 - 0.8) produce more predictable and accurate outputs. They are best used for technical or factual tasks.

Higher temperatures (0.8 - 2.0) produce more creative and diverse outputs. They may cause the AI to produce inconsistent results, potentially making security-related responses unreliable. They are suitable for exploratory tasks.

The default temperature is 0.5.

More information

For more information, see Developing AI features in custom actions - Setting the temperature.
