"""
This file defines the classes needed to create objects of a given type. It defines species, habitat, plant, and weather
objects, and what methods can be performed using them. Several models have commented out sections- these represent choices
the user can make. For example, it is possible to run a more efficient version of the code, or to chose to run a more
detailed and precise version that takes more processing power to complete. Throughout the code are tips and explanations
of the methods used.
"""
import random
import math
"**********************************************************************************************************************"
class species:
    """
    This class defines the creatures which will be the main agents in this model. This class is used for all animal
    species- predators and prey, omnivores, carnivores and herbivores alike. Through the initial instance variables,
    the differences between species can be defined. This means that all species have the same methods, and can interact
    with one another in a variety of ways. This class is also used to create more creatures of the same species, so
    after initiating the program with a set number of creatures of each species, the creatures replicate independently.
    """
    # map: map on which the creatures are living, habitat object.
    # odds_maturing_to_adult: number between 0 and 100 reprensenting the percent of creatures that survive to the age of maturity
    # adult_age: age of maturation, age at which reproduction is possible
    # av_adult_weight: average weight for an adult of this species
    # av_max_age: average maximum age (age of natural death) for a creature in this species
    # annual_growth_rate: factor of increase of weight per year
    # gestation_period: time between conception and birth, pregnancy duration
    # predators: species which can eat this creature object
    # prey: species / plant types which can be eaten
    # av_speed: average maximum speed
    # av_range: daily range, number of "steps" taken, more theoretical than directly related to a distance
    # vision: average eyesight of this species, written as an integer out of 100
    # sound: average hearing ability of this species, written as an integer out of 100
    # smell: average sense of smell of this species, written as an integer out of 100
    # temp_min: minimum survivable temperature for this species
    # temp_max: maximum surivable temperature for this species
    # water_needs: quantity of water needed per week
    # food needs: amount of food needed per week, in square inchess of plant or pound of meat. Meaning customizable
    # herbivore: True or False, whether this species eats plants or not
    # carnivore: True or False, whether or not this species hunts any other creatures. Species can be both (onmivores)
    # name: species name! used for interactions with others and for data collection
    # number_of_offspring: average number of offspring per pregnancy
    # new generation: True or False, False when first creating creatures. For any creatures created by in-model replication, True.

    def __init__(self, map, odds_maturing_to_adult, adult_age, av_adult_weight, av_max_age, annual_growth_rate,
                 gestation_period, dependency_time,
                 predators, prey, av_speed, av_range, vision, sound, smell, temp_min, temp_max, water_needs,
                 food_needs, herbivore, carnivore, name, number_of_offspring, new_generation):

        # DETERMINING STARTING AGE: THIS IS MAXIMUM LIFESPAN, CREATURES WILL NOT NECESSARILY SURVIVE THIS LONG
        self.odds_maturing_to_adult = odds_maturing_to_adult
        # if not mature, this determines whether a creature will survive to maturity
        if new_generation == True:  # called when existing objects create more objects through reproduce method
            survival = random.randint(0,100)
            if survival > odds_maturing_to_adult:  # this means they will die before reaching maturity
                self.personal_maximum_age_days = (adult_age * random.randint(0, 100) / 100) * 365
            else:
                # otherwise, a random, full lifespan is assigned.
                self.personal_maximum_age_days = (av_max_age * random.randint(85, 115) / 100) * 365  # fixed?

        # DETERMINING CURRENT AGE; AGE THE OBJECT WILL BEGIN WITH
        if new_generation == False:  # randomly assigns an age to each first generation object
            self.age_days = random.randint(1, av_max_age*365)
            self.personal_maximum_age_days = (av_max_age * random.randint(85, 115) / 100) * 365
        else:
            self.age_days = 1  # all second generation objects begin life as one day old creatures

        self.alive = True # all creatures begin alive.

        # determining sex - can be weighted if a species has an uneven distribution
        y = random.randint(0,1)
        if y == 1:
            self.gender = "Male"  # half are female, half are male
        else:
            self.gender = "Female"

        # reproduction-related traits
        self.gestation_period = gestation_period  # period of time between conception and birth
        self.gestation_period_remaining = gestation_period  # to be updated throughout a "pregnancy"
        self.number_of_offspring = number_of_offspring # varies for each instance of reproduction, decided later

        self.dependency_time = dependency_time  # fixme remove this

        self.predators = predators # a list of creature types that can eat this one
        self.prey = prey  # a nested list, each interior list contains a creature name and that creature's odds of survival

        # personal abiities
        self.speed = av_speed * random.randint(75,125)/100  # maximum speed
        self.range = av_range * random.randint(75,125)/100  # daily range- number of "steps" taken
        self.vision = vision * random.randint(85,115)/100
        self.sound = sound * random.randint(85,115)/100
        self.smell = smell * random.randint(85,115)/100

        # this will be used to help determine survival by comparing both species abilities in a predation scenario
        self.coefficient = (self.vision + self.sound + self.smell)/300 + (self.speed)/100

        # these can be built into the weather to determine the impacts of climate
        self.temp_min = temp_min
        self.temp_max = temp_max

        # tracking weekly needs
        self.water_needs = water_needs # total weekly water amounts needed
        self.food_needs = food_needs  # weekly food total needed- i.e numbers of plants, pounds of meat

        # determining pregnancy status, to be updated after an interaction
        self.pregnancy = False
        if self.gender == "Female":
            # females are only fertile if younger than 9/10th of their maximum age in days
            if self.age_days >= (av_max_age - (av_max_age/10)) * 365: # could be fine tuned to a species
                self.fertility = False
            else:
                self.fertility = True

        if self.gender == "Male":  # males are always fertile. NOTE: immature creatures cannot reproduce (see procedures)
            self.fertility = True

        # making an empty list for each of food and water consumption to track these through a week
        self.food_history = [0]
        self.water_history = []


        # determining weight: this is the initial weight, it is later impacted by food history, etc.
        if self.age_days >= adult_age * 365:  # if they are not mature
            self.weight = av_adult_weight * random.randint(70,130)/100  # weight is based off of
            self.mature = False
        else:
            ratio = self.age_days / (adult_age * 365)
            self.weight = av_adult_weight * ratio
            self.mature = True
            # add birth weight later so weight is never zero

        # growth factor per year
        self.annual_growth_rate = annual_growth_rate

        # species prey type
        self.herbivore = herbivore
        self.carnivore = carnivore

        # the habitat in which creatures live and with which they will interact
        self.map = map

        # this is just the open places where we can originally place an animal - not in a river, and prechecked places
        self.map_for_animals = map.animal_available_list

        # chose place for animal randomly based off of the available list
        self.location = self.map_for_animals[random.randint(0, len(self.map_for_animals)-1)]

        # age of maturation, to be used later and to be passed on to offspring
        self.adult_age = adult_age
        # for the purpose of passing onto the future generations
        self.max_age = av_max_age
        # species name
        self.name = name

        # weight if mature, when this is reached, growth slows by a preset factor
        self.adult_weight = random.randint(int(0.70*av_adult_weight), int(1.3*av_adult_weight))

        # to be passed on to future generations. Note: evolution is possible throughout!
        # Instead of using the original instance variables for future generations, pass on the parents' "genetics" to the
        # next generation. For example, use self.speed instead of av_speed. The fittest will survive!
        self.av_speed = av_speed
        self.av_range = av_range

        # important! if the creature's weight drops below this, it will die. This has been combined with a number of
        # weeks a species can go without their necessary amount of food food before dying (preset at 2 weeks.)
        self.minimum_weight = random.randint(int(0.4*self.adult_weight), int(0.8*self.adult_weight))
        # FIXME update weight loss to be more based on the amount of food they are short from their needs

        # these will be updated throughout the course of the model.
        self.drought_status = False  # when a creature has not gotten enough water for a week (but has had at least 30% of their necessary amount)
        self.death_cause = False  # reason for death. useful for statistics later
        self.losing_weight = False  # if a creature has not had enough food in this week, it is losing weight
        self.weight_difference = 0  # instance variable to be used later in determining status

        self.distances_list = []  # distances from shelter, updated later
        self.closest_distance = []  # distance to the closest shelter item
            # note: there is an option for a more efficient and a less efficient but more precise model. The former
            # calculated the distances to 5 randomly chosen shelter objects, and returns the most efficient path from these.
            # The latter calculates all distances, sorts this list, and returns the most efficient path. This one is much


    def print(self):
        """
        Just a simple little method to print useful information about the object. Amend as you like.
        :return: print statements
        """
        print("age is ", self.age_days)
        print("age in days is", self.age_days)
        print("status is", self.alive)
        print("speed is", self.speed)
        print("range is", self.range)
        print("smell is", self.smell)
        print("vision is", self.vision)
        print("weight is", self.weight)
        print("prey are", self.prey)
        print("predators are", self.predators)
        print("fertility status is", self.fertility)


    def step(self, height_change, width_change):
        """
        Step is used many times in a day (determined by range) to move a creature's location. This is how they explore
        an area and search for food, water, etc.
        :param height_change: change in height, which means the change in which internal list the creature is in
        :param width_change: change in position in width, the position inside the specific internal list
        :return: self.location, the position of the creature on the map as a coordinate pair
        """
        self.location[0] = self.location[0]+ height_change  # changing the height (interior list number)
        self.location[1] = self.location[1]+ width_change  # changing the width (position in interior list)
        return self.location  # where the object is in relation to the habitat map


    def eat(self, map):
        """
        eat is the method through which all creatures eat. It uses the map to cross reference the creature's position
        with the position of other creatures and plant objects on the map to determine if the creature can eat anything
        in their position. It only does this if the creature has not already eaten their required food intake for the
        week, in an attempt to leave more food for other creatures. This can be modified to allow a creature to eat a
        given amount above their necessary food intake. It also tracks water intake.
        :param map: the map on which the creatures are located and interacting with other objects
        :return: nothing, amends the self.food_history instance variable.
        """
        # counting the total amount of food eaten so far this week.
        weekly_food_counter = 0
        for amount in self.food_history:  # amount is the amount of food eaten at each step where food was consumed
            weekly_food_counter = weekly_food_counter + amount

        # this block controls whether or not a creature eats, and how much it eats
        if weekly_food_counter < self.food_needs:
            # for all creatures that eat plant material of any kind
            if self.herbivore == True:
                # if the creature's location on the map is occupied by a plant:
                if type(self.map.map[self.location[0]-1][self.location[1]-1]) == plant:
                    # naming this plant plant1 to reference with ease
                    plant1 = self.map.map[self.location[0]-1][self.location[1]-1]
                    if plant1.alive == True:  # only living plants may be eaten!
                        # eating a random amount of the plant, based off of the plant's height
                        height_eaten = random.randint(int(plant1.height/5), int(plant1.height))/plant1.height
                        # avoiding eating nothing as this is unlikely! can be customized
                        if height_eaten == 0:
                            height_eaten = 1
                        amount_eaten = height_eaten * plant1.width  # this is the square amount of plant eaten!
                        self.food_history.append(amount_eaten)  # tracking the amount of plant eaten
                        plant1.be_eaten(height_eaten)  # calling a method to update the plant with the amount that was eaten

            # for all creatures that eat meat
            elif self.carnivore == True:
                for species1, location in map.species_placement.items():  # for each other species and their location
                    #print("here", species1.name)
                    if self.location == location and self != species1 and species1.alive == True:
                        for i in self.prey:  # self is predatory i is species that is the prey types in their list
                            if i[0] == species1.name:
                                species1.distance_to_shelter(map)  # how close is the prey to shelter?
                                # testing the prey's survival. The specifics of this equation can be modified to your liking
                                # they currently take into account the relative abilities of each species in question, and
                                # their distance to shelter, so the prey object can make an escape. There is also a random
                                # element to this
                                prey_survival_odds = random.randint(0,100) +((self.coefficient - species1.coefficient) /(species1.closest_distance+1))
                                if prey_survival_odds > i[1]:  # must be smaller than their odds of survival to survive
                                    # example: a species survives 30% of attacks from another set species. If their survival odds are
                                    # anything over 30, they will not survive, but 30 and under, they will.
                                    species1.alive = False  # the prey creature is no longer alive
                                    print(species1.name, "eaten")  # useful data for fine tuning variables
                                    self.food_history.append(species1.weight)  # add the weight of the prey to the predator's food history

        if self.map.map[self.location[0] - 1][self.location[1] - 1] == "R":  # if they are "in" a river
            #print("water", self.map.map[self.location[0]-1][self.location[1]-1])
            self.water_history.append(self.water_needs/ (7/3))  # each time they find water, they drink a day's worth
        if self.map.map[self.location[0] - 1][self.location[1] - 1] == "W":  # if they are "in" a different water source
            #print("water1", self.map.map[self.location[0] - 1][self.location[1] - 1])
            self.water_history.append(self.water_needs / (7/3))  # each time they find water, they drink a day's worth



    def birth(self, number_of_offspring):
        """
        This method controls the creation of new creatures! So, after a pregnancy and the appropriate gestation period,
        this method takes the appropriate number of offspring for this creature at this time, and creates this many
        new objects of the same type, based off of the instance variables used to create new creature objects of the same
        species.
        Note! Here, you can create evolution! You can set the instance variables used to create the new creatures to be
        the specifics of the parents (which are based off of the initial user- input variables but slightly
        randomized to give the species a range of unique individuals) instead of the original instance variables.
        The most fit will survive to pass on their variables!
        :param number_of_offspring: the number of offspring to be born, the number of objects to be created
        :return: a list containing all of the new creature objects created
        """
        baby_list = []  # an empty list to later hold all the newly created creatures
        for i in range(number_of_offspring):  # create "number_of_offspring" creatures
            # using the instance variables from the parent creature (self) to initiate new creatures
            # add the new creatures to the list of new creatures
            baby_list.append(species(self.map, self.odds_maturing_to_adult, self.adult_age, self.adult_weight, self.max_age, self.annual_growth_rate,
                     self.gestation_period, self.dependency_time,
                     self.predators, self.prey, self.av_speed, self.av_range, self.vision, self.sound, self.smell, self.temp_min, self.temp_max, self.water_needs,
                        self.food_needs, self.herbivore, self.carnivore, self.name, self.number_of_offspring, True))
                        # the final variable, "New Generation", is set to True, to control age and size of the new creatures
                        # this is the only way the initiation of the new creatures differ from the original generation of
                        # creatures.

        return baby_list


    def growth_weekly(self):
        """
        This controls the weekly growth of a creature. It is only called if they have consumed enough food that week.
        :return: updates the instance variable

        """
        if self.weight > self.adult_weight:  # if they are at their mature weight, growth slows to the normal amount
            self.weight = self.weight * (1/52)*self.annual_growth_rate
        else:  # when they are below their mature weight, (either because they are juvenilles or because they are underfed,
            # their weight increases at twice the normal weight
            self.weight = self.weight * (1/26)*self.annual_growth_rate



    def lose_weight(self):
        if self.losing_weight == False: #FIXME MAKE MARGINS MORE REALISTIC can be losing weight for a while but die with no food
            #self.weight_difference = self.weight - self.minimum_weight
            #self.weight = self.weight - (self.weight_difference/2)
            self.losing_weight = True  # informs the way weight loss is processed next time.
            print(self.name, "loosing weight")  # useful when trying to balance a system
        else:
            #self.weight = self.weight - (self.weight_difference / 2)  # can be added to manipulate weight loss
            self.alive = False  # dies of stavation with too little food two weeks in a row
            print(self.name, "lost too much weight ")  # useful for balancing systems
            self.death_cause = "lost too much weight"

    def update_status(self, weekly_food_counter, weekly_water_counter):
        """
        This is called weekly to determine and update the status of the creature after each week's events. This means
        alive versus dead, drought and weight loss status, and weight.
        :param weekly_food_counter: a list containing the creature's food intake in the previous 7 days
        :param weekly_water_counter:  a list containing the creature's water intake in the previous 7 days
        :return: None, updates instance variables
        """
        if weekly_food_counter < self.food_needs:  # if the amount of food eaten total that week is lower than needed
            self.lose_weight()  # lose weight
        else:
            self.losing_weight = False
            if weekly_water_counter > self.water_needs:  # if both food and water intake is sufficient
                self.growth_weekly()  # grow!
        if self.age_days >= self.personal_maximum_age_days:  # if its age is above its maximum age in days
            self.alive = False  # death of old age
            self.death_cause = "age"
        if weekly_water_counter < self.water_needs *0.25:  # USER: CHANGE THIS TO IMPACT DROUGHT TOLERANCE
            self.alive = False  # death of dehydration if less than 1/4 of weekly water needs are consumed
            self.death_cause = "dehydration"
        if weekly_water_counter < self.water_needs and self.drought_status == True:
            self.alive = False  # if already in a drought and not consuming enough water a second week in a row
            self.death_cause = "dehydration"  # death by dehydration
        if weekly_water_counter > self.water_needs*0.25 and weekly_water_counter < self.water_needs:
            # if water intake is between a quarter and the proper amount of water, enters a drought status
            self.drought_status = True


    def distance_to_shelter(self, map):
        """
        Calculates the creature's distance to shelter items. This is used when escaping predators. There are two options-
        one to calculate the creature's distance to every single shelter object, which is more accurate in returning the
        closest distance to shelter, but is computationally complex. The second and more efficient object, on the other
        hand, finds the distance between the creature and each of 5 random shelter objects. It the organizes these and
        finds the shortest distance.
        :param map: the map on which the creature is located, which contains a map of all shelter objects on the map
        :return: updates instance variables
        """
        self.distances_list = []

        # finding 5 random shelter pieces on the map, shown as the number representing their place on the list
        first = random.randint(0, len(map.shelter_placement))
        second = random.randint(0, len(map.shelter_placement))
        third = random.randint(0, len(map.shelter_placement))
        fourth = random.randint(0, len(map.shelter_placement))
        fifth = random.randint(0, len(map.shelter_placement))

        # a list of the actual locations of each of the chosen shelter pieces
        points_list = [map.shelter_placement[first-1], map.shelter_placement[second-1], map.shelter_placement[third-1], map.shelter_placement[fourth-1], map.shelter_placement[fifth-1]]

        # this for loop finds the distance between the creature and the shelter unit in question
        for i in points_list:
            length_distance = self.location[0] - i[0]
            width_distance = self.location[1] - i[1]
            length_squared = length_distance ** 2
            width_squared = width_distance ** 2
            sum = length_squared + width_squared
            distance = math.sqrt(sum)
            # adding the distance to the list
            self.distances_list.append(distance)
        # find the smallest distance
        self.distances_list.sort()
        self.closest_distance = self.distances_list[0]  # use the smallest
        """
        ## This code is less efficient but uses all of the points in the shelter placement list. 
        for i in map.shelter_placement:
            length_distance = self.location[0] - i[0]
            width_distance = self.location[1] - i[1]
            length_squared = length_distance ** 2
            width_squared = width_distance ** 2
            sum = length_squared + width_squared
            distance = math.sqrt(sum)
            self.distances_list.append(distance)
        first = random.randint(0,len(self.distances_list))
        first_point = self.distances_list[first]
        second = random.randint(0,len(self.distances_list))
        second_point = self.distances_list[second]
        third = random.randint(0,len(self.distances_list))
        third_point = self.distances_list[third]
        points_options = [first_point, second_point, third_point]
        points_options.sort()  # this adds a lot of complexity 
        self.closest_distance = points_options[0]
        """



