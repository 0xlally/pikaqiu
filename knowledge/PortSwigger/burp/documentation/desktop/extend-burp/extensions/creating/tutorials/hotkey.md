# Adding a hotkey to your Burp extension

Source: https://portswigger.net/burp/documentation/desktop/extend-burp/extensions/creating/tutorials/hotkey
Fetched: 2026-06-28T09:15:48.217863+00:00

Support Center

Documentation

Desktop editions

Extending Burp

Extensions

Creating

Tutorials

Adding a hotkey

ProfessionalCommunity Edition

Adding a hotkey to your Burp extension

Last updated:

June 18, 2026

Read time:

2 Minutes

Hotkeys enable users to trigger functionality directly from their keyboard, without navigating menus or dialogs. You can currently register hotkeys that are active when a user has focus in a HTTP message editor.

Adding a hotkey also makes your command available in the command palette, so users can quickly find and run it.

Note

If you prefer to review the full example before exploring the individual steps in the tutorial, see the complete

code at the bottom of this page.

Step 1: Register the hotkey

Create a HotKey object with a descriptive name and a key combination.

HotKey hotKey = HotKey.hotKey("Copy header names to clipboard", "Ctrl+Alt+H");

Step 2: Create the handler

Implement a HotKeyHandler to define what happens when the user presses the hotkey.

HotKeyHandler handler = event -> event.messageEditorRequestResponse().ifPresent(editor -> {

// Implement your action

Step 3: Implement your action

Decide what you want your handler to do when the hotkey is pressed.

In this example, the handler sends the selected message to Repeater, using the host name as part of the Repeater tab name so users can easily identify where it came from.

HttpRequest request = editor.requestResponse().request();

String caption = "From hotkey: " + request.httpService().host();

api.repeater().sendToRepeater(request, caption);

In this example, the handler copies all header names from the selected message to the clipboard. If the user is viewing the request, it copies the request headers. Otherwise, it copies the response headers. The action automatically respects the user's current focus in the message editor.

SelectionContext selectionContext = editor.selectionContext();

HttpRequestResponse requestResponse = editor.requestResponse();

List<HttpHeader> headers =

selectionContext == SelectionContext.REQUEST

? requestResponse.request().headers()

: requestResponse.response().headers();

String joinedHeaders = headers.stream()

.map(HttpHeader::name)

.collect(Collectors.joining(","));

Clipboard clipboard = Toolkit.getDefaultToolkit().getSystemClipboard();

clipboard.setContents(new StringSelection(joinedHeaders), null);

Step 4: Register the hotkey

Finally, register the hotkey and its handler. They must be registered in the HTTP message editor context.

api.userInterface().registerHotKeyHandler(HotKeyContext.HTTP_MESSAGE_EDITOR, hotKey, handler);

Once registered, your command appears in the command palette and can be triggered using the assigned shortcut.

Complete code

Here's the full example for reference:

import burp.api.montoya.BurpExtension;

import burp.api.montoya.MontoyaApi;

import burp.api.montoya.http.message.HttpHeader;

import burp.api.montoya.http.message.HttpRequestResponse;

import burp.api.montoya.ui.contextmenu.MessageEditorHttpRequestResponse.SelectionContext;

import burp.api.montoya.ui.hotkey.HotKeyContext;

import burp.api.montoya.ui.hotkey.HotKeyHandler;

import burp.api.montoya.ui.hotkey.HotKey;

import java.awt.*;

import java.awt.datatransfer.Clipboard;

import java.awt.datatransfer.StringSelection;

import java.util.List;

import java.util.stream.Collectors;

public class HotKeyExtension implements BurpExtension {

@Override

public void initialize(MontoyaApi api) {

api.extension().setName("Extension with hotkey");

HotKey hotKey = HotKey.hotKey("Copy header names to clipboard", "Ctrl+Alt+H");

HotKeyHandler handler = event -> event.messageEditorRequestResponse().ifPresent(editor -> {

SelectionContext selectionContext = editor.selectionContext();

HttpRequestResponse requestResponse = editor.requestResponse();

List<HttpHeader> headers =

selectionContext == SelectionContext.REQUEST

? requestResponse.request().headers()

: requestResponse.response().headers();

String joinedHeaders = headers.stream()

.map(HttpHeader::name)

.collect(Collectors.joining(","));

Clipboard clipboard = Toolkit.getDefaultToolkit().getSystemClipboard();

clipboard.setContents(new StringSelection(joinedHeaders), null);

});

api.userInterface().registerHotKeyHandler(

HotKeyContext.HTTP_MESSAGE_EDITOR,

hotKey,

handler

);

}

}

Related pages

Command palette
