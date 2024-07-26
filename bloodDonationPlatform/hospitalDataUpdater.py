from django.conf import settings
import requests
import pickle
import pandas as pd

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
        "widget_tweaks",
    ]
)
API_KEY = settings.GOOGLE_API_KEY
HOSPITLAS = []
HOSPITAL_CAZAS = {}
HOSPITAL_LOCATION_DATA = {}

for i in range(1, 6):
    url = f"https://www.moph.gov.lb/en/HealthFacilities/index/3/188/8/%D8%A7%D9%84%D9%85%D9%86%D8%B4%D8%A2%D8%AA-%D8%A7%D9%84%D8%B5%D8%AD%D9%91%D9%8A%D8%A9/page:{i}"
    tables = pd.read_html(url)
    hospitals = tables[0].to_dict()

    names = hospitals["Name"].values()

    for name in names:
        query = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={name}&key={API_KEY}"
        place_id = requests.get(query).json()["results"][0]["place_id"]
        detailed_query = f"https://maps.googleapis.com/maps/api/place/details/json?fields={fields}&place_id={place_id}&key={API_KEY}"
        detailed_json_data = requests.get(detailed_query).json()
        result = detailed_json_data["result"]
        HOSPITAL_LOCATION_DATA[name] = result

    cazas = hospitals["Caza"].values()

    HOSPITLAS.extend(names)

    HOSPITAL_CAZAS.update(dict(zip(names, cazas)))

CAZAS = set(HOSPITAL_CAZAS.values())

data = {
    "HOSPITAL_CAZAS": HOSPITAL_CAZAS,
    "HOSPITALS": HOSPITLAS,
    "CAZAS": CAZAS,
    "HOSPITAL_LOCATION_DATA": HOSPITAL_LOCATION_DATA,
}

with open("hospital_data_with_maps.pickle", "wb") as p:
    pickle.dump(data, p, pickle.HIGHEST_PROTOCOL)
