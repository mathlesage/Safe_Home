import csv
from collections import defaultdict
from math import radians, cos, sin, sqrt, atan2

# Calcul de la distance entre deux coordonnées géographiques (Haversine formula)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Rayon de la Terre en kilomètres
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# Lecture du fichier CSV et regroupement par heure de rentrée
def group_people_by_time_and_proximity(file_path, max_distance_km=1.0):
    groups = defaultdict(list)

    # Lecture des données du fichier CSV
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        people = list(reader)

    # Groupement par heure de rentrée
    for person in people:
        key = person["Heure de rentrée"]
        person_data = {
            "Nom": person["Nom"].strip(),
            "Prénom": person["Prénom"].strip(),
            "Adresse": person["Adresse"].strip(),
            "Latitude": float(person["Latitude"]) if person["Latitude"] else None,
            "Longitude": float(person["Longitude"]) if person["Longitude"] else None,
            "Rentre en voiture": person["Rentre en voiture"].strip(),
        }
        groups[key].append(person_data)

    # Filtrage par proximité géographique
    final_groups = defaultdict(list)
    for time, people_at_time in groups.items():
        while people_at_time:
            person = people_at_time.pop(0)
            group = [person]

            for other in people_at_time[:]:
                if person["Latitude"] is not None and person["Longitude"] is not None:
                    if other["Latitude"] is not None and other["Longitude"] is not None:
                        distance = haversine(
                            person["Latitude"], person["Longitude"],
                            other["Latitude"], other["Longitude"]
                        )
                        if distance <= max_distance_km:
                            group.append(other)
                            people_at_time.remove(other)

            final_groups[time].append(group)

    return final_groups

# Exemple d'utilisation
file_path = "chemin_vers_votre_fichier.csv"
grouped_people = group_people_by_time_and_proximity(file_path)

# Affichage des résultats
for time, groups in grouped_people.items():
    print(f"\nHeure de rentrée : {time}")
    for i, group in enumerate(groups, 1):
        print(f"  Groupe {i}:")
        for person in group:
            print(f"    {person['Nom']} {person['Prénom']} - {person['Adresse']}")
