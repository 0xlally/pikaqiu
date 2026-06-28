# Creating project files

Source: https://portswigger.net/burp/documentation/desktop/projects/create-project-file
Fetched: 2026-06-28T09:15:51.655660+00:00

Support Center

Documentation

Desktop editions

Project files

Creating project files

Professional

Creating project files

Last updated:

June 18, 2026

Read time:

2 Minutes

Burp Suite project files enable you to manage your work. You can use projects to store work for specific tasks or target applications.

Each time you start Burp, you are prompted to create or open a project file by the startup wizard.

You can create two types of Burp project:

Temporary projects are useful for quick tasks where your work doesn't need to be permanently saved. All data is held in memory, and is lost when you exit Burp.

Disk-based projects enable you to save your work and resume it later. All data is held on disk in a project file.

Note

Due to the way our persistence framework operates, we recommend that you use a local drive to save project files.

When you create a project file, you can select the configuration. This enables you to customize the project for particular tasks or clients.

To create a new disk-based project file:

Start Burp.

Select New project on disk.

Enter a name and choose a file, and click Next.

Choose from the following configurations:

Use Burp defaults - Open the project using Burp's default settings.

Use settings saved with project - This is only available when you reopen a project. It opens with the same settings that were selected the last time that you closed the project file.

Load from configuration file - Use the settings stored in a Burp configuration file. Only the project-level settings are loaded: user-level settings are ignored. For more information, see Configuration files.

Click Start Burp.

Opening a project file

To reopen a project file when Burp starts, select Open existing project in the startup wizard or use command line arguments. Burp reloads the most recent project data and configuration settings.

Note

If the project file was created in a different instance of Burp, you are asked if you want to take full ownership of the project.

If work is likely to continue on the project in another instance of Burp, and the Burp Collaborator identifier was saved with the project file, this means that you will share the identifier. In this situation we recommend that you don't take full ownership. This is because if you share the Burp Collaborator identifier, it can cause errors. For more information, see Saving the Burp Collaborator identifier.
