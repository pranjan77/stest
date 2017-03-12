
import sys
import os
#import gzip
import argparse
import regex

import pysam

from cigar import Cigar



def find_split_alignment_chimeras(bam):
	bam="xm.bam"
	fh_in = pysam.Samfile(bam)
	for (num_reads, read) in enumerate(fh_in):
		print read.query_name + " " + read.is_unmapped



def main():
    """main
    """
    find_split_alignment_chimeras("bam")


if __name__ == "__main__":
	main()
