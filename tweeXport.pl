#!/usr/bin/perl

use strict;
use warnings;
use Getopt::Long;

# Command-line options
my $passageNames = 0;
GetOptions(
    "passageNames!" => \$passageNames,
);

# Read the Twee file
my $file = $ARGV[0] or die "Usage: $0 [--passageNames] <file.twee>\n";
open my $fh, '<', $file or die "Can't open $file: $!\n";
my @lines = <$fh>;
close $fh;

# Parse the Twee file
my %passages;
my $current_passage;
my $number_counter = 0;  # Initialize counter
for my $line (@lines) {
    if ($line =~ /^:: (.+)$/) {
        $current_passage = $1;
        $passages{$current_passage} = { description => '', choices => [], number => ++$number_counter }; # Increment counter for each passage
    } elsif ($line =~ /\[(.+?)\]/) {
        my $link = $1;
        my ($display_text, $passage_link) = $link =~ /\|/ ? split(/\|/, $link) :
                                             $link =~ /->/ ? split(/->/, $link) : ($link, $link);
        push @{$passages{$current_passage}->{choices}}, [$display_text, $passage_link];
    } else {
        $passages{$current_passage}->{description} .= $line;
    }
}

# Create Markdown output
open my $md_fh, '>', "$file.md" or die "Can't create markdown file: $!\n";

# Output passages
for my $passage (sort { $passages{$a}->{number} <=> $passages{$b}->{number} } keys %passages) {
    my $heading = $passageNames ? $passage : "## $passages{$passage}->{number}"; # Handle passage names or numbering
    print $md_fh "$heading\n\n";
    print $md_fh $passages{$passage}->{description} . "\n\n";
    for my $choice (@{$passages{$passage}->{choices}}) {
        my $link_text = $choice->[0];
        my $link_target = $choice->[1];
        my $link_number = $passages{$link_target =~ /\|(.+)/ ? $1 : $link_target =~ /->(.+)/ ? $1 : $link_target}->{number};
        print $md_fh "**Go to $link_text - Page $link_number**\n\n";
    }
}

close $md_fh;

print "Markdown file created: $file.md\n";
