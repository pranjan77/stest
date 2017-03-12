
import sys
import os
#import gzip
import argparse
import regex

import pysam

from cigar import Cigar

def read_is_primary(read):
	"""see sam spec: For each read/contig in a SAM file, it is required
	that one and only one line associated with the read satisfies
	'FLAG & 0x900 == 0'. This line is called the primary line of the read.
	"""
	return bool(read.flag & 0x900 == 0)

def sa_tags(read):
	tags = dict(read.tags)
	x=tags.has_key('SA')
	if (x==True):
		return "SA"
	else:
		return "NOSA"


def read_status(read):
	if read.is_unmapped:
		return "unmapped"
	if read.is_duplicate:
		return "duplicate"
	if read.is_qcfail:
		return "qcfail"
	if read_is_primary(read):
		return "primary"
	if read_is_primary(read):
		return "primary"

	return "other"

def append_to_list(read,readlist):
	if readlist.has_key(read.query_name):
		readlist[read.query_name].append(read)
	else:
		listx=[read]
		readlist[read.query_name]=listx


	return readlist

def find_split_alignment_chimeras(bam):
	bam="xm.bam"
	readlist=dict()
	fh_in = pysam.Samfile(bam)
	for (num_reads, read) in enumerate(fh_in):
		#print read.query_name + " " + str(read_status(read)) + " " + str(sa_tags(read))
		append_to_list(read,readlist)

	for ids in readlist.keys():
		split_alignments = readlist[ids]

		for readx in split_alignments:
			print ids + " " + str(read_is_primary(readx)) + " " +  str(readx.reference_start) + " " + str(readx.reference_end)


def main():
    """main
    """
    find_split_alignment_chimeras("bam")


if __name__ == "__main__":
	main()
