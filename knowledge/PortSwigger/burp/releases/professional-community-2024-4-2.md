# Professional / Community 2024.4.2

Source: https://portswigger.net/burp/releases/professional-community-2024-4-2
Fetched: 2026-06-28T09:16:46.528242+00:00

This release fixes a bug where Burp wasn't using its own network settings when fetching URLs in the API scan launcher. This meant that you weren't able to upload API definitions if the host servers required specific network configurations. Burp now applies all network settings that are specified. This enables you to upload API definitions from URLs that use self-signed certificates or an upstream proxy, for example.
