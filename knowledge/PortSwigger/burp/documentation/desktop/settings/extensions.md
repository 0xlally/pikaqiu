# Extensions settings

Source: https://portswigger.net/burp/documentation/desktop/settings/extensions
Fetched: 2026-06-28T09:15:54.656002+00:00

Support Center

Documentation

Desktop editions

Settings

Extensions

ProfessionalCommunity Edition

Extensions settings

Last updated:

June 18, 2026

Read time:

3 Minutes

The Extensions section in the Settings dialog includes the following types of settings:

Core extension settings - Burp's built-in settings for loading and using extensions.

Extension-generated settings - Settings added by installed extensions. If an extension includes settings, you'll see a panel labeled with the extension's name.

The Core extension settings page contains settings for the following:

Startup behavior.

Load behavior.

Java environment.

Python environment.

Ruby environment.

Startup behavior

These settings determine how Burp Suite handles extensions on startup:

Automatically reload extensions on startup - Enable this setting to reload all extensions when you restart Burp. Note that even with this setting enabled, you can restart Burp without reloading extensions. Launch Burp from the command line, and use the --disable-extensions command line flag.

Automatically update installed BApps on startup - If you enable this setting, Burp automatically checks for updates to your installed extensions in the BApp Store.

Related pages

Launching Burp Suite from the command line.

Load behavior

This setting enables you to choose whether the Load Burp extension dialog appears when you reload an extension. By default, the dialog doesn't appear. If you want to view the dialog each time an extension is reloaded, deselect

Hide dialog when reloading.

Related pages

For instructions on how to quickly reload your extension in Burp, see Loading your extension in Burp - Reloading your extension.

Java environment

This setting enables you to specify a folder from which Burp can load Java libraries. Burp searches the specified folder and any subfolders for JAR files. It includes them in the classpath of the classloader that loads Java extensions.

Python environment

These settings enable you to configure the environment in which Python-based extensions are executed:

Location of the Jython standalone JAR file - Specify the location of a Jython standalone JAR file. When loaded, it shows the file location. Jython is a Python interpreter that runs on the Java platform. It enables extensions written in Python to interact with Burp's legacy Java-based Extender API.

Folder for loading modules - Specify the location of a folder containing Python modules. Burp updates the Python sys.path variable with the specified location. This is useful if you create your own set of Python modules for use with multiple separate extensions.

Related pages

You need to install Jython if you see a Download Jython button next to the extension in the BApp Store. For instructions on how to do this, see our troubleshooting guide.

You may encounter memory problems if you load several Python extensions. For more information, see our troubleshooting guide.

Ruby environment

This setting enables you to specify the location of JRuby standalone JAR file. When loaded, it shows the file location.

JRuby is a Ruby interpreter that runs on the Java platform. It enables extensions written in Ruby to interact with Burp's legacy Java-based Extender API.

Related pages

You need to install JRuby if you see a Download JRuby button next to the extension in the BApp Store. For instructions on how to do this, see our troubleshooting guide.

You may encounter memory problems if you load several Ruby extensions. For more information, see our troubleshooting guide.
