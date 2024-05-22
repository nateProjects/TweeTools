#!/usr/bin/perl

use strict;
use warnings;
use List::Util 'shuffle';

# Read the number of passages
my $num_passages = $ARGV[0] or die "Usage: $0 <number_of_passages>\n";

# Create an array of passage numbers
my @numbers = (1..$num_passages);

# Randomize the array after the first element
my @shuffled = (shift @numbers, shuffle @numbers);

# Print the randomized numbers
print join(",", @shuffled) . "\n";
