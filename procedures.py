from main import *


"**********************************************************************************************************************"

"********************************************    PROCEDURES    ********************************************************"

"**********************************************************************************************************************"
def create_creatures(number, map, name):
    my_creatures = []
    for i in range(number):
        my_creatures.append(species(map,90,0.5,5,2,2,15,3,[], ["P"],10,100,100,100,100,100,100,100,5, True, False, name, 8, False))
    return my_creatures
    #for animal in my_creatures:
       # animal.print()
       # print("******************")



"**********************************************************************************************************************"
def create_habitat(plants):
    yes = habitat(5000,10,20, [True,80,20], 100,100,80,40,20,10)
    yes.create_map()
    yes.place_rivers()


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
    weather1 = weather(80, 4, 90)
    #weather1.daily_weather()
    return weather1

"**********************************************************************************************************************"
def make_plants(number):
    my_plants = []
    for i in range(number):
        my_plants.append(plant(6,10,2,6,90,0.5,12,30,8,True))
    #for i in my_plants:
   #    print(i)

   # plant1.water_log = make_weather()
   # print("hre", plant1.height, plant1.width)
   # plant1.growth(7)
    return my_plants

"**********************************************************************************************************************"
# FIXME TOMORROW MAKE CHECKING IF OTHER CREATURES ARE IN THE SAME PLACE MORE EFFICIENT
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
        #print("pregnant rabbit here ")
        creature.gestation_period_remaining = creature.gestation_period_remaining - 1
       # print(creature, creature.gestation_period_remaining)
        baby_animals = []
        if creature.gestation_period_remaining == 0:
            number_of_offspring = random.randint(int(creature.number_of_offspring / 4), creature.number_of_offspring * 2)
            list = creature.birth(number_of_offspring)
            for i in list:
                baby_animals.append(i)
                #print("new baby")
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
    new_plants = []

    weekly_weather = []
    for i in range(7):
        weekly_weather.append(weather.daily_weather())

    weekly_sun = []
    for i in range(7):
        weekly_sun.append(weather.sun_level_daily)

    #print(map.map)
    rain_counter = 0
    for i in weekly_weather:
        rain_counter = rain_counter + i

    sun_counter = 0
    for i in weekly_sun:
        sun_counter = sun_counter + i
    growth_amount = 0

    for plant1 in plants:
        if plant1.alive == True:
            if sun_counter > weather.average_sun_levels / 20:
            #print("new plant")
            #print(plant1.height)
                growth_amount = plant1.growth(rain_counter)
            #print(plant1.height)
            if plant1.pollinated == True and sun_counter > weather.average_sun_levels / 20:
                new_plants = plant.reproduce(plant1, map)
                #print("seeds", plant1.number_seeds)
           # print(growth_amount)
            if growth_amount > 0:
                pollination_status = random.randint(0,1)
                if pollination_status == 1:
                    plant1.pollinated = True
            #print(plant1.pollinated)
    return new_plants

   # print(map.map)




#MAKE CREATURES ONLY EAT WHEN THEY MUST
#EFFICIENCY
"**********************************************************************************************************************"


def main():
    plants = make_plants(600)  # making plants
   # for i in plants:
   #     print(i.alive)
    map = (create_habitat(plants))  # making the habitat using the plants
    all_creatures = []
    rabbits = create_creatures(20, map, "rabbit")  # making 20 creatures using the map #FIXME make this easier to set up different creatures
    for i in rabbits:
        all_creatures.append(i)

    for i in all_creatures:
        map.species_placement[i] = i.location
    print(len(all_creatures))
    rabbit_history = [len(rabbits)]
    plant_history = [len(plants)]
    for week in range(52):
        print(week, "week")
        for day in range(7):  # a week
            for animal in all_creatures:
                if animal.alive == True:
                    new_creatures = animal_day(animal, map) # doing the daily movements each day # FIXME add drinking
                    if new_creatures != 0:
                        for i in new_creatures:
                            all_creatures.append(i)
                    animal.age_days = animal.age_days + 1
        rabbit_counter = 0
        for i in all_creatures:
            if i.alive == True:
                weekly_food_counter = 0
                for food in i.food_history:
                    weekly_food_counter = weekly_food_counter + food
                #print(weekly_food_counter, i.food_needs)
                #print("total food", i.food_history, weekly_food_counter)
                weekly_water_counter = 0
                for drink in i.water_history:
                    weekly_water_counter = weekly_water_counter + drink
                i.update_status(weekly_food_counter, weekly_water_counter)

            if i.name == "rabbit" and i.alive == True:
                rabbit_counter = rabbit_counter + 1
            else:
                print(i.death_cause)
        rabbit_history.append(rabbit_counter)

        more_plants = plant_week(plants, map, make_weather())  # plant week
        for i in more_plants:
            plants.append(i)
        weekly_plant_counter = 0
        for i in plants:
            if i.alive == True:
                weekly_plant_counter = weekly_plant_counter + 1
            else:
                print(i.death_cause)
        #print("plants", weekly_plant_counter)
        plant_history.append(weekly_plant_counter)

            #print(creature)
    print("done")
    print("plants oberall",plant_history)
    print("animals", rabbit_history)
    #print(hi)
          #  print("starting new animal")
   # for animal in rabbits:
    #    print("this one!!!!", animal.food_history)

   # for i in plants:
   #     print(i.alive)
    #make_weather()

    #print("test")
# fixme make baby creatures dependent on mothers/ make this an option


main()






