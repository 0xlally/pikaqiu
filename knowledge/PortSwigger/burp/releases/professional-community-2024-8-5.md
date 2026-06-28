# Professional / Community 2024.8.5

Source: https://portswigger.net/burp/releases/professional-community-2024-8-5
Fetched: 2026-06-28T09:16:49.745319+00:00

We've fixed a bug where project files were sometimes incorrectly saved to the working directory. Now, if a project was previously saved to a specific folder and that folder is still accessible, the project will be saved there by default. Otherwise, it will be saved in the user home directory.
