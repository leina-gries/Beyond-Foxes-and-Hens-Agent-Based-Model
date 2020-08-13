"""
This code is an attempt to work out the classes and perform some basic methods with them.
"""
import random
import math
"**********************************************************************************************************************"
class species:
    # later this should be a nice little GUI
    # add growth later...
    # make preset models later too with types of species ie wolf rabbit, so they don't have to add all the variables
    # odds maturing should be a number between 1 and 100 representing percentage survived to adulthood
    def __init__(self, odds_maturing_to_adult, adult_age, av__adult_weight, av_max_age, annual_growth_rate,
                 gestation_period, dependency_time,
                 predators, prey, av_speed, av_range, vision, sound, smell, temp_min, temp_max, water_needs,
                 food_needs):

        # age, alive or dead
        self.age = random.randint(0, av_max_age)
        #print("age", self.age, "age of maturation", adult_age)
        if self.age < adult_age:  # if they are not mature yet
            x = random.randint(1,100)
            #print(x)
            if x <= odds_maturing_to_adult:
                self.alive = True
            else:
                self.alive = False
        else:
            self.alive = True

        self.age_days = self.age * 365

        #print(self.alive)
        # make all of these actual stats a bell curve distribution later

        self.gestation_period = gestation_period
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
        self.food_needs = food_needs

        # determining gender - can be weighted if a species has an uneven distribution
        y = random.randint(0,1)
        if y == 1:
            self.gender = "Male"
        else:
            self.gender = "Female"
       # print(self.gender)
        # determining fertility
        if self.gender == "Female":
            if self.age >= av_max_age - (av_max_age/10): # could be fine tuned to a species
                self.fertility = False
                self.pregnancy = False
            else:
                self.fertility = True

        if self.gender == "Male":
            self.fertility = True
        #print(self.fertility)

        # making an empty dictionary
        self.food_history = {}
        self.water_history = {}


        # determining weight - not based on food......
        if self.age >= adult_age:
            self.weight = av__adult_weight * random.randint(70,130)/100
        else:
            ratio = self.age / adult_age
            self.weight = av__adult_weight * ratio
            # add birth weight later so weight is never zero

        #print(self.weight)
        self.adult_age = adult_age

        self.annual_growth_rate = annual_growth_rate

        self.personal_maximum_age = av_max_age * random.randint(85,115)/100
        #print(self.personal_maximum_age)


    def print(self):
        print("age is ", self.age)   # FIXME Make ages follow a more realistic distribution
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



    def create_map(self):

        # creating the map randomly
        holder = int(math.sqrt(self.area))
        self.length = random.randint(int(holder*0.5), int(holder*1.5))
        print(self.length, "length")
        self.width = int(self.area/self.length)
        print(self.width, "width")
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
        print("sizes", self.shelter_clump_sizes, "counter", counter)
        return self.shelter_clump_sizes

        # randomly spacing the units of shelter in their size clumps out
    def space_clump_sizes(self):
        clump_list = []
        lines_per_clump = []
        print(self.shelter_clump_sizes)
        for i in self.shelter_clump_sizes:
            while i > 0:
                line_size = random.randint(1, i)
                clump_list.append(line_size)
                i  = i - line_size
            lines_per_clump.append(clump_list)
            clump_list = []
        self.lines_per_clump = lines_per_clump
        print(self.lines_per_clump)
        return self.lines_per_clump

        # checking if a space is available
    def check_if_available(self): #FIXME Rename
        mini_map = []
        map_holder = []
        for i in self.map:
            for j in i:
                mini_map.append(j)
            map_holder.append(mini_map)
            mini_map = []

        #FIXME MAKE IT SO THE SHELTER CANNOT BE PLACED ON A RIVER EITHER
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
                        elif map_holder[length_coordinate-1][width_coordinate-1] == "R" or "W":
                             # FIXME MAKE MORE EFFICIENT
                            return False
                    else:
                        return False
                    width_coordinate = width_coordinate + 1

                length_coordinate = length_coordinate + 1
                width_coordinate = width_coordinate - j
            #print(x_coordinate, y_coordinate)
        self.map = map_holder
        return True



    def place_rivers(self):

        mini_map_river = []
        map_holder_river = []
        for i in self.map:
            for j in i:
                mini_map_river.append(j)
            map_holder_river.append(mini_map_river)
            mini_map_river = []


        print(self.river_presence)
        if self.river_presence == True:
            # first, a flat accross river. no slope, just going across until
            print(self.river_length, self.river_width)
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

