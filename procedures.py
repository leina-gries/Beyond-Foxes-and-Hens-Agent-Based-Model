"""
Leina Gries
Summer 2020
For Pomona College's RAISE Summer Fellowship Program
This file implements the classes defined in "ecosystem-classes.py". This code passes parameters to each class, initiating
various species, a habitat, and plants. Then, it carries out days, updating the status of each object on a daily or weekly
basis. Each day, weather statistics impact plant growth, as species objects move randomly around the habitat map, searching
for food, water, and mates. To modify the workings of the classes themselves, modify "ecosystem-classes.py". In order to
modify their parameters, the length of the run, or the order of operations, modify this file.
"""
from main import *  # can be removed if you combine both of the files into one

"**********************************************************************************************************************"

"********************************************    PROCEDURES    ********************************************************"

"**********************************************************************************************************************"
def create_creatures(number, map, odds_maturing_to_adult, adult_age, av_adult_weight, av_max_age, annual_growth_rate,
                 gestation_period, dependency_time,
                 predators, prey, av_speed, av_range, vision, sound, smell, temp_min, temp_max, water_needs,
                 food_needs, herbivore, carnivore, name, number_of_offspring, new_generation):
    """
    This method makes a set number of creatures of the same species (the species "name"), based on "number". It initiates
    and returns the list of creatures created.

    :param number: the number of creatures to be created of this species
    :param map: map on which the creatures are living, habitat object.
    :param odds_maturing_to_adult: number between 0 and 100 representing the percent of creatures that survive to the age of maturity
    :param adult_age: age of maturation, age at which reproduction is possible
    :param av_adult_weight: average weight for an adult of this species
    :param av_max_age: average maximum age (age of natural death) for a creature in this species
    :param annual_growth_rate: factor of increase of weight per year
    :param gestation_period: time between conception and birth, pregnancy duration
    :param predators: species which can eat this creature object
    :param prey: species / plant types which can be eaten
    :param av_speed: average maximum speed
    :param av_range: daily range, number of "steps" taken, more theoretical than directly related to a distance
    :param vision: average eyesight of this species, written as an integer out of 100
    :param sound: average hearing ability of this species, written as an integer out of 100
    :param smell: average sense of smell of this species, written as an integer out of 100
    :param temp_min: minimum survivable temperature for this species
    :param temp_max: maximum survivable temperature for this species
    :param water_needs: quantity of water needed per week
    :param food_needs: amount of food needed per week, in square inches of plant or pound of meat. Meaning customizable
    :param herbivore: True or False, whether this species eats plants or not
    :param carnivore: True or False, whether or not this species hunts any other creatures. Species can be both (omnivores)
    :param name: species name! used for interactions with others and for data collection
    :param number_of_offspring: average number of offspring per pregnancy
    :param new_generation: True or False, False when first creating creatures. For any creatures created by in-model replication, True.
    :return: the list of creatures created
    """
    my_creatures = []

    # creating "number" of creatures of the same species
    for i in range(number):
        my_creatures.append(species(map, odds_maturing_to_adult, adult_age, av_adult_weight, av_max_age, annual_growth_rate,
                 gestation_period, dependency_time,
                 predators, prey, av_speed, av_range, vision, sound, smell, temp_min, temp_max, water_needs,
                 food_needs, herbivore, carnivore, name, number_of_offspring, new_generation))
    return my_creatures


"**********************************************************************************************************************"
def create_habitat(plants):
    """
    This method creates a fully functional habitat. First, it initializes the habitat object. Next, it creates the map,
    then the rivers, shelter clusters, and places the plants and animals in the habitat.
    :param plants: a list of plant objects, already created
    :return: habitat object, the completed object
    """
    habitat_object = habitat(2000,10,20, [True,80,4]) # creating the object
    # area = 2000
    # percent_shelter = 10
    # average size shelter = 20
    # river_presence = True
    # river_length = 80
    # river_width = 4
    habitat_object.create_map()  # making the map
    habitat_object.place_rivers()  # adding the river

    habitat_object.create_random_shelter_units()  # creating randomly sized shelter units
    habitat_object.space_clump_sizes()  # spacing out shelter clumps into line lengths

    while habitat_object.place_shelter() == False:  # placing the shelter objects until all can be placed
        habitat_object.place_shelter()

    habitat_object.check_if_available()
    habitat_object.place_plant_objects(plants)  # placing plant objects
    habitat_object.check_if_available_for_animal()  # updating instance variable for later


    return habitat_object
