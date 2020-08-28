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
        Just a simple little method to print useful information about the object.
        :return:
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
        return self.location


    def eat(self, map):  #FIXME don't let animals go into the river, or make this an option.
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
                for species1, location in map.species_placement.items():
                    #print("here", species1.name)
                    if self.location == location and self != species1 and species1.alive == True:
                        for i in self.prey:  # self is predatory i is species that is the prey
                            if i[0] == species1.name:
                                species1.distance_to_shelter(map)  # how close is the prey to shelter?
                                prey_survival_odds = random.randint(0,100) +((self.coefficient - species1.coefficient) /(species1.closest_distance+1))
                                if prey_survival_odds > i[1]:
                                    species1.alive = False
                                    print(species1.name, "eaten")
                                    self.food_history.append(species1.weight)

        if self.map.map[self.location[0] - 1][self.location[1] - 1] == "R":
            #print("water", self.map.map[self.location[0]-1][self.location[1]-1])
            self.water_history.append(self.water_needs/ (7/3))  # each time they find water, they drink a day's worth
        if self.map.map[self.location[0] - 1][self.location[1] - 1] == "W":
            #print("water1", self.map.map[self.location[0] - 1][self.location[1] - 1])
            self.water_history.append(self.water_needs / (7/3))  # each time they find water, they drink a day's worth

                #self.food_history.append("no plant here.")

        ###print(self.map.map[self.location[0][self.location[1]]])
        #print(self.map_for_animals)
       # print(self.map_for_animals[self.location[0]][self.location[1]])
    def birth(self, number_of_offspring):
        baby_list = []
        for i in range(number_of_offspring):
            baby_list.append(species(self.map, self.odds_maturing_to_adult, self.adult_age, self.adult_weight, self.max_age, self.annual_growth_rate,
                     self.gestation_period, self.dependency_time,
                     self.predators, self.prey, self.av_speed, self.av_range, self.vision, self.sound, self.smell, self.temp_min, self.temp_max, self.water_needs,
                        self.food_needs, self.herbivore, self.carnivore, self.name, self.number_of_offspring, False))
            #print("new baby animal here !!!!!!!!!!")
        #print("list from main", baby_list)

        return baby_list


    def growth_weekly(self):
        if self.weight > self.adult_weight:
            self.weight = self.weight * (1/52)*self.annual_growth_rate #FIXME make food required relative to weight
        else:
            self.weight = self.weight * (1/26)*self.annual_growth_rate

    def lose_weight(self):
        if self.losing_weight == False: #FIXME MAKE MARGINS MORE REALISTIC can be losing weight for a while but die with no food
            #self.weight_difference = self.weight - self.minimum_weight
            #self.weight = self.weight - (self.weight_difference/2)
            self.losing_weight = True
            print(self.name, "loosing weight")
        else:
            #self.weight = self.weight - (self.weight_difference / 2)
            self.alive = False
            print(self.name, "lost too much")
            self.death_cause = "lost too much weight"

    def update_status(self, weekly_food_counter, weekly_water_counter):
        if weekly_food_counter < self.food_needs:
            self.lose_weight()
        else:
            self.losing_weight = False
            if weekly_water_counter > self.water_needs:
                self.growth_weekly()
        #if self.weight < self.minimum_weight and self.age:
        #    self.alive = False
        #    self.death_cause = "starvation"
        if self.age_days >= self.personal_maximum_age_days:
            self.alive = False
            self.death_cause = "age"
        if weekly_water_counter < self.water_needs *0.25:  # CHANGE THIS TO IMPACT DROUGHT TOLERANCE
            self.alive = False
            self.death_cause = "dehydration"
        if weekly_water_counter < self.water_needs and self.drought_status == True:
            self.alive = False
            self.death_cause = "dehydration"
        if weekly_water_counter > self.water_needs*0.25 and weekly_water_counter < self.water_needs:
            self.drought_status = True


    def distance_to_shelter(self, map):
        self.distances_list = []

        first = random.randint(0, len(map.shelter_placement))
        second = random.randint(0, len(map.shelter_placement))
        third = random.randint(0, len(map.shelter_placement))
        fourth = random.randint(0, len(map.shelter_placement))
        fifth = random.randint(0, len(map.shelter_placement))
        points_list = [map.shelter_placement[first-1], map.shelter_placement[second-1], map.shelter_placement[third-1], map.shelter_placement[fourth-1], map.shelter_placement[fifth-1]]
        for i in points_list:
            length_distance = self.location[0] - i[0]
            width_distance = self.location[1] - i[1]
            length_squared = length_distance ** 2
            width_squared = width_distance ** 2
            sum = length_squared + width_squared
            distance = math.sqrt(sum)
            self.distances_list.append(distance)
        self.distances_list.sort()
        self.closest_distance = self.distances_list[0]
        """
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
        points_options.sort()
        self.closest_distance = points_options[0]
        """




