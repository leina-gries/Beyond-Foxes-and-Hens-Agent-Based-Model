from main import *


"**********************************************************************************************************************"

"********************************************    PROCEDURES    ********************************************************"

"**********************************************************************************************************************"
def create_creatures(number, map, name):
    my_creatures = []
    for i in range(number):
        my_creatures.append(species(map,80,10,150,20,8,10,3,[], ["P"],5,10,100,100,100,100,100,100,100, True, False, name, 10, False))
    return my_creatures
    #for animal in my_creatures:
       # animal.print()
       # print("******************")



"**********************************************************************************************************************"
def create_habitat(plants):
    yes = habitat(900,10,5, [True,10,2], 100,100,80,40,20,10)
    yes.create_map()
    yes.place_rivers() #FIXME add extra river placement if it is needed


    yes.create_random_shelter_units()
    yes.space_clump_sizes()


    while yes.place_shelter() == False:
        yes.place_shelter()

    yes.check_if_available()
    yes.place_plant_objects(plants)
    yes.check_if_available_for_animal()


    return yes
"**********************************************************************************************************************"
def make_weather():
    weather1 = weather(50, 2, 90)
    #weather1.daily_weather()
    weekly_weather = []
    for i in range(7):
        weekly_weather.append(weather1.daily_weather())
    return weekly_weather

"**********************************************************************************************************************"
def make_plants(number):
    my_plants = []
    for i in range(number):
        my_plants.append(plant(6,8,1,6,90,1,12,30,8,True))
    #for i in my_plants:
   #    print(i)

   # plant1.water_log = make_weather()
   # print("hre", plant1.height, plant1.width)
   # plant1.growth(7)
    return my_plants

"**********************************************************************************************************************"

def animal_day(creature, map):
    # print(creature)
    #print("width", map.width)
    #print("length", map.length)
    for i in range(int(creature.range)):
     #   print("my range is", creature.range)
        length_step = random.randint(-1,1)
        width_step = random.randint(-1,1)
        #print(creature.location)
        if creature.location[0] + length_step > map.length or creature.location[0] + length_step <= 0:
            length_step = length_step * (-1)

        if creature.location[1]+ width_step > map.width or creature.location[1] + width_step <= 0:
            width_step = width_step * (-1)
            #print("test1")
            #print("test2")
        creature.step(length_step, width_step)
        map.species_placement[creature] = creature.location
        for species1, location in map.species_placement.items():
            if creature.location == location and creature != species:
                if creature.name == species1.name:
                    if creature.gender != species1.gender:
                        if creature.gender == "Female":
                            if creature.fertility == True:
                                if creature.pregnancy == False:
                                    # could add in odds of mating success here if wanted
                                    creature.pregnancy = True
                                    creature.gestation_period_remaining = creature.gestation_period
                                    #number_of_offspring = random.randint(int(creature.number_of_offspring/4), creature.number_of_offspring *2)
                                    #for i in number_of_offspring:
                                        #baby_animals = []
                                        #name = creature.name
                                        #baby_animals.append(species(map, 80, 10, 150, 20, 8, 1, 3, [], ["P"], 5, 10, 100, 100, 100, 100, 100, 100, 100, True, False, name, 10, True))


                        if species1.gender == "Female":
                            if species1.fertility == True:
                                if species1.pregnancy == False:
                                    creature.pregnancy = True
                                    creature.gestation_period_remaining = creature.gestation_period
        """
        for animal_location in map.species_placement:
            if creature.location == (map.species_placement[animal_location]):
                print("wow!!!!", creature.location, creature, map.species_placement[animal_location])
        """
        creature.eat()
    if creature.pregnancy == True:
        creature.gestation_period_remaining = creature.gestation_period_remaining - 1
       # print(creature, creature.gestation_period_remaining)
        baby_animals = []
        if creature.gestation_period_remaining == 0:
            number_of_offspring = random.randint(int(creature.number_of_offspring / 4), creature.number_of_offspring * 2)
            list = creature.birth(number_of_offspring)
            for i in list:
                baby_animals.append(i)
            return(baby_animals)
    return 0

            #print(creature, "this one", creature.birth(number_of_offspring))
              #print("babies!!!!!", baby_animals)

    #creature.step(random.randint(-1,1), random.randint(-1,1))
        #print(creature.location)

"**********************************************************************************************************************"
def plant_week(plants, map, weather): #FIXME add sunlight needs
    #for i in plants:
       # print(i.water_needs)
    print(map.map)
    rain_counter = 0
    for i in weather:
        rain_counter = rain_counter + i
    for plant1 in plants:
        if plant1.alive == True:
            #print("new plant")
            #print(plant1.height)
            growth_amount = plant1.growth(rain_counter)
            #print(plant1.height)
            if plant1.pollinated == True:
                #print("seeds", plant1.number_seeds)
                baby_plants = []
                for i in range(plant1.number_seeds):
                    baby_plants.append(plant(3,3,1,6,90,1,12,30,8, False))
                    map.place_plant_objects(baby_plants)
                plant1.pollinated = False
           # print(growth_amount)
            if growth_amount > 0:
                pollination_status = random.randint(0,1)
                if pollination_status == 1:
                    plant1.pollinated = True
            #print(plant1.pollinated)

   # print(map.map)




                    ### then place them on the map somehwere
"**********************************************************************************************************************"


def main():
    plants = make_plants(10)  # making plants
   # for i in plants:
   #     print(i.alive)
    map = (create_habitat(plants))  # making the habitat using the plants
    all_creatures = []
    rabbits = create_creatures(10, map, "rabbit")  # making 20 creatures using the map
    for i in rabbits:
        all_creatures.append(i)

    for i in all_creatures:
        map.species_placement[i] = i.location
    print(len(all_creatures))
    for week in range(3):
        for day in range(7):  # a week
            for animal in all_creatures:
                new_creatures = animal_day(animal, map) # doing the daily movements each day # FIXME add drinking
                # FIXME add plant daily motions ex. growth, reproduction
                if new_creatures != 0:
                    for i in new_creatures:
                        all_creatures.append(i)
        plant_week(plants, map, make_weather())  # plant week
    print(len(all_creatures))
    #print(hi)
          #  print("starting new animal")
   # for animal in rabbits:
    #    print("this one!!!!", animal.food_history)

   # for i in plants:
   #     print(i.alive)
    #make_weather()

    #print("test")



main()






