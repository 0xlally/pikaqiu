# Best practices for writing AI extensions

Source: https://portswigger.net/burp/documentation/desktop/extend-burp/extensions/creating/creating-ai-extensions/best-practices
Fetched: 2026-06-28T09:15:46.825801+00:00

Support Center

Documentation

Desktop editions

Extending Burp

Extensions

Creating

Creating AI extensions

Best practices for writing AI extensions

Professional

Best practices for writing AI extensions

Last updated:

June 18, 2026

Read time:

3 Minutes

The Montoya API enables you to integrate AI-powered functionality into your Burp Suite extensions. Follow these best practices to ensure your extension is efficient and user-friendly.

Note

For examples of AI-powered extensions that have been accepted into the BApp store, see the Montoya API example repo.

For a general getting started guide to writing extensions, see Creating extensions.

Declare AI support and check availability

For your extension to use AI features, you must:

Explicitly declare AI support for the extension. To do so, override the enhancedCapabilities() method of the BurpExtension interface and return the EnhancedCapability.AI_FEATURES flag.

Check AI functionality is available in the current instance of Burp Suite using the ai.isEnabled() method.

This ensures that the Use AI checkbox appears for users and that your extension handles scenarios where AI features are unavailable.

More information

For more information, see Developing AI features in extensions - Checking AI availability.

Mitigate prompt injection attacks

Treat raw output from AI models as untrusted. Escape any AI-generated content before presenting it to users. Make sure that you use proper HTML encoding to neutralize potential threats.

Optimize AI requests for efficiency and security

To ensure AI interactions are both efficient and secure, it's important to control what data is sent, how it's formatted, and when requests are made.

To optimize requests effectively:

Only send essential data. For example, avoid including full HTTP requests if only headers or parameters are needed, and only send traffic that is in-scope for the application you are testing.

Where possible, strip out sensitive data such as authentication tokens or session cookies.

Use structured data formats like JSON instead of free-text input to prevent prompt injection. Structured formats enforce a strict schema, making it harder for attackers to manipulate AI prompts. Since JSON strings are automatically escaped, they prevent unintended input injection.

Validate and encode outgoing data before sending it, to prevent prompt injection or unintended execution.

Consider implementing a cache to optimize credit usage and improve response times. For example, you can hash the temperature, system message, and prompt to check whether a request has already been made with the same parameters, and serve the cached response instead of sending a new prompt.

Use effective prompts

A well-structured prompt ensures that the AI provides relevant and high-quality responses. We recommend that you:

Provide background information to improve accuracy.

Define the AI's role at the start of the conversation.

Clearly specify what you want the AI to do.

More information

For more information, see Developing AI features in extensions - Sending prompts and handling responses.

Use lower temperatures for better accuracy

The temperature setting controls the balance between determinism and creativity in AI responses. In general, lower values produce focused and accurate results. The default is 0.5. Conversely, higher values may cause the AI to go off on tangents, potentially making security-related responses unreliable.

More information

For more information, see Developing AI features in extensions - Setting the temperature.

Handle exceptions gracefully

AI calls can fail for various reasons, such as the user not having enough credits or service downtime. Handle exceptions gracefully to ensure your extension is able to continue functioning as expected for your users.

The PromptException class represents errors that may occur during AI prompt execution. It is thrown if there is an issue with the AI request. Wrap AI calls in a try-catch block to handle errors appropriately.

More information

For more information, see Developing AI features in extensions - Handling exceptions.

Use an executor service where necessary to avoid blocking threads

AI requests can take longer than typical Burp API calls. Running them in the Swing Event Dispatch Thread can cause Burp to appear unresponsive, as the whole GUI must wait until the slow operation completes.

To keep Burp's UI responsive, execute AI calls asynchronously using an executor service. This prevents long-running operations from locking the Swing thread.

Integrating with third-party LLM providers

Your extension must use Burp AI as the default AI provider. You can also use third-party providers in addition to Burp AI.

If your extension integrates with a third-party provider, then it must:

Still declare AI support and check availability before issuing any requests.

Use the Montoya API networking capabilities for all requests to the third-party provider.

Use RequestOptions.withUpstreamTLSVerification() to verify the integrity of all data sent to the third-party provider.
