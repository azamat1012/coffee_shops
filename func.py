import os
import json


import requests
from geopy import distance
import folium
from dotenv import load_dotenv


current_path = os.path.dirname(__file__)

load_dotenv(f"{current_path}/secrets.env")
apikey = os.getenv("API")


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json(
    )['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


def generate_map():
    try:
        with open(f"{current_path}/coffee.json", "r", encoding="CP1251") as data_file:
            file_content = json.load(data_file)
    except Exception as e:
        print(f"Error: {e}")
        return

    coords_A = input("Где вы находитесь? ")
    coords_A = fetch_coordinates(apikey, coords_A)
    long_A, lat_A = coords_A
    all_coffee_shops = []

    for content in file_content:
        name = content['Name']
        latitude = float(content['Latitude_WGS84'])
        longitude = float(content['Longitude_WGS84'])
        total_distance = distance.distance(
            (lat_A, long_A), (latitude, longitude)).km

        coffee_shop_info = {
            "Title": name,
            "Distance": total_distance,
            "latitude": latitude,
            "longitude": longitude,
        }
        all_coffee_shops.append(coffee_shop_info)

    def get_distance(shop):
        return shop["Distance"]

    nearest_shops = sorted(all_coffee_shops, key=get_distance)[:5]
    print(f"Ваши координаты: {coords_A}\n{nearest_shops[:5]}")

    m = folium.Map(location=(float(lat_A), float(long_A)), zoom_start=12)

    for shop in nearest_shops:
        lat = float(shop['latitude'])
        lon = float(shop['longitude'])
        folium.Marker(
            location=[lat, lon],
            tooltip=shop['Title'],
            popup=f"{shop['Title']}: {shop['Distance']:.2f} км",
            icon=folium.Icon(icon="cloud"),
        ).add_to(m)

    try:
        output_file = f"{current_path}/coffee_map.html"
        m.save(output_file)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    generate_map()
