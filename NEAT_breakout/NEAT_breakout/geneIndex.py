"""
geneIndex.py
Author: James Richter
Class: CS 499, Twitchell/Burton
Last Updated: 1/6/2016

An index of genes.  Whenever a new gene is created, it looks at the
gene_index to see if a gene exists that connects the same two nodes.
If there is, it uses that index number.  This makes checking the delta
distance between genomes possible, since they will have genes with
matching gene_index lookup values.
"""
import gene

gene_index = {}