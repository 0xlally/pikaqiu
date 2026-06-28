# Burp Sequencer live capture

Source: https://portswigger.net/burp/documentation/desktop/tools/sequencer/sample/live-capture
Fetched: 2026-06-28T09:16:08.686125+00:00

Support Center

Documentation

Desktop editions

Tools

Sequencer

Token sample

Live capture

ProfessionalCommunity Edition

Burp Sequencer live capture

Last updated:

June 18, 2026

Read time:

1 Minute

When you start a live capture, Burp Sequencer repeatedly issues the request and extracts the relevant token from the application's responses. This occurs in a new results window.

The results window contains a progress bar, and real-time details of the:

Number of requests made.

Number of tokens captured.

Number of errors found.

The buttons in the results window enable you to control aspects of the capture:

Pause or Resume - Temporarily pause and resume the capture.

Stop - Permanently stop the capture.

Copy tokens - Copy the captured tokens to the clipboard.

Save tokens - Save the captured tokens as a file.

Analyze now - Analyze the current sample of tokens. You need a minimum of 100 captured tokens to perform the analysis.

Auto-analyze - Perform automatic analysis periodically during the live capture.

You can use the copied or saved tokens as payloads for Burp Intruder or Burp Scanner. You can also manually load them in a future Sequencer analysis.

Related pages

For instructions on how to set up a live capture, see Obtaining a token sample.

For information on live capture settings, see Sequencer settings.

To learn how the results are displayed, see Burp Sequencer results.
