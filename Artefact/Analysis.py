#This is the start of the Analysis
#To Get win rate of all the drivers and make it a new column

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import pandas as pd
import numbers
from firebase_admin import credentials, db
import matplotlib.pyplot as plt

cred = credentials.Certificate("lc-230655-firebase-adminsdk-fbsvc-0a2650447e.json")
firebase_admin.initialize_app(cred, {'databaseURL':'https://lc-230655-default-rtdb.europe-west1.firebasedatabase.app/'})

def get_drivers_from_firebase():
    ref = db.reference('DRIVER')  
    driver_data = ref.get()
    #print('===========================')
    #print(driver_data)
    #print('---------------------------')
    return driver_data

Drivers_Data_List = get_drivers_from_firebase()
print(Drivers_Data_List)
#print(get_drivers_from_firebase())

def get_the_nationalities_of_drivers():
    ref = db.reference('NATIONALITY')
    nationality_data = ref.get()
    return nationality_data

#print(get_the_nationalities_of_drivers())
all_nationalites =  get_the_nationalities_of_drivers()
#print(all_nationalites)

def get_wins():
    ref = db.reference('/RACE_WINS')
    wins_data = ref.get()
    #print(type(wins_data))
    return wins_data

def avg_countries(vals):
    count = 0
    total = 0
    for val in vals:
        count = count + 1
        total += val
    return total / count

def avg_dirvers(vals):
    count = 0
    total = 0
    for val in vals:
        count =  count + 1
        total += val
    return total / count
        
        #wins_by_country.keys
        #wins_by_country.values

Wins_Dict = get_wins()
print(Wins_Dict)
#print(Wins_Dict)

Unique_Nationality_List = []
for i in all_nationalites.values():           # <-------- I put the .values here since all_nationalites is a dictionary and I want to get the value not the keys of this dictionary!
    #print(i)
    if i not in Unique_Nationality_List:
        Unique_Nationality_List.append(i)

#print("-------------------------------------------------------------------------------------",Unique_Nationality_List,len(Unique_Nationality_List))

#print(len(Unique_Nationality_List))

#TO GET EACH COUNTRIES WINS:
Length_of_loop = len(all_nationalites)
#print(Length_of_loop)

Nationality_Reference = db.reference('NATIONALITY')
Win_Reference = db.reference('RACE_WINS')

Country_Data = Nationality_Reference.get()
Win_Data = Win_Reference.get()

#print(Country_Data)

Countries_Wins = {}
for country in Unique_Nationality_List:
    for key,drivers_nationality in all_nationalites.items():
        if country == drivers_nationality:
            if country == 'Germany':
                print(country,'----------------', drivers_nationality, '-------',Wins_Dict[key])
            if country not in Countries_Wins:
                Countries_Wins[country] = Wins_Dict[key]
            else:
                Countries_Wins[country] = Countries_Wins[country]+Wins_Dict[key]
print('Country wins: \n',Countries_Wins)

Drivers_Wins = {}
#print(Drivers_Wins)
for key,driver in Drivers_Data_List.items():
    if driver not in Drivers_Wins:
        Drivers_Wins[driver] = Wins_Dict[key]
    else:
        print("Duplicate Entry")
        #print(driver,key,Wins_Dict[key])

print(Drivers_Wins)

wins_by_country = {}
for country, wins_of_country in Countries_Wins.items():
    if wins_of_country > 0:
        print('Country has more than 0 wins')
        #Countries_with_wins.append(country)
       
        if country not in wins_by_country:
            wins_by_country[country]= wins_of_country
        else:
            wins_by_country[country] = wins_by_country[country] + wins_of_country

    else:
        print('Country has 0 wins and has been disregarded')

#print(Countries_with_wins)
#print(wins_by_country)

Drivers_with_wins = []
wins_by_driver = []
for driver,wins_of_driver in Drivers_Wins.items():
    if wins_of_driver > 0:
        #print('Driver has more than 0 wins')
        Drivers_with_wins.append(driver)
        wins_by_driver.append(wins_of_driver)


Countries = Unique_Nationality_List
#print(Countries)
Wins = list(Countries_Wins.values())
#print(Wins)


#print(wins_by_country)

#BAR CHART 1: WINS OF EACH NATIONALITY
plt.bar(list(wins_by_country.keys()),list(wins_by_country.values()))

plt.ylabel('Wins')
plt.xlabel('Nationalities')
plt.title('Wins by Nationality')

plt.xticks(rotation=45, ha='right')

plt.show()

#-----------------------------------------------------------------------------------------------------------

