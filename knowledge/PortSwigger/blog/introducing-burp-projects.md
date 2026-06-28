# Introducing Burp Projects

Source: https://portswigger.net/blog/introducing-burp-projects
Fetched: 2026-06-28T09:15:17.802127+00:00

Introducing Burp Projects

Dafydd Stuttard |

Friday, 8 April 2016 at 16:52 UTC

The latest major release of Burp introduces some great new capabilities for handling Burp's data and configuration. This blog post covers the following areas:

Burp project files

Changes to Burp's configuration options

Configuration files

The new startup wizard

New APIs

New command line arguments

Transitioning existing data and configuration

Feature roadmap

Burp project files

Burp's new project files are used to hold all of the data and configuration for a particular piece of work. Data is saved incrementally into the file as you work. When you reopen an existing project, Burp reloads the project's data and configuration, and you can resume working where you left off.

Burp project files are a replacement for the existing state file functionality, and are significantly superior in various ways:

Data is saved automatically in real time. There is no need to specifically save your work when you are finished. If Burp exits abnormally, all its data is preserved.

Burp reopens project files considerably faster than state files. In our testing, project files that are several gigabytes in size can be reopened in a few seconds.

A problem with Burp's non-incremental automatic backup feature, where each periodic backup consumed more and more disk space, has gone away.

All data is held in the project file, including some items that were not previously included in state files, such as the Scanner's issue activity log.

Note: The new project files feature is not available on 32-bit platforms or in the free edition of Burp.

Changes to Burp's configuration options

Burp's configuration options have been split into two groups: user options and project options. This has been done to make it easier to work with Burp's configuration when dealing with multiple separate projects.

User-level options are those relating to the individual user's environment and UI, including:

Everything in the new "User options" tab, such as font settings.

Options in the Extender tool, including the list of configured extensions.

UI-related options in other tools, such as the selected view of the Target site map.

Project-level options are those relating to the work that is being performed on a particular target application, including:

Everything in the new "Project options" tab, such as session handling rules.

Non-UI-related options in individual Burp tools, such as Proxy and Scanner.

User-level options will typically be long-lived and are automatically preserved across different Burp sessions. Project-level options are not automatically preserved in the same way. Rather, they are stored within project files and configuration files.

Some options, such as upstream proxy settings, can be defined at both the project and user level. For these options, you can configure your normal options at the user level, and then override these if required on a per-project basis. For example, you might normally use a corporate LAN proxy to connect to the Internet, and you can configure this in your user-level settings. For particular projects, when testing an internal application or on site at a particular client, you might need to use a different upstream proxy or none at all. You can configure this in your project-level settings for the relevant projects.

Configuration files

You can use Burp's new configuration files to manage different configurations for particular tasks. For example, you might need to load a particular configuration when working on a particular client. Or you might create different configurations for different types of scans.

Separate configuration files can be used to manage user-level and project-level options.

You can load and save configuration files in various ways:

From the Burp menu, you can load or save configuration files for all user-level or project-level options:

From individual configuration panels throughout Burp, you can use the new "Options" button to load or save the configuration for just that panel:

In the new startup wizard, when creating or reopening a project, you can specify a configuration file from which to load project-level options:

When starting Burp from the command line, you can use the new command line arguments to specify one or more configuration files from which to load project-level options.

Burp extensions can load or save project-level configuration file contents via the new APIs.

Configuration files use the JSON format. The structure and naming scheme used within the JSON correspond to the way that options are presented within the Burp UI. The easiest way to generate a configuration file for a particular purpose is to create the desired configuration within the Burp UI and save a configuration file from it. If preferred, you can also hand-edit an existing configuration file, since the contents are human-readable and self-documenting:

Partial configuration files can be used when needed. You can create a partial configuration file by saving the configuration of just one area of Burp, via the new "Options" button on each configuration panel, or by removing the unneeded sections from a full configuration file. When a partial configuration file is loaded, any options that are not defined within that file are left unchanged. This allows you to create small focused partial configuration files for common purposes, and load them when required to create a desired overall configuration.

New APIs

There are two new APIs that extensions can use to manage project-level options:

void loadConfigFromJson(String config);

String saveConfigAsJson(String... configPaths);

Both methods handle settings using the new JSON format that is used in configuration files.

The load method takes a String containing some configuration options, and updates Burp with the specified options. Partial configurations are acceptable, and any settings not specified will be left unmodified.

The save method by default saves the entire project-level configuration. To include only certain sections of the configuration, you can optionally supply the path to each section that should be included, for example: "project_options.connections".

The APIs only operate on project-level options, and user-level options cannot be loaded or saved via the API.

The old API methods for processing options via maps of name/value pairs, and for saving and loading state files, are now deprecated and will be removed at some future point.

The new startup wizard

When Burp launches, a new startup wizard is displayed.

