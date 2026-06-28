# Performing bulk actions in the site tree

Source: https://portswigger.net/burp/documentation/dast/user-guide/reference/bulk-actions-site-tree
Fetched: 2026-06-28T09:15:39.910910+00:00

DAST

Performing bulk actions in the site tree

Last updated:

June 18, 2026

Read time:

1 Minute

The bulk actions menu enables you to perform the following tasks across multiple sites or folders at once:

Launching a scan of the selected sites.

Moving the selected sites to a different folder.

Deleting the selected sites.

The bulk actions menu is displayed when you use the checkboxes to select sites or folders on the Sites page.

Permissions for bulk actions

The bulk actions available to you depend on your permissions:

If you do not have permission to perform a particular action on any of the selected items, the action is grayed out.

If you have permission to perform a particular action on some of the selected items, you can still select that action. The subsequent dialog displays a padlock icon next to the sites or folders that you do not have permission to edit. These items are skipped when the action runs.

Selecting a folder selects all the sites and subdirectories of that folder. However, some folders may contain sites that are not visible due to your permissions, which may prevent you from performing the chosen action on the folder. If this happens, you should deselect the folder and select all of the visible sites instead.

Related pages

Managing the site tree.

Importing sites in bulk.