"**********************************************************************************************************************"
def make_weather():
    """
    Creates the daily weather for the habitat.
    :return: weather1- the amount of rain for the day
    """
    weather1 = weather(80, 4, 90)
    # rain frequency = 80% chance of rain on any given day
    # rain quantity = 4
    # average sun levels = 90
    return weather1

"**********************************************************************************************************************"
def make_plants(number):
    """
    Creates and initializes a set number of plant objects based off of the same parameters.
    :param number: the number of plant objects to be created
    :return: the list of plant objects
    """
    my_plants = []
    for i in range(number):
        my_plants.append(plant(10,10,2,6,90,2,10,0,8,True))
        # average_width = 10
        # average_height = 10
        # weekly_growth = 2
        # weekly_water_needs = 6
        # nutrient_needs = 90
        # minimum_height = 2
        # number_seeds = 10
        # seed_distribution = 0
        # cover_provided = 9
        # mature = True
    #for i in my_plants:  # useful for learning the code
    #    print(i)

    return my_plants


"**********************************************************************************************************************"
def animal_day(creature, map):
    """
    This function lets creatures move around for their full range, attempting to eat, drink, and mate at each step by
    calling the necessary class methods. It also updates pregnancy status and gestation period, calling for more creature
    creation when a creature's gestation period is complete.
    :param creature: the species object who is moving and interacting with the habitat
    :param map: the map on which the species object exists
    :return: the number of new creatures produced in this creature's day
    """

    # the "length" of the day is different for each creature as it is based on their individual range.
    for i in range(int(creature.range)):
     #   print("my range is", creature.range) # useful to begin
        length_step = random.randint(-1,1)  # deciding which direction the step will be in - imagine this like a coordinate vector
        width_step = random.randint(-1,1)
        #print(creature.location) # useful for viewing movement
        # to prevent the creature from walking off of the map (top or bottom)
        if creature.location[0] + length_step > map.length or creature.location[0] + length_step <= 0:
            length_step = length_step * (-1)  # reverse direction
        # to prevent the creature from walking off of the map (left or right)
        if creature.location[1]+ width_step > map.width or creature.location[1] + width_step <= 0:
            width_step = width_step * (-1)  # reverse direction)

        # use these coordinates to update location
        creature.step(length_step, width_step)
        map.species_placement[creature] = creature.location # updates location

        # this for loop will check if mating can occur
        for species1, location in map.species_placement.items():
            if creature.location == location and creature != species:  # same place but not the same object
                if creature.name == species1.name:  # same species
                    #print("interaction!") # useful
                    if creature.gender != species1.gender:  # opposite sex
                        if creature.gender == "Female":  # this one will become pregnant if successful
                            if creature.fertility == True:
                                if creature.pregnancy == False:
                                    # could add in odds of mating success here if wanted
                                    creature.pregnancy = True
                                    creature.gestation_period_remaining = creature.gestation_period

                        if species1.gender == "Female":
                            if species1.fertility == True:
                                if species1.pregnancy == False:
                                    creature.pregnancy = True
                                    creature.gestation_period_remaining = creature.gestation_period

        # attempt to eat at every step
        creature.eat(map)

    # tracking pregnancy progress and development over time
    if creature.pregnancy == True:
        # updating time left until birth
        creature.gestation_period_remaining = creature.gestation_period_remaining - 1
       # print(creature, creature.gestation_period_remaining)  # can be useful
        baby_animals = []

        # this handles birth
        if creature.gestation_period_remaining == 0:  # birthday of new creatures
            # randomly choosing a number of offspring based off of instance variables
            number_of_offspring = random.randint(int(creature.number_of_offspring / 4), creature.number_of_offspring * 2)
            list = creature.birth(number_of_offspring)

            # adding all new creatures to a list
            for i in list:
                baby_animals.append(i)
            return baby_animals
    return 0  # if no new creatures created today