# plt.clf()
#BAR CHART 2: WINS OF EACH DRIVER
#plt.rc('font', size=100)

# fig, ax = plt.subplots()
print("drivers with wins")
print(Drivers_with_wins)


Drivers_with_wins_save2 = Drivers_with_wins   #REVIEW THIS CODE TO SEE IF CAN OPTIMISE
wins_by_driver_save2 =  wins_by_driver

print("wins by driver")
print(wins_by_driver)

plt.xticks(fontsize=6,rotation=75, ha='right')
plt.bar(Drivers_with_wins,wins_by_driver)

plt.ylabel('Wins')
plt.xlabel('Drivers')
plt.title('Career Wins By Driver')


plt.show()

#-------------------------------------------------------------------------------------------------------------

Drivers_with_wins = []
wins_by_driver = {}

Race_Starts_By_Driver = {}
Driver_WinRate = {}

Races_Started_Sub = 0
Races_Won_Sub = 0

def get_races_started():
    ref = db.reference('RACE_STARTS')
    Races_Raced = ref.get()
    return Races_Raced

Driver_Races_Started = get_races_started() #THIS IS THE DICTIONARY
#print("_______________________________________________________________________________________________________________________________")
#print(Driver_Races_Started)

#print(Drivers_Wins)

for driver,wins_of_driver in Wins_Dict.items():
    if wins_of_driver > 0:
        #print('Driver has more than 0 wins')
        Drivers_with_wins.append(driver)
        wins_by_driver[driver] = wins_of_driver

        #print(driver)
        Race_Starts_By_Driver[driver] = Driver_Races_Started[driver]

        Races_Started_Sub =  Driver_Races_Started[driver]
        Races_Won_Sub = wins_of_driver
        print(Races_Started_Sub)
        print(Races_Won_Sub)
        WinRate = (Races_Won_Sub / Races_Started_Sub) * 100
        WinRate = round(WinRate,2)
        Driver_WinRate[Drivers_Data_List[driver]] = WinRate


#print(Drivers_with_wins)
#print(wins_by_driver)

#print(Driver_WinRate)

#MARRYING DRIVERS_WITH_WINS with WINS_BY_DRIVER TO CREATE A KEY VALUE PAIR DICTIONARY

Wins_By_Driver_Name = {}
#print(Drivers_with_wins_save2)
#print(wins_by_driver_save2)

for i in range(len(Drivers_with_wins_save2)):
    Wins_By_Driver_Name[Drivers_with_wins_save2[i]] = wins_by_driver_save2[i]

print(Wins_By_Driver_Name)

#BAR CHART 3: WIN PERCENTADGE BY DRIVER
# fig, ax = plt.subplots()
plt.plot(list(Driver_WinRate.keys()),list(Driver_WinRate.values()))
plt.ylabel('Win Percentadge')
plt.xlabel('Drivers')
plt.title('Win Percentadge by Driver')

plt.xticks(fontsize=6,rotation=75, ha='right')
plt.show()

average_cunts = avg_countries(wins_by_country.values())
average_cunts = int(average_cunts)
print(average_cunts)

averge_drivers =  avg_dirvers(wins_by_driver.values())
averge_drivers = int(averge_drivers)
print(averge_drivers)

#print("-------------------------------------------------------------")
#print(len(Wins_By_Driver_Name))
#print(Driver_WinRate)


# DATA FOR FIREBASE:
Data_For_Firebase_1 = Driver_WinRate
Data_For_Firebase_2 = wins_by_country
Data_For_Firebase_3 = Wins_By_Driver_Name
Data_For_Firebase_4 = Unique_Nationality_List
Data_For_Firebase_5 = average_cunts
Data_For_Firebase_6 = averge_drivers

# Firebase initialization

ref = db.reference('/'+"DRIVER_WINRATE")
ref.set(Data_For_Firebase_1)

ref = db.reference('/'+"NATIONALITY_WINS")
ref.set(Data_For_Firebase_2)

ref = db.reference('/'+"DRIVER_WINS")
ref.set(Data_For_Firebase_3)

ref = db.reference('/'+"UNIQUE_NATIONALITIES")
ref.set(list(Data_For_Firebase_2.keys()))

ref = db.reference('/'+"AVERAGE_WINS_FOR_COUNTRY")
ref.set({"AVERAGE_WINS_FOR_COUNTRY":Data_For_Firebase_5})

ref = db.reference('/'+"AVERAGE_WINS_FOR_DRIVER")
ref.set({"AVERAGE_WINS_FOR_DRIVER":Data_For_Firebase_6})