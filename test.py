from geopy.geocoders import Nominatim

# Adresse
adresse = "39 rue des galardières Cesson-Sévigné, France"
addresse2 = "1 rue des galardières Cesson-Sévigné, France"
# Initialisation du géocodeur
geolocator = Nominatim(user_agent="geoapi")

# Géocodage
location = geolocator.geocode(adresse)
location2 = geolocator.geocode(addresse2)
# Résultat

if location:
    print(f"Latitude: {location.latitude}, Longitude: {location.longitude}")
else:
    print("Adresse introuvable.")


from math import radians, sin, cos, sqrt, atan2

def haversine(lat1, lon1, lat2, lon2):
    # Rayon de la Terre en kilomètres
    R = 6371.0

    # Conversion des coordonnées en radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Différences des coordonnées
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Formule de Haversine
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Distance en kilomètres
    distance = R * c
    return distance

# Exemple de coordonnées (latitude, longitude)
coord1 = (location.latitude, location.longitude)# Exemple : 39 rue des galardières, Cesson-Sévigné
coord2 = (location2.latitude, location2.longitude)  # Exemple : Tour Eiffel, Paris

# Calcul de la distance
distance_km = haversine(coord1[0], coord1[1], coord2[0], coord2[1])
print(f"La distance entre les deux points est de {distance_km:.2f} km.")
