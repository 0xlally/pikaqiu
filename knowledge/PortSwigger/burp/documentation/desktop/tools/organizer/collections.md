# Collections

Source: https://portswigger.net/burp/documentation/desktop/tools/organizer/collections
Fetched: 2026-06-28T09:16:06.472636+00:00

Support Center

Documentation

Desktop editions

Tools

Organizer

Collections

ProfessionalCommunity Edition

Collections

Last updated:

June 18, 2026

Read time:

3 Minutes

Collections provide a way to group HTTP messages in a way that suits your testing workflow. They help you organize findings and track progress across related requests and responses. You can create and manage collections in Burp Organizer.

Professional You can also share collections with other Burp users.

This provides a secure way to share findings, reproduction steps, or proof-of-concept requests without relying on manual workarounds such as copying and pasting.

Learn more about Sharing collections.

Creating new collections

To create a new collection, click New. Burp creates a new empty collection ready for you to move or copy messages into it.

Moving messages into collections

Moving messages removes them from their current collection and places them into another collection. This is useful for triaging messages out of the inbox or reorganizing work as testing progresses.

To move messages:

In Organizer, select one or more messages.

Right-click and select Move to...

Select the collection you want to move the messages to.

Copying messages into collections

Copying messages leaves the original message in place, and creates a copy of it in another collection. This is useful when the same request or response is relevant to multiple areas of testing.

To copy messages:

In Organizer, select one or more messages.

Right-click and select Copy to...

Select the collection you want to copy the messages to.

Managing collections

You can rename, duplicate, and delete a collection by right-clicking it, then selecting the relevant option from the list.

You can also add notes to a collection using the About tab. Like notes on individual messages, these help you capture context, goals, or summaries.

However, collection notes apply to the collection as a whole, making them useful for describing its purpose, scope, or overall findings.

Note

If you delete a collection that contains messages, you can choose to move these back into the inbox, or delete them from Organizer along with the collection.

While a collection is shared, it is read-only. You must unshare the collection before you can modify or delete it.

Sharing collections

Professional

Sharing a collection encrypts its contents on your device, uploads the encrypted data to PortSwigger servers, and generates a link that you can share with other Burp Suite Professional users.

Any Burp Suite Professional user with the link can import the collection into their own Organizer. Once imported, the messages can be worked with like any other Organizer items.

Only share links with recipients who are authorized to view all included data and avoid posting links in untrusted locations.

Shared links expire after 90 days.

To share a collection:

Right-click a collection.

Select Share collection.

Burp automatically copies the collection link to your clipboard.

Note

If Burp doesn't open automatically, launch it manually and follow the steps in Importing collections manually.

To stop sharing a collection:

Right-click a shared collection.

Select Unshare collection.

The collection data is deleted from the PortSwigger servers, and the link can no longer be accessed.

Note

Any collection data that has already been imported by another user will not be affected by unsharing its original collection.

If you unshare a collection and then share it again, Burp generates a new link. Previously generated links will no longer work.

Importing collections

Professional

To import a collection:

Open the collection link in your browser.

Burp Suite opens automatically and displays a confirmation dialog.

Click Import to import the collection.

Note

If Burp doesn't open automatically, launch it manually and follow the steps in Importing collections manually.

Burp decrypts the collection and adds its messages to Organizer. You can now send the imported messages to other Burp tools, and work with them as you would with any other message.

Importing collections manually

Professional

If your system doesn't support automatic handling of collection links (for example, some Linux setups might not register the required protocol handler),

you can import a collection manually by pasting the collection URL into Burp Suite Professional's command palette.
