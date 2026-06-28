# Project files

Source: https://portswigger.net/burp/documentation/desktop/projects
Fetched: 2026-06-28T09:15:51.953432+00:00

Support Center

Documentation

Desktop editions

Project files

Professional

Project files

Last updated:

June 18, 2026

Read time:

2 Minutes

You can hold all the data and configuration settings for a particular piece of work in a Burp project file. The file saves data incrementally as you work. There is no need to manually save your work.

Note

When you test some applications, it can generate several gigabytes of data. Make sure that you have sufficient free disk space available when you use Burp project files.

You can select or create a project file from the startup wizard. The options available depend on which edition of Burp Suite you use:

Temporary project in memory Professional Community - Select this option for quick tasks where you don't need to save your work. All data is held in memory and is lost when you close Burp.

New project on disk Professional - Create a new project file. This file holds all of the data and configuration for the project.

Open existing project Professional - Reopen a project file. You can choose from a list of recently opened projects.

Warning

You can import project and configuration files from other users. However, for security reasons, we recommend only importing project and configuration files from trusted sources.

This video shows you how to create new projects and open existing projects. It also shows you how to copy and import project files.

Opening an existing project file

If you open an existing project file, you can select the following settings from the startup wizard:

Pause Automated Tasks

This setting can protect you from sending requests that could be set to automatically run when you open a Burp project file. We recommend this setting if the project file is from an unknown or untrusted source.

Select Pause Automated Tasks if you do not want automated tasks to run when you open projects.

Note

If you deselect Trust this project file, automated tasks are paused by default.

Trust this project file

This setting can protect you from potentially harmful settings that could be configured within a Burp project file.

Deselect Trust this project if you want Burp to remove any potentially harmful settings before opening projects. This also pauses any automated tasks configured within the project.

Note

We do not recommend proxying traffic through an untrusted project file, even if you deselect Trust this

project.

Related pages

Creating project files.

Managing project files.

Startup behavior settings.
