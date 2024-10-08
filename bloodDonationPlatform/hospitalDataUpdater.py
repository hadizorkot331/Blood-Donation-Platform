"""
Uses MOPH website, Google Places API, and Gooogle Place Details API to gather the needed location and contact information
of all hospitals in Lebanon.

This data is read into a pickle file which is used later by the views

We used this approach instead of making the api calls when necessary due to the following reasons:
    - All our needed information is limited to ~150 hospitals which repeat throughout all posts
        since they are the only hospitals in lebanon.
    - The data accessed is mostly constant and not subject to change. Locations and contact information of hospitals
        almost never change therefore the information is again repeated
    - Making api calls would add ~3 seconds of delay on average on the less than ideal Lebanese internet. In a
        service where urgency is the primary focus, such easily avoidable latency should be avoided


"""

import requests
import pickle
import pandas as pd
import dotenv
import os

dotenv.load_dotenv(dotenv_path="./bloodDonationPlatform/.env")

fields = ",".join(
    [
        "name",
        "business_status",
        "formatted_address",
        "place_id",
        "plus_code",
        "url",
        "vicinity",
        "current_opening_hours",
        "formatted_phone_number",
        "international_phone_number",
        "opening_hours",
        "website",
    ]
)

API_KEY = os.getenv("GOOGLE_API_KEY")
HOSPITALS = []
HOSPITAL_CAZAS = {}
HOSPITAL_LOCATION_DATA = {}

list_of_tables = []

# Private Hospitals
for i in range(1, 6):
    url = f"https://www.moph.gov.lb/en/HealthFacilities/index/3/188/8/%D8%A7%D9%84%D9%85%D9%86%D8%B4%D8%A2%D8%AA-%D8%A7%D9%84%D8%B5%D8%AD%D9%91%D9%8A%D8%A9/page:{i}"
    tables = pd.read_html(url)
    list_of_tables.append(tables)

# Governmental hospitals
for i in range(1, 3):
    url = f"https://www.moph.gov.lb/en/HealthFacilities/index/3/188/1/page:{i}&facility_type=1"
    tables = pd.read_html(url)
    list_of_tables.append(tables)


for tables in list_of_tables:
    hospitals = tables[0].to_dict()

    names = hospitals["Name"].values()

    for name in names:
        query = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={name}&key={API_KEY}"
        place_id = requests.get(query).json()["results"][0]["place_id"]
        detailed_query = f"https://maps.googleapis.com/maps/api/place/details/json?fields={fields}&place_id={place_id}&key={API_KEY}"
        detailed_json_data = requests.get(detailed_query).json()
        result = detailed_json_data["result"]
        HOSPITAL_LOCATION_DATA[name] = result

    cazas = list(map(str.title, hospitals["Caza"].values()))

    HOSPITALS.extend(names)

    HOSPITAL_CAZAS.update(dict(zip(names, cazas)))


CAZAS = set(map(str.title, HOSPITAL_CAZAS.values()))
HOSPITALS.sort()

data = {
    "HOSPITAL_CAZAS": HOSPITAL_CAZAS,
    "HOSPITALS": HOSPITALS,
    "CAZAS": CAZAS,
    "HOSPITAL_LOCATION_DATA": HOSPITAL_LOCATION_DATA,
}

with open("hospital_data_with_maps.pickle", "wb") as p:
    pickle.dump(data, p, pickle.HIGHEST_PROTOCOL)
