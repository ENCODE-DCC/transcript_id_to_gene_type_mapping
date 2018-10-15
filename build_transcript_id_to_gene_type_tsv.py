"""
Take output from merge_annotation.py and then use that to
build a .tsv file that consists of pairs
Transcript ID <TAB> corresponding gene type
"""

__author__ = 'Otto Jolanki'
__version__ = '0.1'
__license__ = 'MIT'

import argparse
import gzip


def parse_anno_line(line):
    line_list = line.split()
    # some mouse annotation lines don't have transcript_id
    # we want to just skip those
    try:
        transcript_id = line_list[line_list.index('transcript_id') +
                                  1].lstrip('"').rstrip(';"')
    except ValueError:
        return {}
    try:
        gene_type = line_list[line_list.index('gene_type') +
                              1].lstrip('"').rstrip(';"')
    except ValueError:
        gene_type = 'spikein'
    return {transcript_id: gene_type}


def build_transcriptID_to_gene_type_dict(path_to_gz):
    transcript_id_to_gene_type = {}
    with gzip.open(path_to_gz, 'rb') as f:
        for line in f:
            transcript_id_to_gene_type.update(parse_anno_line(line.decode()))
    return transcript_id_to_gene_type


def write_dict_to_tsv(source_dict, filepath):
    with open(filepath, 'w') as f:
        for key, value in sorted(source_dict.items()):
            line = '{key}\t{value}\n'.format(key=key, value=value)
            f.write(line)


def main(args):
    transcript_id_to_gene_type_dict = build_transcriptID_to_gene_type_dict(
        args.input_annotation)
    write_dict_to_tsv(transcript_id_to_gene_type_dict, args.output_tsv)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_annotation')
    parser.add_argument('--output_tsv')
    args = parser.parse_args()
    main(args)
