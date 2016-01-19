"""
species.py
Author: James Richter
Class: CS 499, Twitchell/Burton
Last Updated: 1/6/2016

A collection of similar genomes.  This module contains functions for
mating two genomes, mating the entire species, eliminating the worst
performers of the species, and checking to see if the species is stale.

Speciation is crucial because, if a genome performs at a local maxima 
of fitness performance, a population could get stuck at that maxima.
For example, in Breakout, a genome could get 941 points from simply 
launching the ball and never moving the paddle. This is a suboptimal 
strategy, but it could dominate a population if there are no separation
of species.  Using speciation, it only dominates one species, a small
subset of the population.  In a nutshell, it protects innovation in
other species that are onto a good idea, but haven't quite made it yet.
"""

from genome import Genome

import random
import math

INPUTS = 3
OUTPUTS = 2

# number of attempts the species gets, without improving, 
# before it becomes stale
STALENESS_THRESHOLD  = 2

# chance that a child gene will inherit from the more fit parent
GENE_DOMINANCE = 0.79

# chance that a stale species will have a single survivor
SOLE_SURVIVOR_CHANCE = 0.2

def inverseExp(x):
   """The inverse exponent function."""
   return 1/(7*math.exp(x))

class Species:
   """
   A group of genetically similar genomes.  Contains
   functions for adding and mating genomes, as well as
   calculating the average fitness for the species.
   """
   def __init__(self, name):
      """Initialize an empty species."""
      self.genomes = {}     
      self.average_fitness = 0
      self.name = name
      self.staleness = 0
      
      self.generateGenome()

   def __repr__(self):
      string = ""
      for i,genome in self.genomes.items():
         string += str(i) + ": " + str(genome) + '\t'
      return string
   
   def addGenome(self, genome1):
      """
      Add a genome to our species.
      
      Args:
         genome1: the genome added to the species.
      """
      max_genome = 0
      if self.genomes:
         max_genome = max(self.genomes) + 1
      self.genomes[max_genome] = genome1

   def mateGenomes(self, num_children):
      """
      Mate all of the genomes in the species.
      
      Args:
         num_children: the number of children in the next iteration
         of the species.
      """
      new_gen = {}
      
      if self.genomes.__len__() >= 5:
         mostFit = sorted(self.genomes.items(), key=lambda x: x[1].fitness)
         mostFit = [y for y in reversed([x[1] for x in mostFit])]
         #mostFit is now a list of genomes in order of fitness
         for i in range(num_children):
            g3 = False
            #find the chance of adding a stud
            for j in range(5):
               if random.random() < inverseExp(j):
                  g1 = mostFit[j]
                  g2 = random.sample(mostFit, 1)[0]
                  g3 = self.mate(g1, g2)
                  new_gen[i] = g3
                  break
            if not g3:
               g1, g2 = random.sample(mostFit, 2)
               g3 = self.mate(g1, g2)
               new_gen[i] = g3
         
      elif self.genomes.__len__() >= 2:
         genomes_list = set([j for j in self.genomes])
         for i in range(num_children):
            g1, g2 = random.sample(genomes_list, 2)
            g3 = self.mate(self.genomes[g1], self.genomes[g2])
            new_gen[i] = g3
      else:
         for i in range(num_children):
            g3 = self.mate(self.genomes[max(self.genomes)],
                           self.genomes[max(self.genomes)])
            new_gen[i] = g3
      
      self.genomes = new_gen
   
   def checkForStaleness(self):
      """
      Check to see if the species has gone STALENESS_THRESHOLD generations
      without gaining fitness.
      """
      if not self.genomes:
         return
      if self.staleness > STALENESS_THRESHOLD:
         print "Species", self.name, " has gone STALE."
         numberOfGenomes = self.genomes.__len__()
         mostFit = sorted(self.genomes.items(), key=lambda x: x[1].fitness)
         bestGenome = mostFit[-1][1]
         self.__init__(self.name)
         if random.random() < SOLE_SURVIVOR_CHANCE:
            self.genomes[0] = bestGenome
            for i in range(1,numberOfGenomes):
               self.generateGenome()
         else:
            for i in range(0,numberOfGenomes):
               self.generateGenome()
        
   def generateGenome(self):
      """Create a partially connected genome and add it to our species."""
      max_genome = 0
      if self.genomes:
         max_genome = max(self.genomes) + 1
      genome = Genome(INPUTS,OUTPUTS,self.name,max_genome)
      for node1 in genome.nodes:
         genome.mutateAddConnection()
      self.genomes[max_genome] = genome
      
   def mate(self, genome1, genome2):
      """
      Mate two genomes based on their fitness.

      Args:
         genome1: the first parent genome
         genome2: the second parent genome

      Returns:
         genome3: the resultant child genome
      """
      # we want genome1 to be the most fit
      if genome2.fitness > genome1.fitness:
         tempGenome = genome1
         genome1 = genome2
         genome2 = tempGenome
      assert genome1.fitness >= genome2.fitness  
      genome3 = Genome(INPUTS, OUTPUTS, self.name, None)
      
      possible_genes = set(genome1.genes) | set(genome2.genes)
      for innov in possible_genes:
         if random.random() < GENE_DOMINANCE:
            if innov in genome1.genes:
               genome3.genes[innov] = genome1.genes[innov]
         else:
            if innov in genome2.genes:
               genome3.genes[innov] = genome2.genes[innov]
      
      # creating the nodes
      genome3.generateNodes()
      genome3.mutate()
      
      return genome3
   
   def getRandomGenome(self):
      """Return a random genome from the species."""
      return random.choice(self.genomes.items())[1]
   
   def calculateAverageFitness(self):
      """
      Calculate the average fitness for the species, and also
      update the staleness counter.
      """
      old_average_fitness = self.average_fitness
      self.average_fitness = 0
      for i, genome in self.genomes.items():
         self.average_fitness += float(genome.fitness) / self.genomes.__len__()
      if self.average_fitness <= old_average_fitness:
         self.staleness += 1

   def eliminateLowestPerformers(self):
      """
      Eliminate the lowest half of performers in the species.
      """
      # sort self.genomes by fitness
      genome_performance = sorted(self.genomes.items(),
                                  key = lambda x: x[1].fitness)
      number_removed = genome_performance.__len__() / 2
      for i in range(number_removed):
         del(self.genomes[genome_performance[i][0]])
      
