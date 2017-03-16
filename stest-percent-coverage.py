
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


def get_readlengths(read, readlengths):
	readlengths[read.query_name] = read.inferred_length


def get_alignment_stat(read):
	if (read.cigarstring):
		return   str(read.query_alignment_start) + "-" + str(read.query_alignment_end)
	else:
		return "noalignment"

def find_percent_coverage(locations):
	coverage=set()
	print locations
	for line in locations:
		try:
			v1, v2 = line.strip().split("-")
			print str(v1) + " " + str(v2)
			#if (int(v1)==0):
			#	v1=1
			#if int(v2)==0:
			#	v2=1
			v1_min, v_max = sort([int(v1), int(v2)])
			print "#" + str(v1_min)

		except:
			print "#" + str(123)

			continue
		coverage.update(range(v_min, v_max+1))
		print coverage
	coveragelength = len(coverage)
	if (coveragelength > 100):
		coveragelength = 100

	return coveragelength





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
	readlengths=dict()
	fh_in = pysam.Samfile(bam)
	for (num_reads, read) in enumerate(fh_in):
		get_readlengths(read,readlengths)
		if (read.cigarstring):
			rs = str(get_alignment_stat(read))
			#print read.query_length +" " + str(read.query_alignment_end) + " " + str(read.query_alignment_start) + " " + rs
		#print read.query_name + " " + str(read_status(read)) + " " + str(sa_tags(read))
			append_to_list(read,readlist)

	for ids in readlist.keys():

		readlength = readlengths[ids]
		length1 = readlength -1
		length2 = readlength
		maxlength= str(length1) + "-" + str(length2)
		newlocations = readlist[ids]
		newlocations.append(maxlength)

		coverage = find_percent_coverage(newlocations)
		locations = " ".join(readlist[ids])
		print ids + "\t" +  str(readlength) + "\t" + str(coverage) + "\t"  + " ".join([locations]) 




def main():
    """main
    """
    find_split_alignment_chimeras("aln-bwamem.bam")


if __name__ == "__main__":
	main()
