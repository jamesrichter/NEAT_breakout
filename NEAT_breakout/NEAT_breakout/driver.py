"""
driver.py
Author: James Richter
Class: CS 499, Twitchell/Burton
Last Updated: 1/6/2016

Module that acts as the driver for both the Breakout
game and the NEAT system that hooks up to it.
"""

import breakout
import genome
import species
import population

import itertools
import time
import os.path

def runBreakout(pool, brkout):
   """
   Run the Breakout game.

   Args:
      pool: a pool of species that contains all of our genomes and NEAT logic
      breakout: an instance of the game breakout
   """

   start_time = time.time()
   genomes_list = []
   for _,species in pool.species.items():
      for i,genome1 in species.genomes.items():
         genomes_list.append(genome1)
   current_genome = 0

   print "Generation:", pool.generation
   genomes_list[0].generateNetwork()

   # run the breakout game
   for item in brkout.run():
      # plug in the game outputs into the neural network
      try:
         game_coords = [x for x in item]
         inputs = genomes_list[current_genome].activateNetwork(game_coords)
         inputs = [i for _,i in inputs.items()]
         brkout.inputs = inputs
      # start a new game
      except:
         if item == None and brkout.state == breakout.STATE_WON:
            genomes_list[current_genome].save("winning_genome")
         genomes_list[current_genome].fitness = item
         print "Species ", genomes_list[current_genome].species, ":", \
               "Genome " , current_genome, ":", \
               "Fitness ", item
         current_genome += 1
         # move to the next genome
         if current_genome < genomes_list.__len__():
            genomes_list[current_genome].generateNetwork()
         # get a new generation
         else:
            current_genome = 0
            pool.nextGeneration()
            print "Generation", pool.generation - 1, \
               "had an average fitness of", pool.total_average_fitness
            print "Generation:", pool.generation
            genomes_list = []
            for _,species in pool.species.items():
               for i,genome1 in species.genomes.items():
                  genomes_list.append(genome1)
            current_genome = 0
            genomes_list[current_genome].generateNetwork()
         brkout.score = 0

pool = population.Population()
brkout = breakout.Bricka()

runBreakout(pool, brkout)