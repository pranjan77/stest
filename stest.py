
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




def get_alignment_stat(read):
	if (read.cigarstring):
		return str(read.reference_name) + ":" + str(read.reference_start) + "-" + str(read.reference_end)
	else:
		return "noalignment"

def append_to_list(read,readlist):
	alignment_stat = get_alignment_stat(read)
	if readlist.has_key(read.query_name):
		readlist[read.query_name].append(alignment_stat)
	else:
		listx=[alignment_stat]
		readlist[read.query_name]=listx


	return readlist

def find_split_alignment_chimeras(bam):
	#bam="xm.bam"
	readlist=dict()
	fh_in = pysam.Samfile(bam)
	for (num_reads, read) in enumerate(fh_in):
		#if (read.cigarstring):
		#	rs = str(get_alignment_stat(read))
		#	print read.query_name +" " + str(read.query_alignment_start) + " " + str(read.query_alignment_end) + " " + rs
		#print read.query_name + " " + str(read_status(read)) + " " + str(sa_tags(read))
		append_to_list(read,readlist)

	for ids in readlist.keys():
		locations = " ".join(readlist[ids])
		print "\t".join([ids,locations])




def main():
    """main
    """
    find_split_alignment_chimeras("aln-bwamem.bam")


if __name__ == "__main__":
	main()