"**********************************************************************************************************************"
class plant:  #FIXME starting with just one species and assuming that all animals can eat it, add impact of temperature, seasons, etc
    # FIXME add light
    def __init__(self, width, average_height, weekly_growth, weekly_water_needs, nutrient_needs, minimum_height, number_seeds, seed_distribution, cover_provided):
        self.alive = True
        self.width = random.randint(5*width, 15*width)/10
        self.height = random.randint(75 * average_height, 125 * average_height)/100
        self.weekly_growth_average = weekly_growth
        #self.density = density # number of plants per square foot  # mayve do this in a more metal place????
        self.water_needs = random.randint(9*weekly_water_needs, 11*weekly_water_needs)/10
        self.nutrient_needs = nutrient_needs
        self.minimum_height = random.randint(75*minimum_height, 125*minimum_height)/100
        pollinated = random.randint(0,1)
        if pollinated == 1:
            self.pollinated = True
        else:
            self.pollinated = False
        self.number_seeds = random.randint(75*number_seeds, 125*number_seeds)/100
        self.seed_distribution = random.randint(5*seed_distribution, 15*seed_distribution)/10
        self.cover_provided = cover_provided*((self.width*self.height)/100)  # percent cover provided per inch of height
        self.water_log = []        # currently on a two week set up, make variable later.
        self.nutrient_log =[]
        self.drought_status = False


    def growth(self, day):  # done at the end of each week
        counter = 0
        print(self.water_log)
        for i in range(day-7, day):
            #print(i)
            n = self.water_log[i]
            #print(n)
            counter = counter + n
       # print("counter", counter)
       # print(self.water_needs)
        weekly_water = counter
        if self.drought_status == True:  # did not get enough water last week
            if weekly_water < self.water_needs:  # not enough water for 2 weeks in a row, dead
                self.alive = False
                #print("1")
            else:
                self.drought_status = False  # enough water, growth
                growth =  random.randint(75*self.weekly_growth_average, 125*self.weekly_growth_average)/100
                print("growth", growth)
                self.height = self.height + growth /2
                self.width = self.width + growth /2
                #print("2")
        else:  # not currently in a state of drought
            if weekly_water < self.water_needs:  # not enough water, into drought
                self.drought_status = True
                #print("3")
            else:
                self.drought_status = False    # enough water, growth
                growth = random.randint(75 * self.weekly_growth_average, 125 * self.weekly_growth_average) / 100
                print(growth)
                self.height = self.height + growth / 2
                self.width = self.width + growth / 2
                # print("4")
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
"**********************************************************************************************************************"
def create_creatures():
    my_creatures = []
    for i in range(50):
        my_creatures.append(species(80,10,150,20,8,1,3,[], ["rabbit"],100,100,100,100,100,100,100,100,100))
    #for animal in my_creatures:
       # animal.print()
       # print("******************")
"**********************************************************************************************************************"
def create_habitat():
    yes = habitat(2000,10,5, [True,10,2], 100,100,80,40,20,10)
    yes.create_map()
    yes.place_rivers()


    yes.create_random_shelter_units()
    yes.space_clump_sizes()

    while yes.check_if_available() == False:
        yes.check_if_available()

    print(yes.map)
"**********************************************************************************************************************"
def make_weather():
    weather1 = weather(50, 2, 90)
    #weather1.daily_weather()
    daily_weather = []
    for i in range(7):
        daily_weather.append(weather1.daily_weather())
    return daily_weather

"**********************************************************************************************************************"
def make_plants():
    plant1 = plant(6,8,1,2,90,2,12,30,8)
    plant1.water_log = make_weather()
    print("hre", plant1.height, plant1.width)
    plant1.growth(7)
    print(plant1.height, plant1.width)
"**********************************************************************************************************************"

def main():
    #create_creatures()
   # create_habitat()
    #make_weather()
    make_plants()



main()