"""
    def time_basics(self, duration):  # duration is in years
        for i in range(0, duration + 1):
            self.age = self.age + 1
            if self.age >= self.adult_age:
                self.weight = self.weight * self.annual_growth_rate
        if self.age == self.personal_maximum_age:
            self.alive = False
            # otherwise, weight is going to depend on amount eaten... deal with this later
            # deal with whether or not they get eaten.... or starve
"""
"**********************************************************************************************************************"
class habitat:
    # river: array, present or not, length, width, works for rivers and lengths
    def __init__(self, area, percent_shelter, average_size_shelter, river_presence, nutrient_availability, sun_availabiility, max_temp,
                 min_temp, precipitation_frequency, precipitation_amount):

        self.area = area
        self.percent_shelter = percent_shelter
        self.average_size_shelter = average_size_shelter
        self.shelter_clump_sizes  = []
        self.lines_per_clump = []
        self.river_presence = river_presence[0]
        self.river_length = river_presence[1]
        self.river_width = river_presence[2]
        self.units_of_shelter = 0

        self.available_list = []
        self.animal_available_list = []
        self.plants = []

        self.species_placement = {}
        self.shelter_placement = []


    def create_map(self):

        # creating the map randomly
        holder = int(math.sqrt(self.area))
        self.length = random.randint(int(holder*0.5), int(holder*1.5))
       # print(self.length, "length")
        self.width = int(self.area/self.length)
       # print(self.width, "width")
        self.map = []
        mini_map = []
        for i in range(0, self.length):
            for j in range(0, self.width):
                mini_map.append(0)
            self.map.append(mini_map)
            mini_map = []
        return self.map

    def create_random_shelter_units(self):
        # setting randomly sized units of shelter
        self.units_of_shelter = int(self.percent_shelter/100 * self.area)  # square feet
        #print("units total shelter", units_of_shelter)
        counter = 0
        while self.units_of_shelter > 0:
            clump_size = random.randint(int(self.average_size_shelter/2), int(2*self.average_size_shelter))
            if self.units_of_shelter < clump_size:
                clump_size = self.units_of_shelter
            self.shelter_clump_sizes.append(clump_size)
            counter = counter + clump_size
            self.units_of_shelter = self.units_of_shelter - clump_size
            #print(units_of_shelter, "units left")
     #   print("sizes", self.shelter_clump_sizes, "counter", counter)
        return self.shelter_clump_sizes

        # randomly spacing the units of shelter in their size clumps out
    def space_clump_sizes(self):
        clump_list = []
        lines_per_clump = []
      #  print(self.shelter_clump_sizes)
        for i in self.shelter_clump_sizes:
            while i > 0:
                line_size = random.randint(1, i)
                clump_list.append(line_size)
                i  = i - line_size
            lines_per_clump.append(clump_list)
            clump_list = []
        self.lines_per_clump = lines_per_clump
     #   print(self.lines_per_clump)
        return self.lines_per_clump

        # checking if a space is available
    def place_shelter(self):
        #print("here!!!!!!", self.width, self.length)
        mini_map = []
        map_holder = []
        for i in self.map:
            for j in i:
                mini_map.append(j)
            map_holder.append(mini_map)
            mini_map = []

        #FIXME MAKE IT SO THE SHELTER CANNOT BE PLACED ON A RIVER EITHER
        #FIXME add in the test is availble
        for i in self.lines_per_clump:
            width_coordinate = random.randint(1, self.width)
            length_coordinate = random.randint(1, self.length)
            for j in i:
                for k in range(j):
                    if width_coordinate < (self.width) and length_coordinate < (self.length):
                        if map_holder[length_coordinate-1][width_coordinate-1] == 0:
                            map_holder[length_coordinate-1][width_coordinate-1] = "S"
                            self.shelter_placement.append([length_coordinate, width_coordinate, "S"])
                        elif map_holder[length_coordinate-1][width_coordinate-1] == "S":
                            map_holder[length_coordinate-1][width_coordinate-1] = "DS"
                            self.shelter_placement.append([length_coordinate, width_coordinate, "DS"])
                        while map_holder[length_coordinate-1][width_coordinate-1] == "R" or map_holder[length_coordinate-1][width_coordinate-1] == "W":
                            #print("beeo", map_holder[length_coordinate-1][width_coordinate-1])
                            width_coordinate = random.randint(1, self.width)
                            length_coordinate = random.randint(1, self.length)
                    else:
                       # print("hete")
                        return False
                    width_coordinate = width_coordinate + 1

                length_coordinate = length_coordinate + 1
            width_coordinate = width_coordinate - j
            #print(x_coordinate, y_coordinate)
        self.map = map_holder
        #print(self.shelter_placement)
        return True


    def check_if_available(self):
        self.available_list = []
        first_counter = 0
        second_counter = 0
        for i in self.map:
            first_counter = first_counter + 1
            for n in i:
                second_counter = second_counter + 1
                if n == 0:
                    self.available_list.append([first_counter-1, second_counter-1])
                else:
                    pass
                  #  print("no", n)
            second_counter = 0
       # print(self.available_list)


    def check_if_available_for_animal(self):
        self.animal_available_list = []
        first_counter = 0
        second_counter = 0
        for i in self.map:
            first_counter = first_counter + 1
            for n in i:
                second_counter = second_counter + 1
                if n != "R" and n != "W":
                    self.animal_available_list.append([first_counter-1, second_counter-1])
                else:
                    pass
                  #  print("no", n)
            second_counter = 0
        return self.animal_available_list




    def place_rivers(self):

        mini_map_river = []
        map_holder_river = []
        for i in self.map:
            for j in i:
                mini_map_river.append(j)
            map_holder_river.append(mini_map_river)
            mini_map_river = []


       # print(self.river_presence)
        if self.river_presence == True:
            # first, a flat accross river. no slope, just going across until
           # print(self.river_length, self.river_width)
            length_coordinate = 0
            width_coordinate = 0
            for i in range(self.river_width):
                for i in range(self.river_length):
                    if length_coordinate < self.length and width_coordinate < self.width:
                        map_holder_river[length_coordinate-1][width_coordinate] = "R"
                        length_coordinate = length_coordinate + 1
                        width_coordinate = width_coordinate + 1
                    else:
                        random_length = random.randint(1, self.length)
                        random_width = random.randint(1, self.width)
                        while map_holder_river[random_length-1][random_width-1] != 0:
                            random_length = random.randint(1, self.length)
                            random_width = random.randint(1, self.width)
                        map_holder_river[random_length-1][random_width-1] = "W"
                length_coordinate = 1
                width_coordinate = 0
            self.map = map_holder_river

    def place_plant_objects(self, plant_objects):

        for i in plant_objects:
            self.plants.append(i)
            point = random.randint(0, len(self.available_list)-1)
            #print(self.available_list[point][0], self.available_list[point][1])
            (self.map[self.available_list[point][0]][self.available_list[point][1]]) = i
        #print(self.map)








        """
            random_length = random.randint(1, self.length)
            random_width = random.randint(1, self.width)
            if self.map[random_length-1][random_width-1] == "0":
                print("wooot")
            else:
               while self.map[random_length - 1][random_width - 1] != "0":
                    random_length = random.randint(1, self.length)
                    random_width = random.randint(1, self.width)
        """

