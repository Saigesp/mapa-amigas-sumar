# -*- coding: UTF-8 -*-
import os
import csv
import requests
import random
from pathlib import Path

ADD_ROWS = True

GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'
INPUT_FILE_REPLACE = Path(__file__).resolve().parent / "data" / "data-raw-replace.csv"
INPUT_FILE_ADD = Path(__file__).resolve().parent / "data" / "data-raw-add.csv"
OUTPUT_FILE = Path(__file__).resolve().parent / "data" / "data-geocoded.csv"


def compose_address(row: dict) -> str:
    return (
        f'{row["address"]}, '
        f'{row["city"]}, '
        f'{row["cp"]}, '
        "España"
    )


def get_id(row: dict) -> str:
    return row['id']


def get_link(row: dict) -> str:
    return "https://actionnetwork.org/forms/unete-a-un-grupo-de-amigas-de-sumar?ref=grupo_" + row['id']


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
    write_mode = "a" if ADD_ROWS else "w"
    raw_file = INPUT_FILE_ADD if ADD_ROWS else INPUT_FILE_REPLACE
    with open(raw_file) as inputfile:
        with open(OUTPUT_FILE, write_mode) as outputfile:
            writer = csv.writer(outputfile)
            if not ADD_ROWS:
                writer.writerow(["id", "lng", "lat", "form"])
            reader = csv.DictReader(inputfile)
            for row in reader:
                lat, lng = geocode_address(row)
                writer.writerow([get_id(row), lng, lat, get_link(row)])


if __name__ == "__main__":
    if not os.getenv("GOOGLE_MAPS_API_KEY"):
        raise Exception("GOOGLE_MAPS_API_KEY environment variable not defined")
    parse_data()
