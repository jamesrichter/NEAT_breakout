from distutils.core import setup
import py2exe
import numpy
import pygame
setup(console=['human_breakout.py', 'driver.py', 'winningDriver.py'])