"**********************************************************************************************************************"
class plant:  #FIXME starting with just one species and assuming that all animals can eat it, add impact of temperature, seasons, etc
    # FIXME add light
    def __init__(self, average_width, average_height, weekly_growth, weekly_water_needs, nutrient_needs, minimum_height, number_seeds, seed_distribution, cover_provided, mature):


        self.alive = True
        #self.density = density # number of plants per square foot  # mayve do this in a more metal place????
        self.minimum_height = random.randint(int(75*minimum_height), int(125*minimum_height))/100
        self.mature = mature

        if self.mature == True:
            self.nutrient_needs = nutrient_needs
            self.weekly_growth_average = weekly_growth
            self.width = random.randint(int(5 * average_width), int(15 * average_width)) / 10
            self.height = random.randint(int(75 * average_height), int(125 * average_height)) / 100
            self.water_needs = random.randint(int(9 * weekly_water_needs), int(11 * weekly_water_needs)) / 10
            pollinated = random.randint(0,1)
            if pollinated == 1:
                self.pollinated = True
            else:
                self.pollinated = False
        else:
            self.pollinated = False
            self.nutrient_needs = nutrient_needs /10
            self.weekly_growth_average = weekly_growth * 2
            self.width = random.randint(int(5 * average_width), int(15 * average_width)) / 100
            self.height = random.randint(int(75 * average_height), int(125 * average_height)) / 1000
            self.water_needs = random.randint(int(9 * weekly_water_needs), int(11 * weekly_water_needs)) / 100

        self.number_seeds = int(random.randint(int(75*number_seeds), int(125*number_seeds))/100)
        #print(self.number_seeds)
        self.seed_distribution = random.randint(int(5*seed_distribution), int(15*seed_distribution))/10
        self.cover_provided = cover_provided*((self.width*self.height)/100)  # percent cover provided per inch of height
        self.water_log = []        # currently on a two week set up, make variable later.
        self.nutrient_log =[]
        self.drought_status = False

        self.average_width = average_width
        self.average_height = average_height
        self.weekly_growth = weekly_growth
        self.weekly_water_needs = weekly_water_needs

        self.death_cause = False




    def growth(self, weekly_water):  # done at the end of each week
        if self.mature == False:
            if self.height >= self.average_height:
                self.mature = True
                pollinated = random.randint(0, 1)
                if pollinated == 1:
                    self.pollinated = True
                else:
                    self.pollinated = False
            else:
                self.mature = False

        if self.drought_status == True:  # did not get enough water last week
            if weekly_water < self.water_needs:  # not enough water for 2 weeks in a row, dead
                self.alive = False
                self.death_cause = "plant drought"
                return 0
            else:
                self.drought_status = False  # enough water, growth
                growth =  random.randint(75*self.weekly_growth_average, 125*self.weekly_growth_average)/100
               # print("growth", growth)
                self.height = self.height + growth /2
                self.width = self.width + growth /2
                return growth
        else:  # not currently in a state of drought
            if weekly_water < self.water_needs:  # not enough water, into drought
                self.drought_status = True
                return 0
            else:
                self.drought_status = False    # enough water, growth
                growth = random.randint(75 * self.weekly_growth_average, 125 * self.weekly_growth_average) / 100
                #print(growth)
                self.height = self.height + growth / 2
                self.width = self.width + growth / 2
                return growth




    def print1(self):
        print("yeeeeeeee")

    def be_eaten(self, amount_eaten):
        self.height = self.height * (1- amount_eaten)
        if self.height < self.minimum_height:
            self.alive = False
            self.death_cause = "eaten"
        #print("hereherehere", amount_eaten)

    def reproduce(self, map):
        baby_plants = []  # fixme make plant replication seasonal
        for i in range(self.number_seeds):
            #print("new plant")
            baby_plants.append(plant(self.average_width, self.average_height, self.weekly_growth, self.weekly_water_needs, self.nutrient_needs, self.minimum_height, self.number_seeds, self.seed_distribution, self.cover_provided, False))
            map.place_plant_objects(baby_plants)
        self.pollinated = False
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