"**********************************************************************************************************************"
def plant_week(plants, map, weather):
    """
    This method takes each plant object in plants through a week, using the same weather (sun and rain) values for each
    plant. Then, it updates the status of each plant based on sun availability, and initiates growth and reproduction,
    before finishing the week by determining pollination.
    :param plants: the list of all plant objects in the habitat
    :param map: the habitat object's map
    :param weather: the weather object created for this model
    :return: the list of any new plants created this week
    """

    new_plants = []

    # creating the weather each day for the week
    weekly_weather = []
    for i in range(7):
        weekly_weather.append(weather.daily_weather())

    # creating a list of sun levels of each day of the week
    weekly_sun = []
    for i in range(7):
        weekly_sun.append(weather.sun_level_daily)

    # totalling the rain amounts that week
    rain_counter = 0
    for i in weekly_weather:
        rain_counter = rain_counter + i

    # totalling the amount of sun that week
    sun_counter = 0
    for i in weekly_sun:
        sun_counter = sun_counter + i

    growth_amount = 0

    # this for loop updates the status of plants, calling for growth and reproduction as necessary, as well as
    # updating pollination status
    for plant1 in plants:
        if plant1.alive == True:
            if sun_counter > weather.average_sun_levels / 20:
                # must have at least some sun to grow - can be customized
                # this calls growth, which in turn checks out water intake.
                growth_amount = plant1.growth(rain_counter)

            if plant1.pollinated == True and sun_counter > weather.average_sun_levels / 20:
                # must have some sun and be pollinated in order to reproduce
                new_plants = plant.reproduce(plant1, map)

            if growth_amount > 0:
                # the plant must be healthy enough to grow in order to be pollinated
                # odds are customizable
                pollination_status = random.randint(0,1)
                if pollination_status == 1:
                    plant1.pollinated = True
    return new_plants


"**********************************************************************************************************************"


