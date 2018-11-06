# transcript_id_to_gene_type_mapping
The ENCODE RNA-SEQ-PIPELINE includes a QC step that counts reads by gene type. This step requires parsing transcript_id <-> gene_type mapping. Purpose of this repo is to document the process of creating that mapping. The code will be included as a jupyter notebook. The annotation files will be included in the repo in folder `annotations_and_spikeins`. Separate mappings as `.tsv` files are in folder `mappings`. The mappings will be created for [human annotation version hg19](https://www.encodeproject.org/files/gencode.v19.annotation/), [human annotation v24](https://www.encodeproject.org/files/ENCFF824ZKD/) and [mouse annotation version mm10 a.k.a GRCm38.p4 M7](https://www.encodeproject.org/files/gencode.vM7.annotation/) matching tRNAs downloaded from [gencode](https://www.gencodegenes.org) will be included. Additionally, spikein files from [ENCFF001RTP](https://www.encodeproject.org/files/ENCFF001RTP/) and from [ENCFF335FFV](https://www.encodeproject.org/files/ENCFF335FFV/) will be used. For `hg19` and `mm10` the merging is done using the `merge_annotation.py` python script with following command lines run in the `annotations_and_spikeins` folder using `python 3.4.3`: 

```bash
min-tb:annotations_and_spikeins otto$ python3 ../merge_annotation.py --annotation gencode.v19.annotation.gtf.gz --tRNA gencode.v19.tRNAs.gtf.gz --spikeins ENCFF001RTP_spikes_ENCFF335FFV_spikes.fasta.gz --output_filename gencode.v19.trna.ercc.phix.gtf.gz
```

```bash
min-tb:annotations_and_spikeins otto$ python3 ../merge_annotation.py --annotation gencode.vM7.annotation.gtf.gz --tRNA gencode.vM7.tRNAs.gtf.gz --spikeins ENCFF001RTP_spikes_ENCFF335FFV_spikes.fasta.gz --output_filename gencode.vM7.trna.ercc.phix.gtf.gz
```

Subsequently the transcript id and gene type are extracted from the file resulting from the merge_annotation.py step by running the accompanied python script `build_transcript_id_to_gene_type_tsv.py`. For [human GRCh38](https://www.encodeproject.org/files/ENCFF824ZKD/) the file where annotation, tRNAs and spikeins are contained is downloaded from the ENCODE portal and used directly in this step. Example command line looks like this:

```bash
min-tb:github otto$ python3 build_transcript_id_to_gene_type_tsv.py --input_annotation annotations_and_spikeins/gencode.vM7.trna.ercc.phix.gtf.gz --output_tsv gencode.vM7.trna.ercc.phix.transcript_id_to_genes.tsv
``` 

# rRNA and Mt_rRNA removal

Within `annotations_and_spikeins` folder are also annotation files (with spikeins), from which all rRNA annotations are removed, and files from which rRNA, excluding Mt_rRNA annotations are removed. This was done by using unix shell commands in the following way:

## Remove all rRNA.

As an example, the shell command to remove all rRNA annotations from `ENCFF824ZKD_gencodeV24pri-tRNAs-ERCC-phiX.gtf.gz`

```bash
min-tb:annotations_and_spikeins otto$ gzip -cd ENCFF824ZKD_gencodeV24pri-tRNAs-ERCC-phiX.gtf.gz | grep -v rRNA | gzip -n > ENCFF824ZKD_gencodeV24pri-tRNAs-ERCC-phiX-minus-rRNA-and-Mt-rRNA.gtf.gz
```

## Remove rRNA , leave Mt_rRNA in.

As an example, the shell command to remove rRNA annotations, leaving Mt_rRNA annotations untouched from gencode.vM7.trna.ercc.phix.gtf.gz.

```bash
min-tb:annotations_and_spikeins otto$ gzip -cd gencode.vM7.trna.ercc.phix.gtf.gz | grep -v \"rRNA | gzip -n > gencode.vM7.trna.ercc.phix.minus.rRNA.gtf.gz 
```
