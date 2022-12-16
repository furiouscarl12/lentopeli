from geopy import distance
import mysql.connector
import math
import time

connection = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='game',
    user='database',
    password='password',
    autocommit=False
)

airports = []
flight_compare = ""
temp_dest = ""
turns_total = 0
km_total = 0
dist_by_type = {
    "heliport": 100,
    "small_airport": 300,
    "medium_airport": 500,
    "seaplane_base": 100,
    "large_airport": 1000,

}


def get_distance(curr_lat, curr_long, dest_lat, dest_long):
    distance_result = distance.distance([curr_lat, curr_long],
                                        [dest_lat, dest_long]).km
    return distance_result


def generate_random_location():
    sql = "SELECT ident, airport.name as airport_name," \
          "country.name as country_name, type, latitude_deg, longitude_deg " \
          "FROM airport, country WHERE NOT type='closed' " \
          "and airport.iso_country = country.iso_country" \
          " ORDER BY RAND() LIMIT 1;"
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()



def fetch_available_airports(curr_lat, curr_long, type):
    if type in dist_by_type:
        radius_km = dist_by_type[type]
    else:
        raise Exception(f"Airport type '{type}' is invalid.")


    sql = f"""SELECT ident, airport.name, country.name, type, latitude_deg, longitude_deg FROM airport, country
    WHERE 3963.0 * acos((sin(RADIANS({curr_lat})) * sin(RADIANS(latitude_deg))) +
    cos(RADIANS({curr_lat})) * cos(RADIANS(latitude_deg)) *
    cos(RADIANS(longitude_deg) - RADIANS({curr_long}))) * 1.609344 <= {radius_km}
    AND type != 'closed'
    AND ident != '{curr["ident"]}'
    AND country.iso_country = airport.iso_country;"""
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    airports.clear()



def print_available_airports():
    global dest
    for i, airport in enumerate(airports):
        if airport['ident'] == dest['ident']:
            print("Oma päämäärä")

        print(f"{str(i + 1) + ':':<5} {airport['airport_name'][0:43] + ',':<45}"
              f" {airport['type']:<20} {airport['country_name'][0:23]:<25}"
              f" {str(round(get_distance(curr['lat'], curr['long'], airport['lat'], airport['long']), 2)) + ' km':<15}"
              f" {airport['direction']}")

def print_starting_message():
    print(
          f"\n{'Pienistä voit lentää':<35} {dist_by_type['small_airport']} km"
          f"\n{'Keskikokoisista lentokentistä voit lentää':<35} {dist_by_type['medium_airport']} km"
          f"\n{'Isot lentokentät':<35} {dist_by_type['large_airport']} km\n"
          "\n")


def move(index, flight):
    global curr, turns_total, km_total
    turns_total = turns_total + 1
    km_total = km_total + flight
    curr = airports[index]








curr = generate_random_location()
dest = generate_random_location()
dist = get_distance(curr["lat"], curr["long"], dest["lat"], dest["long"])
while curr['ident'] != dest['ident']:
    print(f"\nNykyinen siainti '{curr['airport_name']}', {curr['type']} in {curr['country_name']}"
          f"\nPäämääräsi on '{dest['airport_name']}' in {dest['country_name']}."
          f"\npäämäärä on {dist:.0f} km päässä.")
while dest == curr or (dist > 4000 or dist < 1500):
    dest = generate_random_location()
    dist = get_distance(curr["lat"], curr["long"], dest["lat"], dest["long"])





    input("\nPaina enter jotta voit löytää saatavat lentokentät.")
    fetch_available_airports(curr["lat"], curr["long"], curr["type"])
    print_available_airports()


    index = input("\nKirjoita määränpään index: ")
    while not index.isdigit() or (int(index) >= len(airports) + 1 or int(index) < 1):

    dest_dist = get_distance(curr["lat"], curr["long"], dest["lat"], dest["long"])
    airport_dist = get_distance(curr['lat'], curr['long'], airports[index]['lat'], airports[index]['long'])



    if airport_dist > dest_dist:
        dist *= -1

    move(index, airport_dist)

##print_results()
connection.close()
