Car Simulation with Neural Networks

This repository contains a Python implementation of a car simulation using neural networks and the NeuroEvolution of Augmenting Topologies (NEAT) algorithm. The simulation is built using the Pygame library.

Features:
Car Class: Represents a car in the simulation. Handles car movement, collision detection, sensor data collection, and rendering.

NeuralNetwork Class: Manages the neural network associated with each car. Takes input from car sensors and produces output for car control.

Simulation Class: Orchestrates the main simulation loop. Utilizes NEAT for evolving neural networks over generations.

Files:
car_simulation.py: The main script containing the simulation logic, car class, neural network class, and the simulation loop.

config.txt: NEAT configuration file specifying the genetic algorithm parameters.

car.png: Sprite image for the car.

map.png: Map image for the simulation environment.

Usage:
Clone the repository:

bash
Copy code
git clone https://github.com/mariemsamout/simulation_car
Install the required dependencies:










