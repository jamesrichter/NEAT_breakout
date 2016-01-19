"""
genome.py
Author: James Richter
Class: CS 499, Twitchell/Burton
Last Updated: 1/7/2016

The genome module is the "meat and potatoes" of the NEAT system.
It represents an the genetic information of an individual of the 
population.  Its genetic information can be used to build a neural 
network to perform that individual's actions.  

This module also provides some basic mutations that can be performed
on a genome, including mutation of one weight, mutation of all of the
weights, adding a genome, or adding a node.
"""

from network import Network
from network import MAX_LAYER
from gene import Gene
from geneIndex import gene_index

import copy
import pickle
import random

ADD_CONNECTION_CHANCE = 0.45
ADD_NEURON_CHANCE = 0.05
ONE_WEIGHT_CHANCE = 0.5
ALL_WEIGHT_CHANCE = 0.1

class Genome:
   """
   The genetic information for one individual of a species.  This
   genetic information can be saved and reloaded later, it can be
   activated to see how it performs, or it can be mutated.
   """
   def __init__(self, num_inputs, num_outputs, species, name):
      """
      Initializes the Genome class.  Adds input, output, and bias nodes
      to the list of nodes.

      Species and name are usually integers.

      Args:
         num_inputs: the number of inputs to the neural network.
         num_outputs: the number of outputs from the neural network.
         species: the name of the species to which this genome belongs.
         name: the name of this genome.
      """
      self.genes = {}  # {innovation_number, Gene}
      self.nodes = set()
      self.num_inputs = num_inputs
      self.num_outputs = num_outputs
      self.network = None
      self.fitness = 0
      self.species = species
      self.name = name

      # add the inputs to the node set
      for i in range(num_inputs):
         self.nodes.add(-1 - i)
      
      # add the outputs to the node set
      for i in range(num_outputs):
         self.nodes.add(i + MAX_LAYER + 1)
         
      # add the bias to the node set
      self.nodes.add(0)

   def copy(self, genome1):
      """Copy constructor for the Genome class"""
      self.genes = copy.deepcopy(genome1.genes)
      self.num_inputs = genome1.num_inputs
      self.num_outputs = genome1.num_outputs
      self.nodes = genome1.nodes.copy()
      self.fitness = genome1.fitness
      self.species = genome1.species
      self.name = genome1.name
      self.generateNetwork()

   def __repr__(self):
      genomeString = ''
      for _,gene in self.genes.items():
         genomeString += str(gene)
         genomeString += '\n'
      genomeString += '\nNodes: ' + str(sorted(self.nodes))
      return genomeString
      
   def generateNetwork(self):
      """
      Generate the neural network from the genes.
      This is necessary for activateNetwork().
      """
      self.network = Network()
      self.network.num_inputs = self.num_inputs
      self.network.num_outputs = self.num_outputs
      self.network.generateNetwork(self.genes, self.nodes)
   
   def generateNodes(self):
      """ Create a list of nodes from self.genes"""
      for _,gene in self.genes.items():
         if gene.source_neuron not in self.nodes:
            self.nodes.add(gene.source_neuron)
         if gene.target_neuron not in self.nodes:
            self.nodes.add(gene.target_neuron)
   
   def activateNetwork(self, inputs):
      """
      Get the output from our neural network.

      Args:
         inputs: the input to the neural network in a list.
      
      Returns:
         outputs: the outputs from the neural network in a list.
      """
      if self.network == None:
         self.generateNetwork()
      outputs = self.network.activateNetwork(inputs)
      return outputs

   def save(self, string1):
      """Save the genome to the filename indicated by string1."""
      pickle.dump(self, open(string1, "wb"))

   def load(self, string1):
      """Load the genome from the filename indicated by string1."""
      self.copy(pickle.load(open(string1, "rb" )))
   
   def mutate(self):
      """
      Randomly mutate the genome in place.  Note that two different
      mutations are possible, but the same mutation cannot be performed
      twice.
      """
      if random.random() < ADD_CONNECTION_CHANCE:
         self.mutateAddConnection()
      if random.random() < ADD_NEURON_CHANCE:
         self.mutateAddNeuron()
      if random.random() < ONE_WEIGHT_CHANCE:
         self.mutateOneWeight()
      if random.random() < ALL_WEIGHT_CHANCE:
         self.mutateAllWeights()
         
   def mutateAddConnection(self):
      """Add a connection between two random, valid nodes."""
      # get some random nodes
      node1, node2 = sorted(random.sample(self.nodes, 2))
      
      # make sure we didn't get 2 inputs or 2 outputs
      while node1 > MAX_LAYER or node2 <= 0:
         node1, node2 = sorted(random.sample(self.nodes, 2))
      
      # make sure we didn't get 2 nodes that are already connected
      for inno, gene in self.genes.items():
         if gene.source_neuron == node1 and gene.target_neuron == node2:
            gene.enabled = True
            return
      
      self.addGene(node1, node2)

   def addGene(self, node1, node2):
      """
      Add a randomly weighted gene between two nodes.
      
      Args:
         node1: the first node
         node2: the second node
      """
      # connect the two valid, unconnected nodes
      g = Gene()
      g.source_neuron = node1
      g.target_neuron = node2
      g.weight = random.random() * 4 - 2
      #check to see if the gene already exists in the index
      for index,gene in gene_index.items():
         if gene.source_neuron == node1 and gene.target_neuron == node2:
            # if found, use that same innovation number
            self.genes[index] = g
            return
      
      #if it's not in the index, add it and record in the index
      if gene_index:
         self.genes[max(gene_index) + 1] = g
         gene_index[max(gene_index) + 1] = g
      else:
         gene_index[0] = g
         self.genes[0] = g
         
   def mutateAddNeuron(self):
      """
      Add a neuron at the location of a random gene.
      This is done by disabling the original gene, 
      then adding a new node and connections between
      the new node and the original gene nodes.
      """
      # get one random gene
      if self.genes:
         innov = random.sample(self.genes, 1)[0]
      else:
         return
      gene = self.genes[innov]
      
      node1 = gene.source_neuron
      node2 = gene.target_neuron
      # make sure our nodes aren't two consecutive integers
      if node1 + 1 > node2 - 1:
         return
      
      g = Gene()
      g.copy(gene)

      # create a new node
      node = random.randint(node1 + 1, node2 - 1)
      
      # make sure our node isn't the same as any existing nodes
      if node in self.nodes:
         return
      # should be a hidden node
      assert node >= 1 and node <= MAX_LAYER
      
      # morph the gene into two genes and add the node
      g1 = Gene()
      g1.source_neuron = node1
      g1.target_neuron = node
      g1.weight = 1
      g2 = Gene()
      g2.source_neuron = node
      g2.target_neuron = node2
      g2.weight = gene.weight
      self.nodes.add(node)
      
      # disable the original gene, replace it with the new ones
      g.enabled = False
      self.genes[innov] = g
      self.genes[max(gene_index) + 1] = g1
      self.genes[max(gene_index) + 2] = g2
      
      #add the new genes to the index
      gene_index[max(gene_index) + 1] = g1
      gene_index[max(gene_index) + 1] = g2
      

   def mutateOneWeight(self):
      """Find a random gene, and alter its weight a little."""
      if self.genes:
         innov = random.sample(self.genes, 1)[0]
      else:
         return
      v = random.random()
      g = Gene()
      g.copy(self.genes[innov])
      g.weight += v * .2 - .1
      self.genes[innov] = g

         
   def mutateAllWeights(self):
      """Find all genes, and alter their weights a little."""
      g = Gene()
      for innov in self.genes:
         g.copy(self.genes[innov])
         g.weight += random.random() * .2 - 1
         self.genes[innov] = g
