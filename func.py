import os 
import json 
import requests 
from geopy import distance 
import folium 
from dotenv import load_dotenv 
 
 
def fetch_coordinates(api_key, address): 
    base_url = "https://geocode-maps.yandex.ru/1.x" 
    response = requests.get(base_url, params={ 
        "geocode": address, 
        "apikey": api_key, 
        "format": "json", 
    }) 
    response.raise_for_status() 
    found_places = response.json()['response']['GeoObjectCollection']['featureMember'] 
     
    if not found_places: 
        return None 
 
    most_relevant = found_places[0] 
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ") 
    return lon, lat 
 
def get_distance(shop): 
    return shop["distance"] 
 
def main(): 
    load_dotenv("secrets.env") 
    API_KEY = os.getenv("API") 
    coffee_json_path = "coffee.json" 
    output_map_path = "coffee_map.html" 
    
    with open(coffee_json_path, "r", encoding="CP1251") as data_file: 
        coffee_shops = json.load(data_file) 
 
    user_address = input("Где вы находитесь? ") 
    user_coords = fetch_coordinates(API_KEY, user_address) 
    long_user, lat_user = user_coords 
 
    coffee_shop_data = [] 
    for shop in coffee_shops: 
        name = shop['Name'] 
        latitude = float(shop['Latitude_WGS84']) 
        longitude = float(shop['Longitude_WGS84']) 
        shop_distance = distance.distance( 
            (lat_user, long_user), (latitude, longitude)).km 
 
        coffee_shop_data.append({ 
            "title": name, 
            "distance": shop_distance, 
            "latitude": latitude, 
            "longitude": longitude, 
        }) 
 
    nearest_shops = sorted(coffee_shop_data, key=get_distance)[:5] 
 
    coffee_map = folium.Map( 
        location=(float(lat_user), float(long_user)), zoom_start=12) 
 
    for shop in nearest_shops: 
        folium.Marker( 
            location=[shop["latitude"], shop["longitude"]], 
            tooltip=shop["title"], 
            popup=f"{shop['title']}: {shop['distance']:.2f} км", 
            icon=folium.Icon(icon="cloud"), 
        ).add_to(coffee_map) 
 
    coffee_map.save(output_map_path) 
 
if __name__ == "__main__": 
    main()
