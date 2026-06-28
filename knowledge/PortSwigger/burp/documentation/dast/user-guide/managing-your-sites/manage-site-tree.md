# Managing the site tree

Source: https://portswigger.net/burp/documentation/dast/user-guide/managing-your-sites/manage-site-tree
Fetched: 2026-06-28T09:15:38.173989+00:00

DAST

Managing the site tree

Last updated:

June 18, 2026

Read time:

3 Minutes

Cloud

Self-hosted

As you add more sites to Burp Suite DAST, you may find it useful to organize those sites into folders. For example, you could group your sites based on their physical location.

Each folder has its own dashboard, enabling you to view aggregated charts and statistics for all the sites in the folder. You can also use folders to restrict access to sites, to make sure that users can only access data for sites that are relevant to them.

You can manage your folders and subfolders using the site tree, located on the Sites page.

You can also add tags to your sites or folders. This enables you to organize sites any way you want. For example, you could create tags for the following:

Geographic locations or time zones

Specific teams

Different levels of criticality

For more information, see Adding tags to sites.

Creating folders and subfolders

To create a new folder:

On the top menu, select Sites to display the site tree.

Click New folder. The New Folder dialog opens.

Enter a Folder Name. Make sure there are no other folders in the parent folder with the same name.

Optionally, you can add a Description to your folder.

If you want to add the folder to an existing folder, select a parent from the site tree under Add to existing folder.

Click Add to add your new folder.

Adding individual sites to a folder

You can select a folder when you initially add a site using the Site folder field on the Create a new site page.

To add an existing site to a folder:

On the top menu, select Sites to display the site tree.

Select the site you want to move.

Select the Details tab.

Click Edit.

Select the relevant folder from the Site folder field.

Click Save to add the site to the folder.

Moving sites and folders in bulk

To move multiple sites or folders at the same time:

On the top menu, select Sites to display the site tree.

Use the checkboxes in the list to select the sites you want to add.

In the popup menu, click Move.

In the Select a destination folder window, select the folder you want to add the sites to.

Click Move and then click OK to close the dialog.

If you click Move on the dialog without selecting a destination folder then Burp Suite DAST moves the selected sites and folders to the root level of the site tree.

Deleting sites and folders

To delete an individual site or folder, click its delete icon.

To delete multiple sites or folders at the same time:

On the top menu, select Sites to display the site tree.

Use the checkboxes in the list to select the sites or folders you want to delete.

In the popup menu, click Delete.

In the Confirm delete dialog, click Delete.

Related pages

Restricting access to sites - explains how to user folders to restrict site access for selected users.

Folder-level view - explains the folder-level dashboard in more detail.

Add new sites - explains how to add a new site to Burp Suite DAST.

Bulk actions reference page.
