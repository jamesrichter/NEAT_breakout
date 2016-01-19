Welcome to a NEAT system, and my project for CS 499.

If you own both python and the pygame library, you can run 
the NEAT system by opening the command window and typing:

python driver.py

If you do not own python, you can run the NEAT system by
looking in the "dist" folder and executing driver.exe.

Once you have run the NEAT driver to the point where it
learns to complete a Breakout game, it will keep looping
the completed game until the window is closed.  However,
it will also save the completed game under the file
winning_genome.
In order to load winning_genome, you can either type into
the command window:

python winningDriver.py

or, in the "dist" folder, executing winningDriver.exe.

Note: there is a bug where the closing the pygame window
will overwrite the file winning_genome.  Do not run 
driver.py or driver.exe until you are finished with 
winningDriver.

There is a small difference between the executable driver
and the python driver.  The fonts will not work on the
executable driver.  This has no affect on the NEAT system,
but it is nice to see the fitness score of the game being
played.

If you want to play the Breakout game yourself, you can
either type "python human_breakout.py" in a command
window, or go into "dist" and execute human_breakout.py.
Use spacebar to start the game, and after three lives,
you can restart the game by pressing enter.

Enjoy!