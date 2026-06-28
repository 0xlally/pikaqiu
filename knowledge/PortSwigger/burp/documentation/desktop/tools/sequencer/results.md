# Burp Sequencer analysis results

Source: https://portswigger.net/burp/documentation/desktop/tools/sequencer/results
Fetched: 2026-06-28T09:16:08.691977+00:00

Support Center

Documentation

Desktop editions

Tools

Sequencer

Results

ProfessionalCommunity Edition

Burp Sequencer analysis results

Last updated:

June 18, 2026

Read time:

4 Minutes

You can view the Burp Sequencer analysis results in the results window tabs. These are populated during the analysis. The tabs include an overall result summary, and details of each individual test.

Summary

The Summary tab contains a summary of the results compiled from all tests.

Overall result

Burp generates an overall estimate of the quality of randomness in the captured tokens.

Effective entropy

The Effective entropy chart shows the number of bits that pass the randomness tests at various significance levels, ranging from > 0.001% to 10%.

In most cases, the Effective entropy chart shows that the choice of significance level is not important. This occurs when the tokens possess either a clearly satisfactory or clearly unsatisfactory amount of randomness for any of the significance levels.

Related pages

For more information on how the Sequencer tests work, and how to choose a significance level, see Burp Sequencer randomness tests.

Reliability

Sequencer estimates the reliability of the results based on the sample size. As with any statistical-based test for randomness, the test results may contain false negatives and positives. Treat the results as an indicative guide to the randomness of the sampled data.

Data that is generated in a deterministic way may be deemed random. For example, a well-designed linear congruential pseudo-random number generator, or an algorithm which calculates the hash of a sequential number, may appear to generate random output. However, an attacker who knows the internal state of the generator can reliably extrapolate its output in both forwards and reverse directions.

Data deemed to be non-random may not actually be predictable. For example, when the patterns that are discernible within the data do not sufficiently narrow down the range of possible future outputs to a range that can be viably tested.

Sample

The Summary tab contains details of the sample, including:

The sample size.

The token length range.

The number of tokens that were padded.

Analysis result tabs

The Character-level analysis and Bit-level analysis tabs contain a summary of the results for each analysis type, and details of individual tests. These tabs enable you to:

Gain a deeper understanding of the properties of the sample.

Identify the causes of any anomalies.

Assess the possibilities for token prediction.

Note

The Character-level analysis tab may not be populated for your analysis. This occurs because Burp Sequencer disables the character-level tests at low sample sizes. This prevents unreliable character-level results from undermining the overall conclusion.

Character-level tests are deemed unreliable if the size of the character sets is too large relative to the number of samples. For example, you can't draw a reliable conclusion from a sample size of 100 if a token uses 64 different characters at each position.

Summary

Each tab contains two charts that summarize the results compiled from the character-level or bit-level tests:

Significance levels chart - This shows the lowest overall probability of the observed results occurring for each character or bit position, if the results are randomly generated. It enables you to quickly gauge the randomness of the sample at each position against various significance levels.

Effective entropy chart - This shows the number of bits of effective entropy at each significance level, based on all character-level or bit-level tests. It enables you to quickly measure the number of bits that pass that test type for each significance level.

Related pages

For more information on how the tests work, see Burp Sequencer randomness tests.

Individual tests

Both the character-level and bit-level analysis tabs contain details of each individual test:

Significance levels chart - This shows the lowest overall probability of the results occurring for each

character or bit position, if the results are randomly generated. This enables you to quickly gauge the

randomness of the sample at each position, based on a single test.

Anomalies - Details of any anomalies identified in the test.

Test description - A description of how the test determines whether a sample is randomly generated.

FIPS result - For FIPS tests, a FIPS pass or fail result. Any bits that failed the test are identified.

Related pages

For detailed information on the individual tests used in the analysis, see Burp Sequencer randomness

tests.

Character set

The Character-level analysis tab contains two charts that summarize the number of characters and maximum bits of entropy at each character position:

Character set chart - This shows the number of different characters that appear at each position.

Maximum entropy bits chart - This shows the maximum bits of entropy available at each position, given the size of the character set used at that position. This data is used to calculate the effective entropy for the character-level analysis.

Note

If a position has a character set with a size that isn't a round power of two, the sample data at that position is translated into a character set with a size that is the nearest smaller round power of two. The partial bit of data at the position is merged into the whole bits derived from that position.

This translation is done in a way that preserves the randomness characteristics of the original sample, without introducing or removing any bias. However, it is likely the process of analyzing samples with non-round character set sizes will introduce some inaccuracies into the analysis results.

Bit conversion

The Bit-level analysis tab contains a chart that shows the number of bits contributed by each character position in the token. This enables you to cross-reference individual bits within the token back to the original character positions.

Analysis settings tab

The Analysis settings tab enables you to view and modify the analysis settings, then redo the analysis. For more information, see Sequencer settings.
