# Professional / Community 2024.11

Source: https://portswigger.net/burp/releases/professional-community-2024-11
Fetched: 2026-06-28T09:16:45.898497+00:00

This release introduces site map filter Bambdas, match and replace Bambdas, dynamic authentication tokens for API scanning, and Enhanced payload management for Intruder attacks. We’ve also made several quality of life improvements, performance improvements, and some bug fixes.

Filtering the site map with Bambdas

We're introducing Bambdas into more areas of Burp. These Java-based code snippets enable you to customize Burp directly from the UI.

This release introduces Bambdas into the site map filter. This enables you to customize the site map to capture exactly what you need, helping you to focus your analysis by filtering out unnecessary traffic.

To learn more about Bambdas in Burp, see Bambdas.

Advanced match and replace rules with Bambdas

We've extended the capabilities of match and replace Bambdas by adding access to a subset of the MontoyaAPI functionality. This enables you to create more complex Bambdas for advanced use cases.

Please use the MontoyaAPI

functionality carefully. While we've restricted access to known dangerous functionality, certain methods may still potentially impact Burp's performance or cause memory leaks.

Dynamic authentication tokens for API-only scans

We’ve introduced support for dynamic authentication tokens in API-only scans. Burp can now automatically handle token renewal during scans, ensuring uninterrupted access to secured endpoints without the need for you to intervene.

This functionality is available for bearer tokens and our new custom method, which gives you the flexibility to specify where the token is placed in requests. Both methods support fixed and dynamic tokens.

Enhanced payload management for Intruder attacks

We've made a number of changes to improve payload marker handling when configuring Intruder attacks.

The use of the § character as a payload marker is now purely visual. This means that you can run an Intruder attack on a request that includes the § character - it won't be interpreted as defining a payload position.

When you're configuring a Pitchfork or Cluster bomb attack, the Payload position dropdown in the Payloads side panel now shows the enclosed text of the payload position as well as the payload position number. In addition, if you click a payload position in the request, Burp automatically selects the corresponding item from the Payload position dropdown. These updates help you quickly identify and manage payload sets when configuring an attack.

Output console for debugging Bambdas

We’ve added the ability to print or log output to a console when writing Bambdas. Use the provided logging object to debug more efficiently with real-time feedback on code execution, making it easy to inspect variables, track errors, and test your code.

Quality of life improvements

We've made the following quality of life improvements:

We've added a new setting that allows you to choose whether Burp Suite prioritizes IPv4 or IPv6 for DNS resolution. This is especially useful if your routing restrictions allow only IPv4 or IPv6 traffic.

The cookie jar now displays whether each cookie has HTTPOnly and Secure flags, giving you a more complete view of cookie attributes.

Performance improvements

We've made the following performance improvements:

The scanner now prioritizes authenticated items over unauthenticated ones when all other factors are the same.

We’ve improved the scanner’s ability to parse large resource files, significantly reducing processing times that were sometimes causing scans to time out.

Bug fixes

We've fixed the following bugs:

A bug in the recorded logins replayer causing drop-down selections to reset incorrectly.

A bug in the recorded logins recorder causing it to capture only partial login sequences, and preventing logins from being copied to the clipboard.

Browser upgrade

We've upgraded Burp's browser to Chromium 131.0.6778.86 for Windows & Mac and 131.0.6778.85 for Linux. For more information, see the Chromium release notes.
