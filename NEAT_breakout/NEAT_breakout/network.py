"""
network.py
Author: James Richter
Class: CS 499, Twitchell/Burton
Last Updated: 1/6/2016

A module representing an individual of the population.
The neural network is the "brain" of the individual, and
from it our individual has all it needs to know how to
perform a task to the best of its ability.  However, its 
outputs need to be connected to a program to perform a task.

Our network is represented in part by a list of nodes, with nodes
less than 0 representing inputs, the node equal to zero representing
the bias, nodes greater than MAX_LAYER representing outputs, and nodes
between 1 to MAX_LAYER representing hidden nodes.  This means that
we will run out of hidden node space eventually, but this never happens
in practice, and it makes writing activation and display functions
much easier.
"""
import math

MAX_LAYER = 100000
INPUT_LAYER = 0
OUTPUT_LAYER = MAX_LAYER + 1

def sigmoid(x):
   """A sigmoid function with a gradual slope."""
   if x > 100:
      return 1
   if x < -100:
      return 0
   return 2.0 / (1.0 + math.exp(-4.9*x))

# helper class for our network
class Neuron:
   """A single neuron in our neural network."""
   def __init__(self):
      self.outgoing = []
      self.outgoing_weight = []
      self.value = None
   def __repr__(self):
      neuronString = str(self.outgoing) + '\\' + str(self.value)
      return neuronString

# our network
class Network:
   """
   A neural network, used for calculating outputs to the system.
   Contains neurons, and functions for generating and activating
   a network from genetic information.
   """
   def __init__(self):
      self.neurons = {} # {node: neuron}
   
   def generateNetwork(self, genes, nodes):
      """
      Generate the neural network from its genes and nodes.
      
      Args:
         genes: a dictionary of genes.
         nodes: a list of nodes.
      """
      orderedNodes = sorted(nodes)
      
      # add all the nodes
      for node in orderedNodes:
         self.neurons[node] = Neuron()
         # bias
         if node == 0:
            self.neurons[node].value = 1
            
      # find the outgoing connections and weights
      for _,gene in genes.items():
         if gene.enabled:
            source = gene.source_neuron
            target = gene.target_neuron
            weight = gene.weight
            self.neurons[source].outgoing.append(target)
            self.neurons[source].outgoing_weight.append(weight)
      
   def activateNetwork(self, inputs):
      """
      Activate the neural network.  inputs should not include the bias.

      Args:
         inputs: a tuple or list of inputs
        
      Returns:
         outputs: a list of outputs
      """
      outputs = {}
      neurons = self.neurons
      inputCounter = 0
      
      # flush the network
      for _,neuron in neurons.items():
         neuron.value = None
      
      for node in sorted(neurons):
         neuron = neurons[node]
         # plug in if it's input
         if node < 0:
            neuron.value = inputs[inputCounter]
            inputCounter += 1
            
         if node == 0:
            neuron.value = 1
         
         outgoing = neuron.outgoing
         # add effect to outgoing nodes
         for i in range(outgoing.__len__()):
            if neurons[outgoing[i]].value == None:
               neurons[outgoing[i]].value = 0
            neurons[outgoing[i]].value += neuron.outgoing_weight[i] \
               * sigmoid(neuron.value)
            
         if node > MAX_LAYER:
            outputs[node] = neuron.value
            
      return outputs