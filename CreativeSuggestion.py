import random
import numpy as np
import geocoder
import time 
import sys 
from Weatherin import Weather
from googletrans import Translator
from IndexChecka import findIndex

#Welcome message with weather inputs
print("Welcome to the suggestion program!\nThis program will suggest you things to do based on your mood and the weather outside.\n")

#Weather API and weather inputs that returns humidity, weather description, temperature and feels like temperature
def Weather(cityy):
    import requests
    api_key = "4f609b898d660d4ef8740b763a13a636"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + cityy
    response = requests.get(complete_url)
    x = response.json()
    if x["cod"] != "404":
        y = x["main"]
        temp = round((y["temp"]-275.15))
        tempFeels = round((y["feels_like"]-275.15))
        humidity = str(y["humidity"])+"%"
        z = x["weather"]
        weather_desc = z[0]["description"]
        return humidity, weather_desc, temp, tempFeels 
    else:
        return print(" City Not Found ")

#city API that finds current city and calls the weather function with city as input
city = str(geocoder.ip("me"))
city = city[24:].split(',')[0]
humidity, weather_desc, temp, tempFeels = Weather(city)

#Weighting function that changes the probability of a suggestion based on the temperature
def Weighting(Dg):
    Dg = int(Dg)
    Ms = 100-2*Dg
    Rd = 100-((2*Dg)//2)
    Cd = 100-((2*Dg)//4)
    Cl = 100-(1.25*Dg)
    Mg = 100
    Md = 100-((2*Dg)//5)
    Yg = 100-((2*Dg)//5)
    Ch = 100+(2*Dg)
    Pl = 100-(2*Dg)
    return Ms, Rd, Cd, Cl, Mg, Md, Yg, Ch, Pl

Ms, Rd, Cd, Cl, Mg, Md, Yg, Ch, Pl = Weighting(temp)
WeightList = [Ms, Rd, Cd, Cl, Mg, Md, Yg, Ch, Pl]

print("Loading:")

#Loading animation from 0-100%
animation = ["[■□□□□□□□□□] 10%","[■■□□□□□□□□] 20%", "[■■■□□□□□□□] 30%", "[■■■■□□□□□□] 40%", "[■■■■■□□□□□] 50%", "[■■■■■■□□□□] 60%", "[■■■■■■■□□□] 70%", "[■■■■■■■■□□] 80%", "[■■■■■■■■■□] 90%", "[■■■■■■■■■■] 100%"]

for i in range(len(animation)):
    time.sleep(0.1)
    sys.stdout.write("\r" + animation[i % len(animation)])
    sys.stdout.flush()
print('Complete!')
print("\n")

#Checks temperature to see if the activities should be outdoor or indoor
if temp > 10:
    resp = "It is quite warm outisde, let's find some nice outdoor activities"
elif 0 < temp < 10:
    resp = "It is somewhat cold today, let's look for both indoor and outdoor activities"
else:
    resp = "It is quite cold today, let's find some nice indoor activities"

print("It is currently {} and {} in humidity[0-100], and around {}°C in {}, but it feels like {}°C. {}.".format(weather_desc, humidity, temp, city, tempFeels, resp))

#2D numpy array of suggestions
Data = np.array([["Work on music / beats"], 
        ["Read", "the bible", "the Lord of the Rings", "When", "Ketamine for TR-D", "Metazoa", "a new book"],
        ["Code a program that", 'measures the degree of variation in your diet', 'measures the time you have spent at a website', 'is a simple shooter game', 'can chat with you'],
        ["Clean your room"],
        ["Message or call", "Johanne", "Pappa", "Mamma", "Dom", "Emilie", "Eirik", "Sindre", "Ingvild", "André","Henrik"],
        ["Meditate"],
        ["Do yoga"],
        ["Do a challenge like", "an extreme morning routine", "ice cold shower or swim", "running a 10km", "extreme workout"],
        ["Play", "BO4", "CODM", "Vallheim", "Chess", "AmongUs", "CODM Warzone"]], dtype = object)


#Loop that randomly selects one of the items in the list and removes previously selected items
inp = "B"
tot = 8

while inp != "Done":
    num = random.choices(Data[:], weights = WeightList)
    main = str(num[0][0])
    idx = findIndex(Data,main)
    if len(num[0]) > 1:
        num2 = random.randint(1,len(Data[idx])-1)
        Subs = Data[idx][num2]
        print("\nSuggestion: {} {}\n".format(main,Subs))
        inp == input("Are you satisfied with the suggestion? If yes, type 'Done', if not, press any other key. ")
        Data[idx].pop(num2)
        if len(num[0]) == 1:
            Data = np.delete(Data, idx)
            WeightList = np.delete(WeightList, idx)
    else:
        print("\nSuggestion: {}\n".format(main))
        inp == input("Are you satisfied with the suggestion? If yes, type 'Done', if not, press any other key. ")
        Data = np.delete(Data, idx)
        WeightList = np.delete(WeightList, idx)
    if inp == "Done":
        break
    if Data.size == 0:
        print("You have no more suggestions")
        break
    tot = len(Data)-1

