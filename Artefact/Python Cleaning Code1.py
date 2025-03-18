#This is the start of my computer Science project 12/12/2024

#Here I import Firebase and initilise it
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import pandas as pd
import numbers

#Here I extract the data from my CSV File
df = pd.read_csv("C:\\Users\\20JPiwosz.ACC\\Downloads\\OneDrive_2025-03-12\\F1 LEAVING CERT PROJECT MOST UPDATED VERSION\\F1Drivers_Dataset.csv", encoding='utf-8')
print(df)

#HERE I MAKE ALL COLUMNS IN MY DATASET UPERCASE
df.columns = df.columns.str.upper()
print(df.info())

# Drivers_Data = df[['DRIVER']].copy()
# print(Drivers_Data)

#Here I check if there is any missing information in my data
print(df.isnull().any()) #Prints any missing values in the Driver column that are missing

# Drivers_Missing = df[Drivers_Data.isna().any(axis=1)]
# print(Drivers_Missing)

#Here I fill any missing drivers with the name "Unknown"
df['DRIVER'] = df['DRIVER'].fillna('Unknown')

#Here I fill the champion ship columns for any drivers who have not won a champion ship with "No ChampionShip Won"
df['CHAMPIONSHIP YEARS']= df['CHAMPIONSHIP YEARS'].fillna('No ChampionShip Won')

# Drivers_Missing = df[df.isna().any(axis=1)]
# print(Drivers_Missing)

#Here I replace all instances of RAF In nationalities with Russia
df['NATIONALITY'].replace('RAF','Russia', inplace=True)

#df['DRIVER'].replace("Carlos Sainz Jr.","Carlos Sainz Jr", inplace=True)

#df['DRIVER'].replace(to_replace=pattern1, value='Germany', regex=True, inplace=True)  look AT THIS LATER

#Here i define paterns of what I want to replace things with
pattern1 = r'.*Germany'
pattern2 = r'Belgium.*France'
pattern3 = r'.*Netherlands'
pattern4 = r'.*Rhodesia.*'
parern5 = r'\.*'
#df.replace(r'(.*),\s+(.*)', r'\2 \1', inplace=True, regex=True)
#print("-------------------------------------------------")
#print(df['DRIVER'])
df['DRIVER'].replace("Carlos Sainz Jr.","Carlos Sainz Jr", inplace=True, regex=True)
#print(df['DRIVER'])
#print("-------------------------------------------------")

#Here i replace any invalid data with the country that they belong to 
#For example I replace east germany and west germany to just simply germany 
df['NATIONALITY'].replace(to_replace=pattern1, value='Germany', regex=True, inplace=True)
df['NATIONALITY'].replace(to_replace=pattern2, value='Belgium', regex=True, inplace=True)
df['NATIONALITY'].replace(to_replace=pattern3, value='Netherlands', regex=True, inplace=True)
df['NATIONALITY'].replace(to_replace=pattern4, value='Rhodesia', regex=True, inplace=True)

# ChampionShip_Years_Data = df[['CHAMPIONSHIP YEARS']].copy()
# print(ChampionShip_Years_Data)
# #df['Championship Years'] = 
# df['CHAMPIONSHIP YEARS'].fillna('No ChampionShip Won')

#prints the first 20 lines of the driver column.
print(df['DRIVER'].head(20))
print(df['CHAMPIONSHIP YEARS'].head(20))
#ChampionShip_Years_Data = df[df.isna().any(axis=1)]
# print(ChampionShip_Years_Data)
df.to_csv('cleaned file.csv',  encoding='utf-8', index=False)
# for index, row in ChampionShip_Years_Data.iterrows():
#     if index <20:
#       print(row["CHAMPIONSHIP YEARS"])
#print('here')
df.index = df.index.map(str)
#Here i define the data that i want to send to firebase
Data_For_FireBase = df.to_dict()
#print('now here')
#print(Data_For_FireBase)
print(df['DRIVER'].head(20))

#Here i set my credentials so that I can write to firebase
cred = credentials.Certificate("lc-230655-firebase-adminsdk-fbsvc-0a2650447e.json")
firebase_admin.initialize_app(cred, {'databaseURL':'https://lc-230655-default-rtdb.europe-west1.firebasedatabase.app/'})

#databaseReference

#HERE I DROP THE COLUMNS I WONT BE USING
df = df.drop(df.columns[[14, 15, 16, 17, 18]],axis = 1)
print(df.info())


#reference the root node of the database

#Here i send my information to Firebase
for branch, childData in Data_For_FireBase.items():
    print(branch)
    ref = db.reference('/'+branch)
    for idx, val in childData.items():
        ref.update({'*'+str(idx):val})


      
#ref.set(Data_For_FireBase) #set puts the data at the ref location. It deletes any other data at that location

