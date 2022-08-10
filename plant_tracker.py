import datetime
import time


def get_plants(plants):
    for plant in plants:
        plant.split(" ")
        plant_list = list(plant.split())

        today = datetime.datetime.now()
        with open('date.txt', 'w') as date_file:
            date_file.write(f"{today}")
        datetime_watered = datetime.datetime.strptime(plant_list[3], "'%Y-%m-%d'")
        datetime_fertilized = datetime.datetime.strptime(plant_list[4], "'%Y-%m-%d'")
        delta_water = abs(today - datetime_watered)
        delta_fertilized = abs(today - datetime_fertilized)
        water_interval = int(plant_list[1])
        fertilize_interval = int(plant_list[2])

        if delta_water.days >= water_interval:
            plant = plant_list[0]
            print(f"Plants that need watered today: {plant}")
            with open('water.txt', 'a') as water_file:
                water_file.write(f"{plant}\n")

        if delta_fertilized.days >= fertilize_interval:
            plant = plant_list[0]
            print(f"Plants that need fertilized today: {plant}")
            with open('fertilizer.txt', 'a') as fert_file:
                fert_file.write(f"{plant}\n")
        open('run.txt', 'w').close()


def main():
    print('listening')
    while True:
        time.sleep(1)
        file = open("run.txt", "r")
        text = file.readline()
        file.close()

        if text == "run\n":
            file = open('schedule.txt', 'r')
            text = file.readlines()
            plants = []
            for i in text:
                plants.append(i.rstrip())
            file.close()
            get_plants(plants)


if __name__ == '__main__':
    main()