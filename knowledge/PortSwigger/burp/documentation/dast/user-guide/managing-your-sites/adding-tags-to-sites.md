# Adding tags to sites

Source: https://portswigger.net/burp/documentation/dast/user-guide/managing-your-sites/adding-tags-to-sites
Fetched: 2026-06-28T09:15:37.724250+00:00

DAST

Adding tags to sites

Last updated:

June 18, 2026

Read time:

3 Minutes

Cloud

Self-hosted

You can create and add tags to organize your sites or folders. Once you've added tags to your site, you can do the following:

Filter your sites and folders by tags

Add descriptions to your tags, such as region, owner, or importance

Note

If you apply a tag to a folder, you also apply it automatically to all the folder's sites and subfolders.

Permissions required to manage tags

To create, edit, or delete tags, you need to be assigned a role that has Manage tags permission. You need Edit sites and folders permission to add or remove tags from sites and folders.

To view tags, you only need permission to view the site. No extra permissions are required.

For more information about role-based permissions, see Role-based access control.

Creating tags

When you create a tag, you can choose the color and name. You can also add a detailed description.

On the Sites page, select the tick box for a site or folder in the site tree. The bottom menu appears.

From the bottom menu, select Tags.

Click Create new tag.

Enter a Tag name. You can also add a Description.

Select a color for your tag.

Click Save.

The tag now appears alphabetically in the list of tags.

Adding tags to a single site or folder

Go to the Sites page.

In the Tags column for your site or folder, click the button.

Select one or more tags to add to your site or folder.

Click Confirm.

Adding tags to multiple sites or folders

Go to the Sites page.

Select the tick box for the sites and folders that you want to tag. The bottom menu appears.

From the bottom menu, select Tags.

Select one or more tags.

Click Confirm.

The tags now appear in the Tags column for your selected sites and folders.

Filtering by tags

If you use tags to filter sites and folders, you only see sites and folders that you have permission to view. You don't need specific permissions to be able to filter by tags.

Go to the Sites page.

Click the Filter menu and select one or more tags to filter by.

The site list is now filtered by tagged sites, and folders that contain tagged sites.

Note

You can schedule scans for your filtered sites and folders. All the sites in a tagged folder will be scanned, even if you have untagged individual sites.

Untagging a single site or folder

Untagging a site of folder removes the tag from that site, but doesn't remove it from your library of tags. Use this method If you want to untag a folder, but leave the tag on its sites and subfolders.

Go to the Sites page.

In the Tags column, click the tag you want to remove from the site or folder. If the site has more than one tag, click the +n label to see more tags.

Click and then click Untag site.

Untagging multiple sites or folders

You can untag multiple sites or folders. Use this method if you want to untag a folder, and all its sites and subfolders.

To untag multiple sites and folders:

Go to the Sites page.

Select the sites and folders that you want to untag.

From the bottom menu, click Tags.

Deselect your chosen tags.

Click Confirm.

Editing tags

You can edit the name and description for tags, and change the color. If you edit a tag, you change it for every site that has the tag.

Go to the Sites page.

In the Tags column, click the tag you want to edit. If the site has more than one tag, click the +n label to see more tags.

Click and then click Edit tag.

Edit the tag.

Click Save.

Deleting tags

If you delete a tag, you remove it from every site and folder. You also remove it from your library.

Go to the Sites page.

In the Tags column, click the tag you want to delete. If the site or folder has more than one tag, click the +n label to see more tags.

Click , then click Delete tag. A dialog box appears.

To confirm, click Delete tag.
