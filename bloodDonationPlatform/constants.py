"""
Loads constants from pickle file and creates necessary constants such as blood mappings
"""

import pickle

BLOOD_TYPES = [
    ("A+", "A+"),
    ("A-", "A-"),
    ("B+", "B+"),
    ("B-", "B-"),
    ("O+", "O+"),
    ("O-", "O-"),
    ("AB+", "AB+"),
    ("AB-", "AB-"),
]

DONORS_TO_RECIPIENTS = {
    "O-": ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"],
    "O+": ["O+", "A+", "B+", "AB+"],
    "A-": ["A-", "A+", "AB-", "AB+"],
    "A+": ["A+", "AB+"],
    "B-": ["B-", "B+", "AB-", "AB+"],
    "B+": ["B+", "AB+"],
    "AB-": ["AB-", "AB+"],
    "AB+": ["AB+"],
}

DONORS_OF = {
    "O-": ["O-"],
    "O+": ["O-", "O+"],
    "A-": ["O-", "A-"],
    "A+": ["O-", "O+", "A-", "A+"],
    "B-": ["O-", "B-"],
    "B+": ["O-", "O+", "B-", "B+"],
    "AB-": ["O-", "A-", "B-", "AB-"],
    "AB+": ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"],
}


with open("../bloodDonationPlatform/hospital_data_with_maps.pickle", "rb") as p:
    data = pickle.load(p)

HOSPITALS = data["HOSPITALS"]
CAZAS = data["CAZAS"]

# Django forms require choices to be in this format
HOSPITALS_AS_CHOICES = [(HOSPITAL, HOSPITAL) for HOSPITAL in HOSPITALS]
CAZAS_AS_CHOICES = [(CAZA, CAZA) for CAZA in CAZAS]

HOSPITAL_CAZAS = data["HOSPITAL_CAZAS"]
HOSPITAL_LOCATION_DATA = data["HOSPITAL_LOCATION_DATA"]

CAZA_HOSPITALS = {}
for hospital, caza in HOSPITAL_CAZAS.items():
    if caza in CAZA_HOSPITALS:
        CAZA_HOSPITALS[caza].append(hospital)
    else:
        CAZA_HOSPITALS[caza] = [hospital]
