# Blender-N-Body-Simulation-Plugin
A plugin for Blender 2.79 that allows you to create and animate N-body simulations.  
This is a project I made for CodeDay 2019.
## Simulation
The simulation uses Newtonian gravity. The simulation automatically determines and simulates from the reference frame of the center of mass. The simulation is not live - it is calculated and then saved for you to view. The program simulates the system for the given number of timesteps, and keyframes the bodies at each step. This creates an animation which you can rewatch and save. This animation can be overridden if you want to redo the simulation.
## Collisions
Collisions are perfectly inelastic. When two bodies collide, they combine into one sphere which is scaled accordingly.

# Options
All functions of the plugin can be found in the operator search pop-up menu (opened by pressing spacebar in blender 2.79).
## Properties
All objects in the simulation have certain custom properties. These are found in the object tab under "Custom Properties" (at the bottom).
 * Active - If this value is 0, the object is not part of the N-body simulation. If this value is one, the object is part of the N-body simulation.
 * mass - The object's mass in kg.
 * velocity - The object's velocity vector in m/s \[velocity x, velocity y, velocity z]
## Setup n body simulation
Open operator search (by pressing spacebar) and search for "setup n body simulation".  
Clicking this will add all the necessary properties to all objects. Missing properties are added and randomized. By default, if the Active property is added it is set to 0 (the object will not be part of the simulation unless you change this property to 1). You could also manually add in all properties, but this functionality is here to make your life easier.
## Generate random bodies
Open operator search (by pressing spacebar) and search for "generate random bodies".  
Clicking this will prompt you with the amount of bodies to generate. The program will then generate this amount of random bodies, randomly setting their mass, velocity, and position (the range of randomly generated positions depends on the amount of bodies, and was fine tuned to lead to the most interesting simulations, although this is not always the case). The random bodies generated will have an Active property set to 1, meaning that they will be part of the simulation by default.
## Simulate (n body simulation)
Open operator search (by pressing spacebar) and search for "simulate (n body simulation)".  
Clicking this will prompt you to set the distance scale, time step, iterations (the number of time steps simulated), and the interval (the number of time steps per frame). When you click OK, the computer will start simulating. Once it finishes, you can view the simulation.
