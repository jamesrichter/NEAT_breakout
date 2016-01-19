"""
gene.py
Author: James Richter
Class: CS 499, Twitchell/Burton
Last Updated: 1/6/2016

Not much to it.  A genome is made up of genes.
The genome can be built solely from its inputs, 
its outputs, and its genes.
"""

class Gene:
   """
   A simple part of an individual genome.  A genome is 
   made up of many genes.
   """
   def __init__(self):
      """Initialize a blank gene."""
      self.source_neuron = 0
      self.target_neuron = 0
      self.weight = 0.0
      self.enabled = True

   def copy(self, gene1):
      """Gene copy constructor."""
      self.source_neuron = gene1.source_neuron
      self.target_neuron = gene1.target_neuron
      self.weight = gene1.weight
      self.enabled = gene1.enabled
      #self.innovation_number = gene1.innovation_number
      
   def __repr__(self):
      return str(self.source_neuron) + '\\' + \
         str(self.target_neuron) + '\\' + \
         str(self.weight) + '\\' + \
         str(self.enabled) + '\\' #+ \
         #str(self.innovation_number)