"**********************************************************************************************************************"
class habitat:
    """
    This class is used to create the habitat in which the creatures will live in this model. The most commonly used
    part of a habitat object is the map, which encodes all the information in the habitat in a spatial representation.
    The habitat map, as it is often referred to in future methods and procedures, is a nested list. The length of the
    outer list represents the length of the habitat map, and the length of the interior list represents the width of the
    map. The interior lists contain information about what is at that particular place in the shelter, whether it be
    plant, shelter, or water.

    This is an example map. We will call it map.

    This is the width. It is 7 units wide.
    ________________
    [[0][0][0][0][0][0][0]]      |
    [[0][0][0][0][0][0][0]]      |
    [[0][0][0][0][0][0][0]]      |
    [[0][0][0][0][0][0][0]]    This is the length. It is 8 units wide.
    [[0][0][0][0][0][0][0]]      |
    [[0][0][0][0][0][0][0]]      |
    [[0][0][0][0][0][0][0]]      |
    [[0][0][0][0][0]["R"][0]]

                ^
    This unit has a river on it. The location of the river is map[8][6]. This is backwards from standard coordinates!
    Here, length ( the "y" coordinate) comes before width (the "x" coordinate).

    """
    def __init__(self, area, percent_shelter, average_size_shelter, river_presence):
        """
        Establishes instance variables and creates a habitat object of the given specifications.
        :param area: the area in square units of this habitat.
        :param percent_shelter: the percent of the area of the habitat that is covered in shelter.
        :param average_size_shelter: the average size, in square units, of the shelter clumps, ie how many shelter units tend to be
         in the same area as a group
        :param river_presence: a list containing three elements. The first, True or False, whether or not there is a river. The
         second, the length of the river in units. The third, the width of the river, in units.
        """

        self.area = area
        self.percent_shelter = percent_shelter
        self.average_size_shelter = average_size_shelter
        self.shelter_clump_sizes  = []
        self.lines_per_clump = []
        self.river_presence = river_presence[0]
        self.river_length = river_presence[1]
        self.river_width = river_presence[2]
        self.units_of_shelter = 0

        self.available_list = []  # available shelter units
        self.animal_available_list = []  # places where animals can be (places on the map)
        self.plants = []

        self.species_placement = {}
        self.shelter_placement = []


    def create_map(self):
        """
        Creates the map (nested list) of the proper area, using random length, and the corresponding width. The width is
        the nested interior list, and the length is the exterior list.
        :return: self.map - the completed map
        """
        # creating the map randomly
        holder = int(math.sqrt(self.area))  # this is to prevent the creation of an extrordinarily long and skinny map
        self.length = random.randint(int(holder*0.5), int(holder*1.5))  # ensures each side is of at least moderate length
       # print(self.length, "length")  # can be used to show map dimensions
        self.width = int(self.area/self.length)  # finding the corresponding width
       # print(self.width, "width")
        self.map = []
        mini_map = []

        # this for loop creates the map through the use of a mini map to be a placeholder.
        for i in range(0, self.length):  # creating the exterior list
            for j in range(0, self.width):  # creating the interior list
                mini_map.append(0)  # filling each map space with a 0
            self.map.append(mini_map)
            mini_map = []
        return self.map


    def create_random_shelter_units(self):
        """
        This makes the shelter units randomly sized based off of the average size defined in the instance variables. It
        does not go above the number of shelter units given in the instance variables.
        :return: the sizes of the shelter clumps
        """
        # setting randomly sized units of shelter
        self.units_of_shelter = int(self.percent_shelter/100 * self.area)  # square feet or units
        #print("units total shelter", units_of_shelter) # helpful at the start
        counter = 0
        while self.units_of_shelter > 0:  # while there are still remaining units of shelter
            # a clump is between half and twice the average shelter size, normally
            clump_size = random.randint(int(self.average_size_shelter/2), int(2*self.average_size_shelter))
            # if the clump is larger than the remaining units of shelter, the clump is the remaining units of shelter
            if self.units_of_shelter < clump_size:
                clump_size = self.units_of_shelter
            # adding the clump size to the list
            self.shelter_clump_sizes.append(clump_size)
            # keeping a counter of total units used
            counter = counter + clump_size
            # tracking the units of shelter used so as not to go over
            self.units_of_shelter = self.units_of_shelter - clump_size
            #print(units_of_shelter, "units left")
     #   print("sizes", self.shelter_clump_sizes, "counter", counter)  # useful
        return self.shelter_clump_sizes


    def space_clump_sizes(self):
        """
        Randomly spacing out the clumps. This randomly breaks the shelter clump into lines of different lengths, to be
        stacked vertically. This will give varied shapes of shelter, so they are not uniform, and not a single line.
        :return: updates the self.lines_per_clump instance variable
        """
        clump_list = []
        lines_per_clump = []
      #  print(self.shelter_clump_sizes)
        for i in self.shelter_clump_sizes:  # for each shelter clump
            while i > 0:  # while there are units of shelter remaining
                line_size = random.randint(1, i)  # a randomly sized line at most the remaining number of units left
                clump_list.append(line_size)  # add this to the list
                i  = i - line_size  # remove these from the remaining units
            lines_per_clump.append(clump_list)  #add the list of lines per that clump to the overlal list
            clump_list = []
        self.lines_per_clump = lines_per_clump  # update the instance variable
     #   print(self.lines_per_clump)
        return self.lines_per_clump



    def place_shelter(self):
        """
        This method places the shelter units in their respective clumps on the map. If only one shelter unit is in a place,
        the space is mapped with a "S", and if there are two, then it is a "DS", for "dense shelter". There may not be
        three shelter units overlapping; if a shelter unit is placed on "DS", this method returns False and so it starts
        over finding a place for this shelter clump.
        :return: True - indicating all units were placed successfully
        """
        mini_map = []
        map_holder = []

        # this for loop creates a replica of the main map object. This is so this method can try out multiple placements
        # of shelter clumps before finding the one that works for all shelter units.
        for i in self.map:
            for j in i:
                mini_map.append(j)
            map_holder.append(mini_map)
            mini_map = []

        for i in self.lines_per_clump:  # for each shelter clump
            width_coordinate = random.randint(1, self.width)  # cho0se a random coordinate within the width
            length_coordinate = random.randint(1, self.length)   # choose a random coordinate within the length
            for j in i: # for each line in each shelter clump
                for k in range(j):  # in the range of the length of this line of the shelter clump
                    if width_coordinate < (self.width) and length_coordinate < (self.length):  # checking it fits the map
                        if map_holder[length_coordinate-1][width_coordinate-1] == 0:  # if blank, place shelter
                            map_holder[length_coordinate-1][width_coordinate-1] = "S"
                            # adding this to the list of locations with shelter
                            self.shelter_placement.append([length_coordinate, width_coordinate, "S"])
                        elif map_holder[length_coordinate-1][width_coordinate-1] == "S":  # if sheltered, add dense shelter
                            map_holder[length_coordinate-1][width_coordinate-1] = "DS"
                            # adding this to the list of locations with shelter
                            self.shelter_placement.append([length_coordinate, width_coordinate, "DS"])
                        while map_holder[length_coordinate-1][width_coordinate-1] == "R" or map_holder[length_coordinate-1][width_coordinate-1] == "W":
                            # if there is water or a river here, select a different coordinate and start over
                            width_coordinate = random.randint(1, self.width)
                            length_coordinate = random.randint(1, self.length)
                    else:  # if this goes off the edge of the map
                        self.shelter_placement = []  # clear this instance variable
                        return False  # start the placement over. This means a line went over the edge
                    width_coordinate = width_coordinate + 1  # move over one for the length of the line

                length_coordinate = length_coordinate + 1  # move down one for a new line in the shelter clump
            width_coordinate = width_coordinate - j  # reset location

        self.map = map_holder # if all works, set the main map equal to the placeholder
        #print(self.shelter_placement) # can be useful
        return True


    def check_if_available(self):
        """
        This is used to make placing the next environmental factors (plants) more efficient. It is a list of spaces with
        no other information or objects, spaces that only contain "0". The locations of these spaces are added to a list
        as a list coordinate (ie [2][1]).
        :return: updates the available list instance variable
        """
        self.available_list = []
        first_counter = 0
        second_counter = 0

        # this for loop finds the available spaces, spaces which only contain "0"
        for i in self.map: # for each exterior list (aka length)
            first_counter = first_counter + 1  # counting the current location
            for n in i:  # for the interior lists in this exterior list
                second_counter = second_counter + 1  # tracking this location as well
                if n == 0:  # if this space is empty
                    self.available_list.append([first_counter-1, second_counter-1])  # adding the location to the list
                else:
                    pass  # can be used to create a list of filled spaces
            second_counter = 0  # resetting the counter each time.



    def check_if_available_for_animal(self):
        """
        Ensures that creatures are not placed in the water. This is used to make creature placement more efficient.
        :return: updates and returns the animal_available list instance variable
        """
        self.animal_available_list = []
        first_counter = 0
        second_counter = 0

        for i in self.map:
            first_counter = first_counter + 1  # tracking current location in exterior list
            for n in i:
                second_counter = second_counter + 1  # tracking location in interior list
                if n != "R" and n != "W":  # if it is not water, add to list of available locations
                    self.animal_available_list.append([first_counter-1, second_counter-1])
                else:
                    pass  # this can be added if you want to note spaces with water
                  #  print("no", n)
            second_counter = 0
        return self.animal_available_list



    def place_rivers(self):
        """
        This code places the rivers on the map using the self.river_presence instance variable for the data. This is done
        before shelter objects are creates, so river spaces do not need to be placed in a manner that avoids shelter clumps.
        :return: updates the map
        """
        mini_map_river = []
        map_holder_river = []

        # this makes a mini map to hold the river data placement attepts before pushing these through to the main map
        for i in self.map:  # each outer list
            for j in i:  # each inner list
                mini_map_river.append(j)
            map_holder_river.append(mini_map_river)
            mini_map_river = []

        if self.river_presence == True:  # only make a river if there is a river on the map!
            length_coordinate = 0
            width_coordinate = 0
            for i in range(self.river_width):  # this will move left to right adding river units depending on width
                for i in range(self.river_length):  # this will go downwards as long as necessary until length is met
                    # checking that we have not moved off of the map
                    if length_coordinate < self.length and width_coordinate < self.width:
                        # adding a river marker
                        map_holder_river[length_coordinate-1][width_coordinate] = "R"
                        # moving diagonally down the map
                        length_coordinate = length_coordinate + 1
                        width_coordinate = width_coordinate + 1
                    else:
                        # if placing this river unit would take us off the map, place the unit of water randomly
                        random_length = random.randint(1, self.length)
                        random_width = random.randint(1, self.width)
                        while map_holder_river[random_length-1][random_width-1] != 0:
                            # keep trying random coordinated until one is an empty space
                            random_length = random.randint(1, self.length)
                            random_width = random.randint(1, self.width)
                        # place this unit as "W" for water instead of river.
                        map_holder_river[random_length-1][random_width-1] = "W"
                length_coordinate = 1  # move the length over by one to go through the next diagonal line
                width_coordinate = 0  # start the width over

            # when complete, use the map_river_holder to replace the map object.
            # the map object now has river markers
            self.map = map_holder_river

    def place_plant_objects(self, plant_objects):
        """
        This method places the plant objets created elsewhere on the map. It places the entire object here, which enables
        them to be manipulated simply and efficiently. It uses the available_list to find empty (non water) spots to
        place plants.
        :param plant_objects: A list of plant objects
        :return: modifies the map to include the plant objects on the map.
        """
        # for each plant object in the list
        for i in plant_objects:
            # add this object to the list of plants known by the map
            self.plants.append(i)
            # select a random point within the map- this is a point from the list of available points
            # this point represents a location on the available_list, which is a coordinate that is available on the map
            point = random.randint(0, len(self.available_list)-1)
            #print(self.available_list[point][0], self.available_list[point][1])  # useful
            # sets the location on the map (selected by the random point referenced with the available list) to the plant object
            (self.map[self.available_list[point][0]][self.available_list[point][1]]) = i


