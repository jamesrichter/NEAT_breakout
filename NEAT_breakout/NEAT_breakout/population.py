"""
population.py
Author: James Richter
Class: CS 499, Twitchell/Burton
Last Updated: 1/6/2016

A generation-level view of different species of genomes.

This module controls most of the important genetic algorithm
functions such as separating the genomes into species, allocating
how many genomes a species will get next generation, and 
calculating the delta distance between two genomes.
"""

import species
from geneIndex import gene_index

import random

# the amount of influence the weight differences and gene differences
# between genomes affect their inclusion in the same species.  Should be 
# numbers from 0 to 1, and should sum to 1.
DISJOINT_GENE = 0.95
DISJOINT_WEIGHT = 1 - DISJOINT_GENE

# the highest amount of difference that two genomes can have to be
# in the same species
DISJOINT_THRESHOLD = 0.5

GENERATION_SIZE = 200

# the maximum portion of the population that can be taken by any one species
MAX_PORTION = 0.2

# DT and GS trials
# .6 and 700: 7591s (started with a 4000 in gen0)
# .5 and 200: 253s, 5112s, 11730s, quit (~12h), 4972s, quit, quit,
# 

class Population():
   """
   Overarching class that keeps track of all of the species in our experiment.
   Basically, the gene pool that contains all species of life.
   """
   def __init__(self):
      self.species = {}
      self.generation = 0
      self.total_average_fitness = 0
      self.newGeneration()
      
   def newGeneration(self):
      """Make GENERATION_SIZE species with one genome each."""
      for i in range(GENERATION_SIZE):
         self.species[i] = species.Species(i)
         
   def nextGeneration(self):
      """Create the next generation through breeding."""
      self.sortTheGenomesIntoSpecies()
      self.removeLowestPerformers()
      self.allocateSpecies()
      self.pruneStaleSpecies()
      self.generation += 1
      
   def pruneStaleSpecies(self):
      """
      Check to see if a species has been dominating for too long
      without improving.
      """
      for i in self.species:
         self.species[i].checkForStaleness()
   
   def removeLowestPerformers(self):
      """Remove the lowest performers of a species."""
      for i in self.species:
         self.species[i].eliminateLowestPerformers()
   
   def sortTheGenomesIntoSpecies(self):
      """
      Sort the genomes according to what species they belong to.
      This is done in place.
      """
      # get the representative genome for each species
      representative_genomes = {}
      temp_genomes = []
      for i, specie in self.species.items():
         if specie.genomes:
            for j, genome in specie.genomes.items():
               temp_genomes.append(genome)
            representative_genomes[i] = specie.getRandomGenome()
            # take out the genomes from the original species.
            specie.genomes = {}
         else:
            pass
      
      
      # look at all genomes in all species and put them into new species
      for genome in temp_genomes:
         found = False
         # does the genome match one of the representative species
         for k, rep_genome in representative_genomes.items():
            if deltaGenome(genome, rep_genome) < DISJOINT_THRESHOLD:
               self.species[k].addGenome(genome)
               found = True
               break
         # if not, make a new species for it 
         if found == False:
            l = 0
            while l in representative_genomes:
               l += 1
            self.species[l] = species.Species(l)
            self.species[l].genomes[0] = genome
            representative_genomes[l] = genome
      
      # clean out the empty species
      for i, specie in self.species.items():
         if not specie.genomes:
            del self.species[i]
   
   def allocateSpecies(self):
      """
      Allocate the amount of population each species gets for the next 
      generation.
      Since the number of "organisms" is limited by GENERATION_SIZE, it
      is a very competitive world.
      """
      allocation_amount = {} # {species: allocation amount}
      average_fitnesses = {}
      total_average_fitness = 0
      for i, specie in self.species.items():
         specie.calculateAverageFitness()
         if specie.average_fitness > 0:
            average_fitnesses[i] = specie.average_fitness
            total_average_fitness += specie.average_fitness
         else:
            average_fitnesses[i] = 1
            total_average_fitness += 1
      self.total_average_fitness = \
         total_average_fitness / self.species.__len__()

      # discover how many genomes we can allocate to each species
      total_allocated = 0
      for specie, average_fitness in average_fitnesses.items():
         portion = float(average_fitness) / total_average_fitness
         if portion > MAX_PORTION:
            portion = MAX_PORTION
         allocation_amount[specie] = int(round(portion * GENERATION_SIZE))
         total_allocated += allocation_amount[specie]
      
      # due to rounding, we sometimes try to allocate more or less
      # than is available.  GENERATION_SIZE is the proper amount.
      while total_allocated != GENERATION_SIZE:
         if total_allocated < GENERATION_SIZE:
            allocation_amount[random.sample(set(allocation_amount), 1)[0]] += 1
            total_allocated += 1
         else:
            allocation_amount[random.sample(set(allocation_amount), 1)[0]] -= 1
            total_allocated -= 1
      
      assert(total_allocated == GENERATION_SIZE)
      for specie, allocated in allocation_amount.items():
         self.species[specie].mateGenomes(allocated)
         
def deltaGenome(genome1, genome2):
   """
   Determine the delta, or the genetic difference between two genomes.
   
   Args:
      genome1: the first genome
      genome2: the second genome

   Returns:
      delta: the difference between genomes
   """
   set1 = set(genome1.genes)
   set2 = set(genome2.genes)
   disjoint_set = set1 ^ set2
   larger_genome_length = max(set1.__len__(), set2.__len__())
   if larger_genome_length == 0:
      return 0
   
   number_disjoint_genes = disjoint_set.__len__()
   
   delta_topology = DISJOINT_GENE * number_disjoint_genes/larger_genome_length
   
   matching_set = set1 & set2
   if matching_set.__len__() == 0:
      return 9
   
   weight_difference = 0
   for i in matching_set:
      weight1 = genome1.genes[i].weight
      weight2 = genome2.genes[i].weight
      weight_difference += abs(weight1 - weight2)
   delta_weight = DISJOINT_WEIGHT * weight_difference / matching_set.__len__()
   
   delta = delta_topology + delta_weight
   return delta