# SIF2CSV
# Language: Python
# Input: SIF file
# Output: CSV file
# Tested with: PluMA 1.1, Python 3.6

PluMA plugin that takes as input a file in the Simple Interaction Format (SIF) and converts it to a CSV file,
estimating correlations.

Any of the following interactions in the SIF file will be estimated, with the following values:

directlyIncreases	0.99
directlyDecreases	-0.99
increase		0.5
decreases		-0.5
positiveCorrelation	0.5
negativeCorrelation	0.5
association		0.25
actsIn			0.25

Membership (i.e. is-a and hasMember) relationships are also taking into account.


