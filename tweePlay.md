#!/usr/bin/perl

use strict;
use warnings;
use Getopt::Long;
use List::Util 'shuffle';

# Command-line options
my $show_passage_name = 1;
my $bookNums = 0;
GetOptions(
    "show-passage-name!" => \$show_passage_name,
    "bookNums!"          => \$bookNums,
);

# Read the Twee file
my $file = $ARGV[0] or die "Usage: $0 [--show-passage-name] [--bookNums] <file.twee>\n";
open my $fh, '<', $file or die "Can't open $file: $!\n";
my @lines = <$fh>;
close $fh;

# Parse the Twee file
my %passages;
my $current_passage;
my $choice_count = 1;
for my $line (@lines) {
    if ($line =~ /^:: (.+)$/) {
        $current_passage = $1;
        $passages{$current_passage} = { description => '', choices => [] };
        $choice_count = 1;
    } elsif ($line =~ /\[(.+?)\]/) {
        my $link = $1;
        my ($display_text, $passage_link) = $link =~ /\|/ ? split(/\|/, $link) :
                                             $link =~ /->/ ? split(/->/, $link) : ($link, $link);
        push @{$passages{$current_passage}->{choices}}, [$choice_count++, $display_text, $passage_link];
    } else {
        $passages{$current_passage}->{description} .= $line;
    }
}

# Randomize passage numbers if bookNums is true
my %randomized_numbers;
if ($bookNums) {
    my $num_passages = keys %passages;
    my $randomized_output = `./randBookNum.pl $num_passages`;
    chomp $randomized_output;
    my @shuffled_numbers = split /,/, $randomized_output;
    my $i = 0;
    for my $passage (keys %passages) {
        $randomized_numbers{$passage} = $shuffled_numbers[$i++];
    }
}

# Play the game
my $passage = 'Start';
while (1) {
    if ($show_passage_name) {
        print ":: $passage\n";
    }
    print $passages{$passage}->{description} . "\n";
    
    my @choices_display;
    for my $choice (@{$passages{$passage}->{choices}}) {
        my $choice_number = $choice->[0];
        if ($bookNums) {
            $choice_number = $randomized_numbers{$choice->[2] =~ /\|(.+)/ ? $1 : $choice->[2] =~ /->(.+)/ ? $1 : $choice->[2]};
        }
        push @choices_display, "$choice_number. $choice->[1]";
    }
    print join("\n", @choices_display) . "\n";
    
    print "Enter choice: ";
    my $choice = <STDIN>;
    chomp $choice;
    my $found = 0;
    for my $link (@{$passages{$passage}->{choices}}) {
        my $choice_number = $link->[0];
        if ($bookNums) {
            $choice_number = $randomized_numbers{$link->[2] =~ /\|(.+)/ ? $1 : $link->[2] =~ /->(.+)/ ? $1 : $link->[2]};
        }
        if ($choice_number == $choice) {
            $passage = $link->[2] =~ /\|(.+)/ ? $1 : $link->[2] =~ /->(.+)/ ? $1 : $link->[2];
            $found = 1;
            last;
        }
    }
    unless ($found) {
        print "Invalid choice. Try again.\n";
    }
}
