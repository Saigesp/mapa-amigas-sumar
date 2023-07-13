# -*- coding: UTF-8 -*-
import os
import csv
import requests
import random
from pathlib import Path


GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'
INPUT_FILE = Path(__file__).resolve().parent / "data" / "data-raw.csv"
OUTPUT_FILE = Path(__file__).resolve().parent / "data" / "data-geocoded.csv"


def compose_address(row: dict) -> str:
    return (
        f'{row["Dirección postal"]}, '
        f'{row["Municipio"]}, '
        f'{row["Provincia"]}, '
        f'{row["Código Postal"]}, '
        "España"
    )

def get_geometry_from_results(response: dict) -> dict:
    empty_result = {"lat": "", "lng": ""}

    if not response.get("status") == "OK":
        return empty_result
    
    for result in response.get("results", []):
        if result.get("geometry") and result["geometry"].get("location"):
            return result["geometry"].get("location")

    return empty_result


def randomize_geometry(geometry: dict) -> dict:
    lat_range = 0.004
    lng_range = 0.006
    if geometry.get("lat") is None or geometry.get("lng") is None:
        return {"lat": "", "lng": ""}

    lat_diff = 0
    while round(lat_diff, 3) == 0:
        lat_diff = random.uniform(lat_range * -1, lat_range)

    lng_diff = 0
    while round(lng_diff, 3) == 0:
        lng_diff = random.uniform(lng_range * -1, lng_range)
    
    return {
        "lat": round(geometry.get("lat") + lat_diff, 7),
        "lng": round(geometry.get("lng") + lng_diff, 7),
    }


def geocode_address(row: dict) -> tuple:
    params = {
        "key": os.getenv("GOOGLE_MAPS_API_KEY"),
        "address": compose_address(row),
        "sensor": "false",
        "region": "es",
    }
    print(params["address"])
    req = requests.get(GOOGLE_MAPS_API_URL, params=params)
    geometry = get_geometry_from_results(req.json())
    geometry = randomize_geometry(geometry)

    return geometry["lat"], geometry["lng"]


def parse_data():
    with open(INPUT_FILE) as inputfile:
        with open(OUTPUT_FILE, "w") as outputfile:
            writer = csv.writer(outputfile)
            writer.writerow(["lng", "lat"])
            reader = csv.DictReader(inputfile)
            for row in reader:
                if not row["Municipio"]:
                    row["Municipio"] = row["Provincia"]
                lat, lng = geocode_address(row)
                writer.writerow([lng, lat])


if __name__ == "__main__":
    if not os.getenv("GOOGLE_MAPS_API_KEY"):
        raise Exception("GOOGLE_MAPS_API_KEY environment variable not defined")
    parse_data()
