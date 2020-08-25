"""
This code is an attempt to work out the classes and perform some basic methods with them.
"""
import random
import math
"**********************************************************************************************************************"
class species:
    # add growth later...
    # make preset models later too with types of species ie wolf rabbit, so they don't have to add all the variables
    # odds maturing should be a number between 1 and 100 representing percentage survived to adulthood
    # adult age is age of maturation
    def __init__(self, map, odds_maturing_to_adult, adult_age, av_adult_weight, av_max_age, annual_growth_rate,
                 gestation_period, dependency_time,
                 predators, prey, av_speed, av_range, vision, sound, smell, temp_min, temp_max, water_needs,
                 food_needs, herbivore, carnivore, name, number_of_offspring, new_generation):

        #FIXME make all ages in days?
        self.odds_maturing_to_adult = odds_maturing_to_adult
        if new_generation == True:
            survival = random.randint(0,100)
            if survival <= odds_maturing_to_adult:
                self.personal_maximum_age_days = (av_max_age * random.randint(85, 115) / 100) * 365
            else:
                self.personal_maximum_age_days = random.randint(0,int(adult_age*365))


        # age, alive or dead
        self.max_age = av_max_age

        if new_generation == False:
            self.age_days = random.randint(1, av_max_age*365)
            self.personal_maximum_age_days = (av_max_age * random.randint(85, 115) / 100) * 365
        else:
            self.age_days = 1/365

        #print("age", self.age, "age of maturation", adult_age)

        """  
        if self.age < adult_age:  # if they are not mature yet
            x = random.randint(1,100)
            #print(x)
            if x <= odds_maturing_to_adult:
                self.alive = True
            else:
                self.alive = False
        else:
            self.alive = True
        """
        self.number_of_offspring = number_of_offspring
        self.alive = True #

        #print(self.alive)
        # make all of these actual stats a bell curve distribution later

        self.gestation_period = gestation_period
        self.gestation_period_remaining = gestation_period
        self.dependency_time = dependency_time

        self.predators = predators
        self.prey = prey

        # personal abiities
        self.speed = av_speed * random.randint(75,125)/100
        self.range = av_range * random.randint(75,125)/100
        self.vision = vision * random.randint(85,115)/100
        self.sound = sound * random.randint(85,115)/100
        self.smell = smell * random.randint(85,115)/100
        #print(self.speed, self.range, self.vision, self.sound, self.smell)

        self.temp_min = temp_min
        self.temp_max = temp_max
        self.water_needs = water_needs
        self.food_needs = food_needs  # weekly food total needed

        # determining gender - can be weighted if a species has an uneven distribution
        y = random.randint(0,1)
        if y == 1:
            self.gender = "Male"
        else:
            self.gender = "Female"
       # print(self.gender)
        # determining fertility
        self.pregnancy = False
        if self.gender == "Female":
            if self.age_days >= (av_max_age - (av_max_age/10)) * 365: # could be fine tuned to a species
                self.fertility = False
            else:
                self.fertility = True

        if self.gender == "Male":
            self.fertility = True
        #print(self.fertility)

        # making an empty dictionary
        self.food_history = [0]
        self.water_history = []


        # determining weight - not based on food......
        if self.age_days >= adult_age * 365:
            self.weight = av_adult_weight * random.randint(70,130)/100
            self.mature = False
        else:
            ratio = self.age_days / (adult_age * 365)
            self.weight = av_adult_weight * ratio
            self.mature = True
            # add birth weight later so weight is never zero

        #print(self.weight)
        self.adult_age = adult_age

        self.annual_growth_rate = annual_growth_rate

        #print(self.personal_maximum_age)

        self.herbivore = herbivore
        self.carnivore = carnivore
        self.map = map

        self.map_for_animals = map.animal_available_list  # this is just the open places where we can originally place an animal

        # chose place for animal
        self.location = self.map_for_animals[random.randint(0, len(self.map_for_animals)-1)]
       ### map.species_placement.extend([self, self.location])
        #print(self.location)

        self.name = name
        self.adult_weight = random.randint(int(0.70*av_adult_weight), int(1.3*av_adult_weight))

        self.av_speed = av_speed
        self.av_range = av_range
        self.minimum_weight = random.randint(int(0.4*self.adult_weight), int(0.8*self.adult_weight))

        self.drought_status = False
        self.death_cause = False
        self.losing_weight = False
        self.weight_difference = 0



    def print(self):
        print("age is ", self.age_days)   # FIXME Make ages follow a more realistic distribution
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
        # add number of kids, dependency status, etc


    def day(self):
        self.age_days = self.age_days + 1

    def step(self, height_change, width_change):
        #print(self.age, self.location)
        self.location[0] = self.location[0]+ height_change
        self.location[1] = self.location[1]+ width_change
        #print(self.location)
        return self.location


    def eat(self):  #FIXME don't let animals go into the river.
        #print(self.map.map[0][1])
        #print(self.location)
        #print(self.location[0], self.location[1])
        weekly_food_counter = 0
        for i in self.food_history:
            weekly_food_counter = weekly_food_counter + i
        if weekly_food_counter < self.food_needs:
            if self.herbivore == True:
                if type(self.map.map[self.location[0]-1][self.location[1]-1]) == plant:
                   # print(plant)
                    plant1 = self.map.map[self.location[0]-1][self.location[1]-1]
                    if plant1.alive == True:

                        height_eaten = random.randint(int(plant1.height/5), int(plant1.height))/plant1.height
                        amount_eaten = height_eaten * plant1.width
                    #print("amount eaten", amount_eaten)
                        self.food_history.append(amount_eaten)
                        plant1.be_eaten(height_eaten)
                else:
                    pass

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
                        self.food_needs, self.herbivore, self.carnivore, self.name, self.number_of_offspring, True))
            #print("new baby animal here !!!!!!!!!!")
        #print("list from main", baby_list)

        return baby_list


    def growth_weekly(self):
        if self.weight < self.adult_weight:
            self.weight = self.weight * (1/52)*self.annual_growth_rate #FIXME make food required relative to weight

    def lose_weight(self):
        if self.losing_weight == False: #FIXME MAKE MARGINS MORE REALISTIC can be losing weight for a while but die with no food
            self.weight_difference = self.weight - self.minimum_weight
            self.weight = self.weight - (self.weight_difference/2)
            self.losing_weight = True
        else:
            self.weight = self.weight - (self.weight_difference / 2)
            self.alive = False
            self.death_cause = "lost too much weight"

    def update_status(self, weekly_food_counter, weekly_water_counter):
        if weekly_food_counter < self.food_needs:
            self.lose_weight()
            #print(self, "loosing weight")
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
            width_coordinate = random.randint(0, self.width)
            length_coordinate = random.randint(0, self.length)
            for j in i:
                for k in range(j):
                    if width_coordinate < (self.width) and  length_coordinate < (self.length):
                        if map_holder[length_coordinate-1][width_coordinate-1] == 0:
                            map_holder[length_coordinate-1][width_coordinate-1] = "S"
                        elif map_holder[length_coordinate-1][width_coordinate-1] == "S":
                            map_holder[length_coordinate-1][width_coordinate-1] = "DS"
                        while map_holder[length_coordinate-1][width_coordinate-1] == "R" or map_holder[length_coordinate-1][width_coordinate-1] == "W":
                            #print("beeo", map_holder[length_coordinate-1][width_coordinate-1])
                            width_coordinate = random.randint(0, self.width)
                            length_coordinate = random.randint(0, self.length)
                    else:
                       # print("hete")
                        return False
                    width_coordinate = width_coordinate + 1

                length_coordinate = length_coordinate + 1
                width_coordinate = width_coordinate - j
            #print(x_coordinate, y_coordinate)
        self.map = map_holder
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
        self.height = self.height * amount_eaten
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

