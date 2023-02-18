# Evolving Creatures - A Simulation of Evolutionary Process using Genetic Algorithm

The project embodies a simplified implementation of evolving virtual creatures over several generations through the use of phisical simulation engine and evolutionary algorithms. This attempts to implement the work of Sims (1994), inspired by the lecture on bio-inspired computing within Artificial Intelligence module from [University of London](https://www.london.ac.uk).

You can also visit the web page for the project [here](https://hanzholahs.quarto.pub/contents/projects/04-evolving-creatures/). 

## Objectives 

This is intended to create a program that can simulate evolutionary process of creatures within a simulated environment, which requires the capability of the program to:

* transform a sequence of numbers (representing genotype) which was initally generated randomly, and represent this sequence into a virtual creature that can act in a simulated environment by a physics engine (representing phenotype).
* run the creatures within a simulation environment and evaluate their fitness based on a specified function.
* perform genetical manipulation of the creatures to generate subsequent generation based on the fitness of the population. These include the selection of fittest parents, crossover parents’ dna and mutation of creature genes.

## Limitations

Some adjustments to the implementation of evolving virtual creatures by Sims (1994) were made.

* Sensors, internal neural nodes, and effectors to control the creatures from the original paper are not covered in this implementation. Instead, the more straightforward control mechanisms are defined, which constitute pre-defined functions to specify the speed of the body parts movements based on the joint types.
* In the implementation, it is impossible for a body part to be connected with two or more different body parts with different genotype. If there is four genotypes connected with each other, each body type defined by its genotype is connected only to other parts from two other genotypes at maximum.
* The behavioural selection used was only walking towards a specific direction. The fitness of a creature is based on the distance. This means that the genes of creatures with the longest distance traveled are more likely to survived for the next generation. Simpler creatures are preferred so that there is a penalty for each creature with larger number of body parts.

## Progress

- [x] Virtual Creature
    - [x] Basic genome and phenotype class
    - [x] Creature class
- [x] Environment
    - [x] Simulator class
    - [x] Creature XML read and write
    - [x] Creature movements
- [x] New generation
    - [x] Selection of parents
    - [x] Mating of parents
    - [x] Mutation of genes
- [ ] Simulation run
    - [x] Execution trial
    - [ ] Simulation run
- [ ] Report writing


## Reference

K. Sims, “Evolving virtual creatures,” in Proceedings of the 21st annual conference on Computer graphics and interactive techniques  - SIGGRAPH ’94, Not Known, 1994, pp. 15–22. doi: 10.1145/192161.192167.