def main():
    """

    """
    plants = make_plants(1500)  # making (x) plant objects

    map = (create_habitat(plants))  # making the habitat object using the plant objects

    all_creatures = []

    # creating the creature species objects for the model
    deer = create_creatures(50,map, 80, 3,100,18,2,60,100,["wolf"], [["P", 100]], 40,500,90,100,80,0,100,30,15,True, False, "deer", 3, False)
    mice = create_creatures(150,map,90,1,1,2,2,15,0,["wolf"],[["P",0]],20,100,90,90,90,30,90,5,0.5,True, False, "mouse", 15,False)
    rabbits = create_creatures(190, map,90,1,5,2,2,15,3,["wolf"], [["P",0]],37,350,125,100,100,100,100,10,3, True, False, "rabbit", 8, False)  # making 20 creatures using the map #FIXME make this easier to set up different creatures
    wolves = create_creatures(8, map, 70, 2, 100, 8, 2, 90,90,[], [["rabbit", 45], ["mouse", 40], ["deer", 90]], 34,250,100,100,100,0,90,10,4,False, True, "wolf", 5, False)
    # add one of these to add more creatures
    # creature = create_creature(number, map, odds_maturing_to_adult, adult_age, av_adult_weight, av_max_age, annual_growth_rate,
    #                  gestation_period, dependency_time,
    #                  predators, prey, av_speed, av_range, vision, sound, smell, temp_min, temp_max, water_needs,
    #                  food_needs, herbivore, carnivore, name, number_of_offspring, new_generation)

    # adding each type of creature to the list of all creatures
    for i in rabbits:
        all_creatures.append(i)
    for i in wolves:
        all_creatures.append(i)
    for i in mice:
        all_creatures.append(i)
    for i in deer:
        all_creatures.append(i)
    # add one of these to add the other species to the list
    # for i in creature:
    #    all_creatures.append(i)

    for i in all_creatures:
        map.species_placement[i] = i.location
        # giving each creature a place

    print(len(all_creatures)) # useful to begin

    # establishing population trackers beginning with initial populations
    mouse_history = [len(mice)]
    wolf_history = [len(wolves)]
    rabbit_history = [len(rabbits)]
    deer_history = [len(deer)]
    # species_history = [len(species)]
    plant_history = [len(plants)]

    # this for loop runs the model in its entirety for (x) weeks
    for week in range(2):
        print("Week number:", week + 1)  # useful for tracking populations
        for day in range(7):  # a week
            for animal in all_creatures:
                if animal.alive == True:
                    new_creatures = animal_day(animal, map) # doing the daily movements each day
                    if new_creatures != 0:  # adding any new creatures to the list of all creatures
                        for i in new_creatures:
                            all_creatures.append(i)
                    animal.age_days = animal.age_days + 1
        rabbit_counter = 0
        wolf_counter = 0
        mouse_counter = 0
        deer_counter = 0
        # species_counter = 0

        for i in all_creatures:
            # counting living creatures
            if i.name == "rabbit" and i.alive == True:
                rabbit_counter = rabbit_counter + 1
            elif i.name == "wolf" and i.alive == True:
                wolf_counter = wolf_counter + 1
            elif i.name == "mouse" and i.alive == True:
                mouse_counter = mouse_counter + 1
            elif i.name == "deer" and i.alive == True:
                deer_counter = deer_counter + 1
            # elif i.name == "species" and i.alive == True:
                # species_counter = species_counter + 1

            # updating the status of all living animals
            if i.alive == True:
                if i.age_days > i.dependency_time:  # can be modified, my version of infant care by the mother
                    weekly_food_counter = 0
                    # finding total food
                    for food in i.food_history:
                        weekly_food_counter = weekly_food_counter + food
                    #print(weekly_food_counter, i.food_needs)  # useful for balancing
                    #print("total food", i.food_history, weekly_food_counter)
                    i.food_history = []
                    weekly_water_counter = 0
                    # finding total water
                    for drink in i.water_history:
                        weekly_water_counter = weekly_water_counter + drink
                    # updating status of all creatures
                    i.update_status(weekly_food_counter, weekly_water_counter)

        mouse_history.append(mouse_counter)
        rabbit_history.append(rabbit_counter)
        wolf_history.append(wolf_counter)
        deer_history.append(deer_counter)
        # species_history.append(species_counter)
        print("mice", mouse_counter)
        print("rabbits", rabbit_counter)
        print("wolves", wolf_counter)
        print("deer", deer_counter)
        # print("species", species_counter)

        more_plants = plant_week(plants, map, make_weather())  # plant week complete with weather
        # adding any new plants to the list
        for i in more_plants:
            plants.append(i)
        weekly_plant_counter = 0
        # counting plants
        for i in plants:
            if i.alive == True:
                weekly_plant_counter = weekly_plant_counter + 1
            else:
                pass
                #print(i.death_cause)  # useful for tracking growth and death

        plant_history.append(weekly_plant_counter)
        print("plants", weekly_plant_counter)
        print("plants overall", plant_history)

        # printing current full history at the end of each week
        # this means you can stop a run at any time and still easily get the data set for the days run
        print("rabbits", rabbit_history)
        print("wolves", wolf_history)
        print("mouse", mouse_history)
        print("deer", deer_history)
        #print("species", species_history)

    print("Model of ", week + 1, " weeks complete.")
    print("Plant history: ",plant_history)

    print("Rabbit history:", rabbit_history)
    print("Wolf history:", wolf_history)
    print("Mouse history:", mouse_history)
    print("Deer history:", deer_history)


main()






