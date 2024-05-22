#!/usr/bin/perl

use strict;
use warnings;

# Read the markdown file
my $file = $ARGV[0] or die "Usage: $0 <file.md>\n";
open my $fh, '<', $file or die "Can't open $file: $!\n";
my @lines = <$fh>;
close $fh;

# Run randBookNum.pl to get randomized numbers
my $numPass = 0;
foreach my $line (@lines) {
    $numPass++ if $line =~ /^## /;
}
my $bookNums_str = `./randBookNum.pl $numPass`;
chomp $bookNums_str;
my @bookNums = split /,/, $bookNums_str;

# Re-order passages according to BookNums
my @passages;
my $current_passage = '';
my $passage_text = '';
foreach my $line (@lines) {
    if ($line =~ /^## /) {
        push @passages, { header => $current_passage, text => $passage_text } if $current_passage;
        $current_passage = $line;
        $passage_text = '';
    } else {
        $passage_text .= $line;
    }
}
push @passages, { header => $current_passage, text => $passage_text };

# Output re-ordered passages
my $output_file = $file =~ s/\.md$/.sort.md/r;
open my $out_fh, '>', $output_file or die "Can't create output file: $!\n";
foreach my $num (@bookNums) {
    my $passage = $passages[$num - 1]->{header};
    my $text = $passages[$num - 1]->{text};
    print $out_fh "$passage$text";
}
close $out_fh;

print "Re-ordered markdown file created: $output_file\n";
