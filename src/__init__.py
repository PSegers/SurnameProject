from random import randint
from random import shuffle
from statistics import mean
import time

"""
author: Pieterjan Segers
version: 1.0
date: 14/07/2017

Calculates how much surnames go extinct over a certain period of time.
Takes into consideration the arguments listed below.

Keyword arguments:
population(int) -- population of a certain group of individuals
classes(int) -- how this population is classified evenly (surnames)
gen_amount(int) -- how many generations will pass (every generation is approximately 20-30 years)
birthrate(int) -- birthrate of children in integer percentages
sim_runs(int) -- how many times the simulation is ran
    
NOTES:
    * Most console prints disabled

TODO:
    * Add exceptions
"""
template = input("Use a template? ")
if template == "Zoersel" or template == "zoersel":
    population = 21000
    classes = 611
    birthrate = 175
elif template == "test":
    population = 10000
    classes = 305
    birthrate = int(input("Birthrate in %? (no decimals) "))
else:
    population = int(input("Population? "))
    classes = int(input("# of classes? "))
    birthrate = int(input("Birthrate in %? (no decimals) "))

gen_amount = int(input("# of generations? "))
sim_runs = int(input("How many times should the simulation be run? "))
generations = dict()


def creation(population, classes):
    """
    Initial generation creation. Will evenly distributed amount of classes (surnames) across population.
    Afterwards, the created list is shuffled.
    :param population:
    :param classes:
    :return:
    """

    generation = list()
    population2 = (population//classes)*classes

    for x in range(classes):
        for y in range(population2//classes):
            generation.append(x)
        # print("Surname " + str(x) + " completely assigned.")

    # print("Generation 0 complete. Initiating Shuffle.")
    shuffle(generation)
    # print("Shuffle complete.")
    add_gen(generation, 0)
    # print("Initial generation created.")


def add_gen(gen, era):
    """
    Adds a generation to the "generations" dictionary.
    :param gen:
    :param era:
    :return:
    """
    generations["Gen{0}".format(era)] = gen


def pairing(gen, era):
    """
    Pairs two couples together and creates children according to the birthrate.
    The surnames of the children are decided on a 50/50 basis — either father's or mother's name
    :param gen:
    :param era:
    :return:
    """
    new_gen = list()
    # If only one surname remains, simply keep the generation intact.
    if len(set(gen)) == 1:
        add_gen(gen, era)
    else:
        # Half of the population of generation x is coupled with the other half.
        for n in range(len(gen)//2):
            # 50/50 chance on which surname is given to the child(ren).
            randpair = randint(1, 2)
            br_whole = int(birthrate/100)
            br_remain = birthrate-br_whole*100
            if randpair == 1:
                # Birthrate of children. 175% birthrate means one child and 75% chance for a second child.
                for x in range(int(br_whole)):
                    new_gen.append(gen[2*n])
                rand_br = randint(0, 99)
                if rand_br < br_remain:
                    new_gen.append(gen[2*n])

            else:
                for x in range(int(br_whole)):
                    new_gen.append(gen[2*n+1])
                rand_br = randint(0, 99)
                if rand_br < br_remain:
                    new_gen.append(gen[2*n+1])

            # print(str(n) + "/" + str(len(gen)) + " completed.")

        # print("Generation " + str(era) + " complete. Initiating Shuffle.")
        shuffle(new_gen)
        # print("Shuffle of generation " + str(era) + " complete.")
        add_gen(new_gen, era)

# The simulation is run x times to get an average number.
remains = list()
extinct = list()
remaining_pop = list()
start_time = time.time()
for x in range(sim_runs):
    # Initial generation creation
    creation(population, classes)

    # Pairing is done for the amount of generations given.
    for y in range(gen_amount):
        # print("Starting creation of generation " + str(x))
        pairing(generations["Gen{0}".format(y)], y+1)

    remains.append(len(set(generations["Gen{0}".format(gen_amount)])))
    extinct.append(classes - len(set(generations["Gen{0}".format(gen_amount)])))
    remaining_pop.append(len(generations["Gen{0}".format(gen_amount)]))
    print("Simulation " + str(x+1) + "/" + str(sim_runs) + " complete.")
    print("--- %.2f seconds elapsed ---" % (time.time() - start_time))

# Information is printed.
print("===============================================================================================================")
print("You started with " + str(classes)
      + " surnames distributed evenly across a population of approximately "
      + str(population) + " people, with a birthrate of "
      + str(birthrate) + "%, over "
      + str(sim_runs) + " simulations.")

print("After " + str(gen_amount)
      + " generations, you ended up with an average of " + str(mean(remaining_pop))
      + " people left, with an average of " + str(mean(remains)) + " surnames remaining.")

print("This means an average of " + str(mean(extinct)) + " surnames went extinct.")
print("===============================================================================================================")
print("--- %.2f seconds elapsed ---" % (time.time() - start_time))
print("End of simulation.")
