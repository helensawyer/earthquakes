# The Python standard library includes some functionality for communicating
# over the Internet.
# However, we will use a more powerful and simpler library called requests.
# This is external library that you may need to install first.
import requests
import json
import datetime
import math
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

def get_data():
    # With requests, we can ask the web service for the data.
    # Can you understand the parameters we are passing here?
    response = requests.get(
        "http://earthquake.usgs.gov/fdsnws/event/1/query.geojson",
        params={
            'starttime': "2000-01-01",
            "maxlatitude": "58.723",
            "minlatitude": "50.008",
            "maxlongitude": "1.67",
            "minlongitude": "-9.756",
            "minmagnitude": "1",
            "endtime": "2018-10-11",
            "orderby": "time-asc"}
    )

    # The response we get back is an object with several fields.
    # The actual contents we care about are in its text field:
    text = response.text
    
    # To understand the structure of this text, you may want to save it
    # to a file and open it in VS Code or a browser.
    # See the README file for more information.
    #json_object=json.dumps(text)
    quakes_dict = json.loads(text)
    with open("earthquake.json","w") as outfile:
        #outfile.write()
        json.dump(quakes_dict, outfile)
    #json.dumps()
    #print(response.url)

    # We need to interpret the text to get values that we can work with.
    # What format is the text in? How can we load the values?
    return quakes_dict

quakes_dict=get_data()
#print(response)

def count_earthquakes(data):
    """Get the total number of earthquakes in the response."""
    return data["metadata"]["count"]
#print(count_earthquakes(response))

def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""
    return earthquake["properties"]["mag"]


def get_location(earthquake):
    """Retrieve the latitude and longitude of an earthquake item."""
    coordinates = earthquake["geometry"]["coordinates"]
    # There are three coordinates, but we don't care about the third (altitude)
    return (coordinates[0], coordinates[1])


def get_maximum(data):
    """Get the magnitude and location of the strongest earthquake in the data."""
    current_max_magnitude = get_magnitude(data["features"][0])
    current_max_location = get_location(data["features"][0])
    for item in data["features"]:
        magnitude = get_magnitude(item)
        # Note: what happens if there are two earthquakes with the same magnitude?
        if magnitude > current_max_magnitude:
            current_max_magnitude = magnitude
            current_max_location = get_location(item)
    return current_max_magnitude, current_max_location
    # There are other ways of doing this too:
    # biggest_earthquake = sorted(data["features"], key=get_magnitude)[0]
    # return get_magnitude(biggest_earthquake), get_location(biggest_earthquake)
    # Or...
    # biggest_earthquake = max(
    #     ({"mag": get_magnitude(item), "location": get_location(item)}
    #     for item in data["features"]),
    #     key=lambda x: x["mag"]
    # )
    # return biggest_earthquake["mag"], biggest_earthquake["location"]



# # With all the above functions defined, we can now call them and get the result
data = get_data()
print(f"Loaded {count_earthquakes(data)}")
max_magnitude, max_location = get_maximum(data)
print(f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}")

start_time=datetime.datetime(1970,1,1)

def ms_to_date(date_num):
    days_data=math.floor(date_num/(1000*3600*24))
    return (start_time+datetime.timedelta(days=days_data)).year

#print(ms_to_date(data["features"][0]["properties"]["time"]))

years=[ms_to_date(data["features"][elem]["properties"]["time"]) for elem in range(0,count_earthquakes(data))]
#print(years)

#year_list=list(Counter(years).keys()) + [2012]
#year_freqs=list(Counter(years).values())+[0]
#year_data=np.sort([year_list,year_freqs],1)
#print(year_data)
counter_years=Counter(years)

#plt.bar(year_list, year_freqs)
# plt.bar(counter_years.keys(),list(counter_years.values()))
# plt.show()

mags=[(ms_to_date(data["features"][elem]["properties"]["time"]),get_magnitude(elem)) for elem in range(0,count_earthquakes(data))]
print(mags)