The first screen lets you choose what Burp project to open:

You can choose from the following options to create or open a project:

Temporary project - This option is useful for quick tasks where your work doesn't need to be saved. All data is held in memory, and is lost when Burp exits.

New project on disk - This creates a new project that will store its data in a Burp project file. This file will hold all of the data and configuration for the project, and data is saved incrementally as you work. You can also specify a name for the project.

Open existing project - This reopens an existing project from a Burp project file. A list of recently opened projects is shown for quick selection. When this option is selected, the Spider and Scanner tools will be automatically paused when the project reopens, to avoid sending any unintentional requests to existing configured targets. You can deselect this option if preferred.

Note: You can rename a project later via the Burp menu.

The next screen lets you choose what project configuration to use:

You can choose from the following options for the project configuration:

Use Burp defaults - This will open the project using Burp's default options.

Use options saved with project - This is only available when reopening an existing project, and will open the project using the options that were saved in the project file.

Load from configuration file - This will open the project using the options contained in the selected Burp configuration file. Note that only project-level options in the configuration file will be reloaded, and any user-level options will be ignored. A list of recently used configuration files is shown for quick selection.

New command line arguments

There are two new command line arguments to facilitate working with Burp projects and configuration files:

--project-file=filename  Opens the specified project file. The file will be created as a new project if it does not already exist.

--config-file=filename  Loads the specified project configuration file(s). This option may be repeated to load multiple files.

The new command line arguments are particularly useful for the following purposes:

When automating Burp from scripts or other processes, you can launch Burp with a specified project file and configuration file. For example, your CI pipeline could launch Burp specifying the filename into which the project will be saved as an artifact, and a configuration file containing details of target scope or scanning options.

If you create different configuration files for common purposes, you can create desktop shortcuts to launch Burp with different configurations. When Burp is launched with the config-file option, the startup wizard will skip the step to select a configuration file, thereby speeding up the startup process.

Transitioning existing data and configuration

The changes to Burp may require some action by users who want to continue working with existing data and configuration:

To transition data and configuration in an existing Burp state file, simply create a new Burp project, and then restore the state file in the normal way. All of the data and configuration from the state file will be stored in the project file, and this can then be reopened directly without need for the original state file.

Settings that are now part of user-level options (such as font settings) will automatically carry over from earlier versions of Burp.

Settings that are now part of project-level options (such as session handling rules) will not automatically carry over from earlier versions of Burp. If you have customized these in your locally saved settings, and want to use them in the new version, you'll need to use an old version of Burp to save a config-only state file, use the new version of Burp to restore that state file, and then save a configuration file containing the project-level options. When creating new Burp projects, you can select that configuration file in the startup wizard.

Feature roadmap

Burp's new capabilities surrounding projects and configuration are fully functional in their own terms, but give rise to a number of desirable features that will be added to Burp over the coming months:

If you launch Burp and choose to create a temporary project, it is not currently possible to change your mind and save your work into a disk-based project at a later time. We plan to provide a means of doing this.

Data is incrementally appended onto project files as it is generated. If you accumulate a large amount of data and then delete some of this within Burp (for example, by clearing a large Proxy history), the data is not actually removed from the project file, and the project file will not reduce in size. We plan to provide a means of compressing a project file to remove redundant data and reduce its size.

With the existing state file functionality, it is possible when saving a state file to select which tools' data to include, and whether to include only in-scope items. With the new project file feature, all of Burp's data is saved into the project file. We plan to provide a means of saving a project file that contains only selected items.

With the existing state file functionality, it is possible to restore multiple state files into the same instance of Burp, to merge the results of earlier work. With the new project file feature, only a single project file can be opened into each instance of Burp. We plan to provide a means of importing multiple project files to create a single combined project.

Intruder options are not currently handled by the new configuration file feature. We plan to provide a new way of handling Intruder configuration and attack data, based closely on the new Burp configuration and project files.

In parallel with the addition of the above features, some existing Burp features will be removed:

The automatic backup feature, which saves Burp's state periodically into state files, has been removed in the new release.

Existing APIs relating to configuration options and state files have been deprecated.

The ability to save new state files will be removed in the near term.

The ability to restore old state files will be removed in the longer term.

Dafydd Stuttard

@DafyddStuttard

Latest Posts

Burp Extensibility 2026: Awards, Talks, and Highlights

19 June 2026

Burp Extensibility 2026: Awards, Talks, and Highlights

The beast needs a cage: What's next for AppSec post-Mythos

12 May 2026

The beast needs a cage: What's next for AppSec post-Mythos

3 ways custom scan checks turn practitioner knowledge into scalable automation

01 May 2026

3 ways custom scan checks turn practitioner knowledge into scalable automation

Senior pentesters have a deeply refined intuition about what is vulnerable in an environment. The problem? That expertise is often siloed with an individual and trapped in their notes or Python scripts.
