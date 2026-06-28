# Sequencer settings

Source: https://portswigger.net/burp/documentation/desktop/settings/tools/sequencer
Fetched: 2026-06-28T09:15:56.752790+00:00

Support Center

Documentation

Desktop editions

Settings

Tools

Sequencer

ProfessionalCommunity Edition

Sequencer settings

Last updated:

June 18, 2026

Read time:

2 Minutes

The Sequencer page in the Settings dialog contains settings for the following:

Live capture.

Token handling.

Token analysis.

The Sequencer settings are all project settings. They apply to the current project only.

Live capture

These settings control how Sequencer makes HTTP requests and harvests tokens during a live capture:

Number of threads - Specify the maximum number of concurrent requests that the live capture can make.

Throttle between requests - Specify a delay between each request, in milliseconds. This enables you to avoid overloading the application, or to be more stealthy in your approach.

Ignore token whose length deviates by X characters - Enable this setting to ignore tokens that deviate by a specified number of characters from the average token length. This setting is useful if the application occasionally returns a different item in the location where a token normally appears.

Related pages

For more information on the live capture process, see Burp Sequencer live capture.

Token handling

These settings control how tokens are handled during analysis:

Pad short tokens at start / end - The Sequencer statistical tests can only be performed on tokens of identical length. If the application produces tokens with a variable length, then the tokens are padded. You can choose whether padding is applied at the start or end of each token. In most cases, pad tokens at the start.

Pad - Specify the character that is used for padding. For numeric or ASCII hex-encoded tokens, the 0 character is usually most appropriate.

Base64-decode before analyzing - Enable this setting to decode any Base-64-encoded tokens before analysis. This generally improves the accuracy of the analysis.

Token analysis

This setting controls the tests that are performed during analysis. You can enable or disable each test individually.

This can be useful after you perform an initial analysis with all tests enabled. You can then disable individual tests to reflect your understanding of the tokens' characteristics, or to isolate the effects of unusual characteristics.

To re-perform an analysis:

Go to the results window.

Modify the settings in the Analysis settings tab.

Click Redo analysis.

Related pages

To learn how to obtain a sample of tokens for analysis, see Obtaining a token sample.

For more information on the individual tests performed by Sequencer, see Burp Sequencer randomness tests.
