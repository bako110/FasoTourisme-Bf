# Exemples d'utilisation de l'API Tourisme Burkina

## 1. Destinations

### Créer une destination
```bash
curl -X POST "http://localhost:8000/api/v1/destinations/" \
  -H "Content-Type: application/json" \
  -d '{
    "nom": "Cascade de Banfora",
    "description": "Une des plus belles cascades du Burkina Faso, offrant des piscines naturelles cristallines",
    "region": "Hauts-Bassins",
    "province": "Cascades",
    "localite": "Banfora",
    "type_destination": "cascade",
    "categorie": ["nature", "randonnée", "photographie"],
    "latitude": 10.6347,
    "longitude": -4.7596,
    "meilleure_saison": ["septembre", "octobre", "novembre"],
    "tarif_entree_fcfa": 2000,
    "acces_securise": true
  }'
```

### Récupérer les destinations par région
```bash
curl -X GET "http://localhost:8000/api/v1/destinations/region/Hauts-Bassins"
```

### Récupérer les meilleures destinations
```bash
curl -X GET "http://localhost:8000/api/v1/destinations/top-rated/?limit=5"
```

## 2. Hôtels

### Créer un hôtel
```bash
curl -X POST "http://localhost:8000/api/v1/hotels/" \
  -H "Content-Type: application/json" \
  -d '{
    "nom": "Hôtel Splendid",
    "description": "Hôtel haut standing au cœur de Ouagadougou avec piscine et restaurant",
    "ville": "Ouagadougou",
    "region": "Kadiogo",
    "adresse": "Avenue Kléber, Ouagadougou",
    "categorie": "haut_standing",
    "nombre_etoiles": 4,
    "nombre_chambres": 50,
    "types_chambres": ["simple", "double", "suite"],
    "tarif_nuit_min_fcfa": 35000,
    "tarif_nuit_max_fcfa": 100000,
    "petit_dejeuner_inclus": true,
    "services": ["wifi", "restaurant", "bar", "piscine", "gym", "spa"],
    "equipements": ["climatisation", "tv", "minibar"],
    "telephone": "+226 70 00 00 00",
    "email": "contact@hotelsplendid.bf"
  }'
```

### Récupérer les hôtels par ville
```bash
curl -X GET "http://localhost:8000/api/v1/hotels/city/Ouagadougou"
```

### Récupérer les hôtels par catégorie
```bash
curl -X GET "http://localhost:8000/api/v1/hotels/category/haut_standing"
```

### Récupérer les hôtels par gamme de prix
```bash
curl -X GET "http://localhost:8000/api/v1/hotels/price-range/?min_price=20000&max_price=80000"
```

## 3. Activités

### Créer une activité
```bash
curl -X POST "http://localhost:8000/api/v1/activities/" \
  -H "Content-Type: application/json" \
  -d '{
    "nom": "Randonnée au Parc du W",
    "description": "Excursion de deux jours dans le Parc du W pour observer la faune et flore",
    "type_activite": "randonnée",
    "categorie": ["nature", "faune", "aventure"],
    "ville": "Niamey",
    "region": "Tillabéry",
    "duree_heures": 16,
    "tarif_personne_fcfa": 25000,
    "tarif_groupe_fcfa": 18000,
    "nb_minimum_participants": 2,
    "nb_maximum_participants": 10,
    "niveau_difficulte": "moyen",
    "guide_fourni": true,
    "langue_guide": ["français", "dioula"],
    "equipement_requis": ["chaussures de randonnée", "chapeau", "protecteur solaire"],
    "vetements_recommandes": ["vetements legers", "vetements longs"],
    "jours_activite": ["lundi", "mercredi", "vendredi", "samedi", "dimanche"]
  }'
```

### Récupérer les activités par type
```bash
curl -X GET "http://localhost:8000/api/v1/activities/type/randonnée"
```

### Récupérer les activités par difficulté
```bash
curl -X GET "http://localhost:8000/api/v1/activities/difficulty/moyen"
```

### Récupérer les activités par destination
```bash
curl -X GET "http://localhost:8000/api/v1/activities/destination/{destination_id}"
```

