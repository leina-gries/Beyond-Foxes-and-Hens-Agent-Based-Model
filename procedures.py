from main import *


"**********************************************************************************************************************"

"********************************************    PROCEDURES    ********************************************************"

"**********************************************************************************************************************"
def create_creatures(number, map):
    my_creatures = []
    for i in range(number):
        my_creatures.append(species(map,80,10,150,20,8,1,3,[], ["P"],5,10,100,100,100,100,100,100,100, True, False))
    return my_creatures
    #for animal in my_creatures:
       # animal.print()
       # print("******************")


def daily_movements(creature, map):
    # print(creature)
    print("width", map.width)
    print("length", map.length)
    for i in range(int(creature.range)):
        print("my range is", creature.range)
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
        creature.eat()


        #creature.step(random.randint(-1,1), random.randint(-1,1))
        #print(creature.location)


"**********************************************************************************************************************"
def create_habitat(plants):
    yes = habitat(200,10,5, [True,10,2], 100,100,80,40,20,10)
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
    daily_weather = []
    for i in range(7):
        daily_weather.append(weather1.daily_weather())
    return daily_weather

"**********************************************************************************************************************"
def make_plants():
    my_plants = []
    for i in range(50):
        my_plants.append(plant(6,8,1,2,90,2,12,30,8))
    #for i in my_plants:
   #    print(i)

   # plant1.water_log = make_weather()
   # print("hre", plant1.height, plant1.width)
   # plant1.growth(7)
    return my_plants
"**********************************************************************************************************************"

def main():
    #create_creatures()
    plants = make_plants()
    for i in plants:
        print(i.alive)
    map = (create_habitat(plants))

   # for i in rabbits:
   #     i.print()

    rabbits = create_creatures(20, map)
    for day in range(5):
        for animal in rabbits:
            daily_movements(animal, map)
            print("starting new animal")
    for animal in rabbits:
        print("this one!!!!", animal.food_history)

    for i in plants:
        print(i.alive)
    #make_weather()
    #print("test")



main()






