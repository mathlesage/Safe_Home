import requests

def get_coordinates(address):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": address,
        "format": "json",
        "limit": 1  # On limite les résultats à 1 pour ne pas avoir plusieurs coordonnées
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data:
            lat = data[0]["lat"]
            lon = data[0]["lon"]
            return float(lat), float(lon)
        else:
            return "Address not found!"
    else:
        return f"Error: {response.status_code}"

# Exemple d'utilisation
address = "Tour Eiffel, Paris, France"
coordinates = get_coordinates(address)
if isinstance(coordinates, tuple):
    print(f"Latitude: {coordinates[0]}, Longitude: {coordinates[1]}")
else:
    print(coordinates)
print(get_coordinates("39 Rue des Galardières 35510 Cesson-Sévigné"))



