"""
winning_driver.py
Author: James Richter
Class: CS 499, Twitchell/Burton
Last Updated: 1/6/2016

Module that acts as the driver for both the Breakout
game and the winning genome of the Breakout game.  It
could be implemented in driver.py but I like it better
like this, since I can make a separate executable file
for the training program and the program that displays
the winning genome.
"""

import breakout
import genome
import species

import itertools
import population
import time
import os.path

def runBreakout(breakout):
   current_genome = genome.Genome(3, 2, 0, 0)
   try:
      current_genome.load("./winning_genome")
   except:
      print "Unable to find file named \"winning_genome\".  ", \
             "Run the genetic algorithm to generate the file."
      exit(0)
   current_genome.generateNetwork()

   for item in breakout.run():
      # plug in the game outputs into the neural network
      try:
         game_coords = [x for x in item]
         inputs = current_genome.activateNetwork(game_coords)
         inputs = [i for _,i in inputs.items()]
         breakout.inputs = inputs
      # start a new game
      except:
         pass
      if breakout.done == True:
         break

brkout = breakout.Bricka()

runBreakout(brkout)