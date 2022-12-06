# Import the required library
#def LongLat(city):
#    from geopy.geocoders import Nominatim
#    geolocator = Nominatim(user_agent="MyApp")
#    location = geolocator.geocode(city)
#    Lat, Long = location.latitude, location.longitude
#    return Lat, Long

def Weather(city):
    import requests
    api_key = "4f609b898d660d4ef8740b763a13a636"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    # complete_url variable to store
    # complete url address
    complete_url = base_url + "appid=" + api_key + "&q=" + city
    response = requests.get(complete_url)
    # json method of response object
    # convert json format data into
    # python format data
    x = response.json()
    # Now x contains list of nested dictionaries
    # Check the value of "cod" key is equal to
    # "404", means city is found otherwise,
    # city is not found
    if x["cod"] != "404":
        y = x["main"]
        temp = round((y["temp"]-275.15),2)
        tempFeels = round((y["feels_like"]-275.15),2)
        humidity = y["humidity"]
        z = x["weather"]
        weather_desc = z[0]["description"]
        return humidity, weather_desc, temp, tempFeels 
    else:
        return print(" City Not Found ")

print(Weather("Oslo"))