## 4. Guides

### Créer un guide
```bash
curl -X POST "http://localhost:8000/api/v1/guides/" \
  -H "Content-Type: application/json" \
  -d '{
    "nom": "Traore",
    "prenom": "Aminata",
    "telephone": "+226 70 00 00 00",
    "email": "aminata.traore@example.com",
    "ville": "Ouagadougou",
    "region": "Kadiogo",
    "langues": ["français", "mooré", "dioula", "anglais"],
    "specialites": ["faune", "histoire", "culture", "géologie"],
    "licence_guide": true,
    "annees_experience": 8,
    "destinations_principales": ["Parc du W", "Cascade de Banfora", "Loropeni"],
    "tarif_journee_fcfa": 35000,
    "tarif_demi_journee_fcfa": 18000,
    "biographie": "Guide expérimenté avec une connaissance approfondie de la faune et la flore du Burkina",
    "possede_vehicule": true,
    "type_vehicule": "4x4",
    "disponible": true
  }'
```

### Récupérer les guides par ville
```bash
curl -X GET "http://localhost:8000/api/v1/guides/city/Ouagadougou"
```

### Récupérer les guides par langue
```bash
curl -X GET "http://localhost:8000/api/v1/guides/language/français"
```

### Récupérer les guides par spécialité
```bash
curl -X GET "http://localhost:8000/api/v1/guides/specialty/faune"
```

### Récupérer les guides avec véhicule
```bash
curl -X GET "http://localhost:8000/api/v1/guides/with-vehicle/"
```

### Récupérer les meilleurs guides
```bash
curl -X GET "http://localhost:8000/api/v1/guides/top-rated/?limit=10"
```

## Utilisation avec Python

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# Créer une destination
destination_data = {
    "nom": "Loropeni",
    "description": "Ruines d'une forteresse historique",
    "region": "Poni",
    "province": "Gaoua",
    "localite": "Loropeni",
    "type_destination": "site_historique",
    "categorie": ["histoire", "archéologie"],
    "latitude": 10.3627,
    "longitude": -3.1508
}

response = requests.post(f"{BASE_URL}/destinations/", json=destination_data)
print(response.json())

# Récupérer toutes les destinations
response = requests.get(f"{BASE_URL}/destinations/?skip=0&limit=10")
destinations = response.json()
for destination in destinations:
    print(f"- {destination['nom']} ({destination['region']})")

# Mettre à jour une destination
update_data = {
    "note_moyenne": 4.8,
    "nombre_evaluations": 150
}
response = requests.put(f"{BASE_URL}/destinations/{{destination_id}}", json=update_data)
print(response.json())

# Supprimer une destination
response = requests.delete(f"{BASE_URL}/destinations/{{destination_id}}")
print(response.json())
```

## Utilisation avec JavaScript/Fetch

```javascript
const BASE_URL = "http://localhost:8000/api/v1";

// Créer une activité
const activityData = {
  nom: "Atelier artisanal textile",
  description: "Découvrez les techniques traditionnelles de tissage",
  type_activite: "atelier_artisanal",
  categorie: ["culture", "artisanat"],
  ville: "Ouagadougou",
  region: "Kadiogo",
  duree_heures: 4,
  tarif_personne_fcfa: 15000,
  niveau_difficulte: "facile",
  guide_fourni: true
};

fetch(`${BASE_URL}/activities/`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify(activityData)
})
.then(response => response.json())
.then(data => console.log(data));

// Récupérer les meilleures activités
fetch(`${BASE_URL}/activities/top-rated/?limit=5`)
  .then(response => response.json())
  .then(data => console.log(data));
```

## Notes importantes

1. **Authentification**: À implémenter avec JWT
2. **Validation**: Tous les champs ont des validations côté serveur
3. **Erreurs**: Les erreurs retournent des status codes HTTP appropriés
4. **Pagination**: Utilisez les paramètres `skip` et `limit` pour paginer
5. **IDs**: Les IDs retournés sont les ObjectIds MongoDB convertis en chaînes
