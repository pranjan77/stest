
import sys
import os
#import gzip
import argparse
import regex

import pysam

from cigar import Cigar

def read_status(read):
	if read.is_unmapped:
		return "unmapped"
	if read.is_duplicate:
		return "duplicate"
	if read.is_qcfail:
		return "qcfail"
	return "unknown"


def find_split_alignment_chimeras(bam):
	bam="xm.bam"
	fh_in = pysam.Samfile(bam)
	for (num_reads, read) in enumerate(fh_in):
		print read.query_name + " " + str(read_status(read))



def main():
    """main
    """
    find_split_alignment_chimeras("bam")


if __name__ == "__main__":
	main()