"**********************************************************************************************************************"
class plant:
    """
    This class, Plant, creates all producers in the ecosystem. These serve as the base of the food chain, and are necessary
    for the survival of all other organisms. The growth of plants depends on the weather of the week, in relation to their
    specified needs for rain and sunlight (the latter can be added if relevant to an ecosystem, reproducing the water method).
    Each week, if they have has sufficient water, they will grow. If their height falls below their minimum height, they
    will die. This class can reproduce independently using the special method. # fixme add types of plants
    """
    def __init__(self, average_width, average_height, weekly_growth, weekly_water_needs, nutrient_needs, minimum_height, number_seeds, seed_distribution, cover_provided, mature):
        """
        This method creates a plant object and establishes the instance variables.
        :param average_width: the average mature width of this plant species ( at the widest part)
        :param average_height: the average height of mature plants of this species
        :param weekly_growth: average weekly growth in inches (if a plant receives the necessary nutrients)
        :param weekly_water_needs: amount of water needed for this plant species to survive and grow
        :param nutrient_needs: optional, can be added if relevent. Nutrient richness necessary to thrive
        :param minimum_height: smallest this plant species can be reduced to and still grow back / survive
        :param number_seeds: the average number of seeds produced by this plant species
        :param seed_distribution: optional, use if using plant evolution.
        :param cover_provided: can be used to provide cover to small creatures
        :param mature: True or False, whether or not this plant is a new generation
        """

        self.alive = True
        # personal minimum height- related to the minimum height for the species in general
        self.minimum_height = random.randint(int(75*minimum_height), int(125*minimum_height))/100

        self.mature = mature

        if self.mature == True:
            # mature plants have higher needs than immature plants. This can be customzed to better match the ecosystem
            self.nutrient_needs = nutrient_needs
            self.weekly_growth_average = weekly_growth
            # height and width are selected randomly based off of instance variables
            self.width = random.randint(int(5 * average_width), int(15 * average_width)) / 10  # initial width
            self.height = random.randint(int(75 * average_height), int(125 * average_height)) / 100   # initial height
            self.water_needs = random.randint(int(9 * weekly_water_needs), int(11 * weekly_water_needs)) / 10
            pollinated = random.randint(0,1)  # these odds can be manipulated to represent a specific ecosystem
            if pollinated == 1:
                self.pollinated = True
            else:
                self.pollinated = False
        else:
            # immature plants do not need as much to grow, due to size and lack or reproduction
            self.pollinated = False
            self.nutrient_needs = nutrient_needs /10
            self.weekly_growth_average = weekly_growth * 2  # faster growth rate
            # height and width are selected randomly based off of instance variables
            self.width = random.randint(int(5 * average_width), int(15 * average_width)) / 100
            self.height = random.randint(int(75 * average_height), int(125 * average_height)) / 1000
            # can be customized
            self.water_needs = random.randint(int(9 * weekly_water_needs), int(11 * weekly_water_needs)) / 100

        # number of seeds will vary between plants
        self.number_seeds = int(random.randint(int(75*number_seeds), int(125*number_seeds))/100)
        # optional, can be used. Currently, random seed distribution
        self.seed_distribution = random.randint(int(5*seed_distribution), int(15*seed_distribution))/10
        # can also be used, just add to the "distance to shelter" code for small enough species. Optional
        self.cover_provided = cover_provided*((self.width*self.height)/100)  # percent cover provided per inch of height

        # creating empty logs to store information in later
        self.water_log = []
        self.nutrient_log =[]

        # impacts water needs and status
        self.drought_status = False

        # to be passed on to the next generation
        self.average_width = average_width
        self.average_height = average_height
        self.weekly_growth = weekly_growth
        self.weekly_water_needs = weekly_water_needs

        # a placeholder as the plant currently has no death cause
        self.death_cause = False



    def growth(self, weekly_water):
        """
        Growth updates the plant object's size depending on the plant's water intake in the previous week, the plant's
        drought status, and the plants size ( maturity status).
        :param weekly_water: the total amount of water consumed throughout the week
        :return: the amount of growth- either 0 or a float. Updates instance variables
        """
        # updating maturity status and pollination status
        if self.mature == False:
            if self.height >= self.average_height:  # if it is not mature but above mature height
                self.mature = True  # becomes mature
                pollinated = random.randint(0, 1)  # testing pollination and updating
                if pollinated == 1:
                    self.pollinated = True
                else:
                    self.pollinated = False
            else:
                self.mature = False  # remains immature if below the margin

        # determining growth
        if self.drought_status == True:  # did not get enough water last week
            if weekly_water < self.water_needs:  # not enough water for 2 weeks in a row, dead
                self.alive = False
                self.death_cause = "plant drought"  # useful for balancinh ecosystems
                return 0
            else:
                self.drought_status = False  # enough water this week. Growth is possible
                # the growth will be a random amount in the preset range
                growth =  random.randint(75*self.weekly_growth_average, 125*self.weekly_growth_average)/100
                # print("growth", growth)  # can be useful
                # the growth is divided equally beween the plant's heigt and width to maining the plant's dimension ratop
                self.height = self.height + growth /2
                self.width = self.width + growth /2
                return growth
        else:  # not currently in a state of drought
            if weekly_water < self.water_needs:  # not enough water, into drought
                self.drought_status = True  # updating instance variable
                return 0
            else:
                self.drought_status = False    # enough water, growth
                growth = random.randint(75 * self.weekly_growth_average, 125 * self.weekly_growth_average) / 100
                #print(growth)
                self.height = self.height + growth / 2
                self.width = self.width + growth / 2
                return growth



    def be_eaten(self, amount_eaten):
        """
        Determines if a plant survives being eaten by comparing the amount of the plant that is eaten to the plant's
        current height and their minimum height.
        :param amount_eaten: the percent of the plant that is eaten
        :return: updates the plant's height
        """
        self.height = self.height * (1- amount_eaten)  # calculating how much of the plant is left after being eaten
        # checking if the plant survives being eaten
        if self.height < self.minimum_height:
            self.alive = False
            self.death_cause = "eaten"



    def reproduce(self, map):
        """
        This method creates more plant objects using the parameters initially used to create the plant objects. It creates
        a specific number of them based off of the plant's number of seeds. These newly created plants are then placed
        onto the map randomly. This could be based off of the plant's seed distribution if desired. This is only called
        if a plant is fertilized so it does not need to check this.
        :param map: the map representing the habitat object the plants are to be placed on
        :return: the list of newly created plants (baby_plants)
        """
        baby_plants = []
        for i in range(self.number_seeds):
            #print("new plant") # helps to see if replication is happening
            # makes new plants based off of the variables used to create the original plants
            # however, these new plants are not mature.
            baby_plants.append(plant(self.average_width, self.average_height, self.weekly_growth, self.weekly_water_needs, self.nutrient_needs, self.minimum_height, self.number_seeds, self.seed_distribution, self.cover_provided, True))
            map.place_plant_objects(baby_plants)  # placing the plants on the map using the map method
        self.pollinated = False  # after seeds are produced, fertility reverts to false
        return baby_plants


"**********************************************************************************************************************"
class weather:  # ADD WIND AS A POLLINATION METHOD LATER, TEMPERATURE, ETC
    def __init__(self, rain_frequency, rain_levels, average_sun_levels):
        self.rain_frequency = rain_frequency  # percent out of 100 that it rains
        self.average_amount_rain = rain_levels
        self.average_sun_levels = average_sun_levels
        self.sun_level_daily = 0
        self.rain = False
        self.amount_rain = 0

    def daily_weather(self):
        rain_day = random.randint(0, 100)
        #print(rain_day, self.rain_frequency)
        if rain_day <= self.rain_frequency:  # FIXME deal with sun presence ASAP!!!!!!!!!
            self.rain = True
        else:
            self.rain = False
        if self.rain == True:
            self.amount_rain = random.randint(5*self.average_amount_rain, 15*self.average_amount_rain)/10
            self.sun_level_daily = random.randint(1*self.average_sun_levels, 5*self.average_sun_levels)/10
        else:
            self.amount_rain = 0
            self.sun_level_daily = random.randint(5*self.average_sun_levels, 15*self.average_sun_levels)/10
        return self.amount_rain

