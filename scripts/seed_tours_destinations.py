import asyncio
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings


# URLs d'images réelles pour les destinations (normalisées: image + images)
DESTINATION_IMAGES = {
    "Lac de Tengrela": {
        "image": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1200&h=800&fit=crop",
        "images": [
            "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1200&h=800&fit=crop",
            "https://images.unsplash.com/photo-1489749798305-4fea3ba63d60?w=1200&h=800&fit=crop",
            "https://images.unsplash.com/photo-1495536821757-a1efb6729352?w=1200&h=800&fit=crop",
            "https://images.unsplash.com/photo-1439066615861-d1af74d74000?w=1200&h=800&fit=crop"
        ]
    },
    "Caimans sacres de Sabou": {
        "image": "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=1200&h=800&fit=crop",
        "images": [
            "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=1200&h=800&fit=crop",
            "https://images.unsplash.com/photo-1445308394109-c23814f75bbb?w=1200&h=800&fit=crop",
            "https://images.unsplash.com/photo-1395003593705-88ef62187dd9?w=1200&h=800&fit=crop",
            "https://images.unsplash.com/photo-1464207687429-7505649dae38?w=1200&h=800&fit=crop"
        ]
    },
    "Pics de Sindou": {
        "image": "https://images.unsplash.com/photo-1506905925346-24c1e6c22aee?w=1200&h=800&fit=crop",
        "images": [
            "https://images.unsplash.com/photo-1506905925346-24c1e6c22aee?w=1200&h=800&fit=crop",
            "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1200&h=800&fit=crop",
            "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1200&h=800&fit=crop",
            "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1200&h=800&fit=crop"
        ]
    },
    "Domes de Fabedougou": {
        "image": "https://images.unsplash.com/photo-1469022563149-aa64dbd37dae?w=1200&h=800&fit=crop",
        "images": [
            "https://images.unsplash.com/photo-1469022563149-aa64dbd37dae?w=1200&h=800&fit=crop",
            "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1200&h=800&fit=crop",
            "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1200&h=800&fit=crop",
            "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1200&h=800&fit=crop"
        ]
    },
    "Ruines de Loropeni": {
        "image": "https://images.unsplash.com/photo-1506905925346-24c1e6c16c20?w=1200&h=800&fit=crop",
        "images": [
            "https://images.unsplash.com/photo-1506905925346-24c1e6c16c20?w=1200&h=800&fit=crop",
            "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1200&h=800&fit=crop",
            "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1200&h=800&fit=crop",
            "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1200&h=800&fit=crop"
        ]
    },
    "Cascade de Karfiguela": {
        "image": "https://images.unsplash.com/photo-1439066615861-d1af74d74000?w=1200&h=800&fit=crop",
        "images": [
            "https://images.unsplash.com/photo-1439066615861-d1af74d74000?w=1200&h=800&fit=crop",
            "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1200&h=800&fit=crop",
            "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1200&h=800&fit=crop",
            "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1200&h=800&fit=crop"
        ]
    }
}

# Images pour les guides (extraire juste les URLs)
GUIDE_IMAGES = [
    "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=1200&h=1200&fit=crop",
    "https://images.unsplash.com/photo-1500336541842-6f6b0db2915e?w=1200&h=1200&fit=crop",
    "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=1200&h=1200&fit=crop",
    "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=1200&h=1200&fit=crop",
]

TEST_DESTINATIONS = [
    {
        "nom": "Lac de Tengrela",
        "description": "Un lac paisible connu pour ses hippopotames et ses balades en pirogue.",
        "region": "Cascades",
        "province": "Comoe",
        "localite": "Banfora",
        "type_destination": "site_naturel",
        "categorie": ["nature", "ecotourisme"],
        "latitude": 10.6412,
        "longitude": -4.8587,
        "temps_acces_heures": 6.5,
        "meilleure_saison": ["novembre", "decembre", "janvier"],
        "acces_securise": True,
        "tarif_entree_fcfa": 1500,
        "tarif_guide_fcfa": 10000,
        "image": DESTINATION_IMAGES["Lac de Tengrela"]["image"],
        "images": DESTINATION_IMAGES["Lac de Tengrela"]["images"],
        "video_url": "https://www.youtube.com/watch?v=example1",
        "note_moyenne": 4.6,
        "nombre_evaluations": 18,
        "publie": True,
    },
    {
        "nom": "Caimans sacres de Sabou",
        "description": "Site culturel celebre ou les visiteurs peuvent observer les caimans sacres de Sabou.",
        "region": "Centre-Ouest",
        "province": "Boulkiemde",
        "localite": "Sabou",
        "type_destination": "site_historique",
        "categorie": ["culture", "tradition"],
        "latitude": 12.3258,
        "longitude": -2.1558,
        "temps_acces_heures": 1.5,
        "meilleure_saison": ["octobre", "novembre", "decembre"],
        "acces_securise": True,
        "tarif_entree_fcfa": 1000,
        "tarif_guide_fcfa": 5000,
        "image": DESTINATION_IMAGES["Caimans sacres de Sabou"]["image"],
        "images": DESTINATION_IMAGES["Caimans sacres de Sabou"]["images"],
        "video_url": "https://www.youtube.com/watch?v=example2",
        "note_moyenne": 4.4,
        "nombre_evaluations": 25,
        "publie": True,
    },
    {
        "nom": "Pics de Sindou",
        "description": "Formation rocheuse spectaculaire ideale pour la randonnee et la photographie.",
        "region": "Cascades",
        "province": "Leraba",
        "localite": "Sindou",
        "type_destination": "site_naturel",
        "categorie": ["nature", "randonnee"],
        "latitude": 10.6667,
        "longitude": -5.1667,
        "temps_acces_heures": 7.0,
        "meilleure_saison": ["novembre", "decembre", "janvier", "fevrier"],
        "acces_securise": True,
        "tarif_entree_fcfa": 2000,
        "tarif_guide_fcfa": 12000,
        "image": DESTINATION_IMAGES["Pics de Sindou"]["image"],
        "images": DESTINATION_IMAGES["Pics de Sindou"]["images"],
        "video_url": "https://www.youtube.com/watch?v=example3",
        "note_moyenne": 4.8,
        "nombre_evaluations": 31,
        "publie": True,
    },
    {
        "nom": "Domes de Fabedougou",
        "description": "Ensemble geologique remarquable a proximite de Banfora.",
        "region": "Cascades",
        "province": "Comoe",
        "localite": "Fabedougou",
        "type_destination": "site_naturel",
        "categorie": ["nature", "geologie"],
        "latitude": 10.7102,
        "longitude": -4.8068,
        "temps_acces_heures": 6.0,
        "meilleure_saison": ["novembre", "decembre", "janvier"],
        "acces_securise": True,
        "tarif_entree_fcfa": 1500,
        "tarif_guide_fcfa": 8000,
        "image": DESTINATION_IMAGES["Domes de Fabedougou"]["image"],
        "images": DESTINATION_IMAGES["Domes de Fabedougou"]["images"],
        "video_url": "https://www.youtube.com/watch?v=example4",
        "note_moyenne": 4.5,
        "nombre_evaluations": 14,
        "publie": True,
    },
    {
        "nom": "Ruines de Loropeni",
        "description": "Vestiges classes au patrimoine mondial de l'UNESCO dans le sud-ouest.",
        "region": "Sud-Ouest",
        "province": "Poni",
        "localite": "Loropeni",
        "type_destination": "site_historique",
        "categorie": ["histoire", "patrimoine"],
        "latitude": 10.2996,
        "longitude": -3.5369,
        "temps_acces_heures": 8.0,
        "meilleure_saison": ["novembre", "decembre", "janvier", "fevrier"],
        "acces_securise": True,
        "tarif_entree_fcfa": 2500,
        "tarif_guide_fcfa": 15000,
        "image": DESTINATION_IMAGES["Ruines de Loropeni"]["image"],
        "images": DESTINATION_IMAGES["Ruines de Loropeni"]["images"],
        "video_url": "https://www.youtube.com/watch?v=example5",
        "note_moyenne": 4.7,
        "nombre_evaluations": 20,
        "publie": True,
    },
    {
        "nom": "Cascade de Karfiguela",
        "description": "Chutes d'eau tres visitees dans la region des Cascades, ideales pour les sorties detente.",
        "region": "Cascades",
        "province": "Comoe",
        "localite": "Karfiguela",
        "type_destination": "cascade",
        "categorie": ["nature", "detente"],
        "latitude": 10.6347,
        "longitude": -4.7596,
        "temps_acces_heures": 6.0,
        "meilleure_saison": ["aout", "septembre", "octobre"],
        "acces_securise": True,
        "tarif_entree_fcfa": 2000,
        "tarif_guide_fcfa": 8000,
        "image": DESTINATION_IMAGES["Cascade de Karfiguela"]["image"],
        "images": DESTINATION_IMAGES["Cascade de Karfiguela"]["images"],
        "video_url": "https://www.youtube.com/watch?v=example6",
        "note_moyenne": 4.9,
        "nombre_evaluations": 42,
        "publie": True,
    },
]

GUIDE_PROFILES = [
    {
        "specialites": ["Culture locale", "Histoire", "Nature & Faune"],
        "langues": ["Francais", "Anglais", "Dioula"],
        "destinations_principales": ["Cascades", "Hauts-Bassins"],
        "tours_proposes": ["Lac de Tengrela", "Pics de Sindou", "Cascade de Karfiguela"],
        "region": "Cascades",
        "ville": "Banfora",
    },
    {
        "specialites": ["Culture locale", "Architecture", "Artisanat"],
        "langues": ["Francais", "Mooré"],
        "destinations_principales": ["Centre", "Centre-Ouest"],
        "tours_proposes": ["Caimans sacres de Sabou", "Ruines de Loropeni"],
        "region": "Centre",
        "ville": "Ouagadougou",
    },
]


async def seed_destinations(db):
    collection = db["destinations"]
    inserted = 0
    updated = 0

    for destination in TEST_DESTINATIONS:
        now = datetime.utcnow()
        payload = {
            **destination,
            "date_modification": now,
        }
        result = await collection.update_one(
            {"nom": destination["nom"]},
            {"$set": payload, "$setOnInsert": {"date_creation": now}},
            upsert=True,
        )
        if result.upserted_id:
            inserted += 1
        elif result.modified_count > 0:
            updated += 1

    print(f"Destinations inserees: {inserted}, mises a jour: {updated}")


async def seed_guides(db):
    users = []
    async for user in db["users"].find({"role": "guide"}):
        users.append(user)

    if not users:
        print("Aucun utilisateur avec role=guide trouve. Seed des guides ignore.")
        return

    inserted = 0
    updated = 0

    for index, user in enumerate(users):
        profile_template = GUIDE_PROFILES[index % len(GUIDE_PROFILES)]
        nom_parts = (user.get("nom_complet") or "Guide Test").split(maxsplit=1)
        nom = nom_parts[0]
        prenom = nom_parts[1] if len(nom_parts) > 1 else ""
        now = datetime.utcnow()

        guide_doc = {
            "user_id": str(user["_id"]),
            "nom": nom,
            "prenom": prenom,
            "telephone": user.get("telephone") or "+22670000000",
            "email": user.get("email"),
            "image": GUIDE_IMAGES[index % len(GUIDE_IMAGES)],
            "ville": profile_template["ville"],
            "region": profile_template["region"],
            "langues": profile_template["langues"],
            "specialites": profile_template["specialites"],
            "licence_guide": True,
            "articles_guides": None,
            "annees_experience": 5 + index,
            "destinations_principales": profile_template["destinations_principales"],
            "tarif_journee_fcfa": 25000 + (index * 5000),
            "tarif_demi_journee_fcfa": 12500 + (index * 2500),
            "biographie": f"Guide de test pour {user.get('nom_complet', 'profil guide')}.",
            "possede_vehicule": index % 2 == 0,
            "type_vehicule": "4x4" if index % 2 == 0 else None,
            "disponible": True,
            "jours_disponibilite": ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi"],
            "note_moyenne": 4.5,
            "nombre_avis": 12,
            "nombre_clients_satisfaits": 40,
            "activites_animees": [],
            "destinations_reconnues": [],
            "tours_proposes": profile_template["tours_proposes"],
            "actif": True,
            "verified": True,
            "certifications": ["Guide touristique certifie"],
            "date_modification": now,
        }

        result = await db["guides"].update_one(
            {"user_id": str(user["_id"])},
            {"$set": {**guide_doc, "date_modification": now}, "$setOnInsert": {"date_inscription": now}},
            upsert=True,
        )

        guide = await db["guides"].find_one({"user_id": str(user["_id"])}, {"_id": 1})
        if guide:
            await db["users"].update_one(
                {"_id": user["_id"]},
                {"$set": {"profil_type": "guide", "profil_id": str(guide["_id"]), "profil_verifiee": True}},
            )

        if result.upserted_id:
            inserted += 1
        elif result.modified_count > 0:
            updated += 1

    print(f"Profils guides inseres: {inserted}, mis a jour: {updated}")


async def seed_user_photos(db):
    """Ajoute des photos de profil à tous les utilisateurs"""
    users_collection = db["users"]
    updated_guide = 0
    updated_tourist = 0
    
    # Ajouter des photos aux guides
    async for user in users_collection.find({"role": "guide"}):
        result = await users_collection.update_one(
            {"_id": user["_id"]},
            {"$set": {"photo_url": GUIDE_IMAGES[hash(str(user["_id"])) % len(GUIDE_IMAGES)]}}
        )
        if result.modified_count > 0:
            updated_guide += 1
    
    # Ajouter des photos aux tourists
    async for user in users_collection.find({"role": "tourist"}):
        # Utiliser un sous-ensemble d'images pour les tourists
        tourist_photo = GUIDE_IMAGES[hash(str(user["_id"])) % len(GUIDE_IMAGES)]
        result = await users_collection.update_one(
            {"_id": user["_id"]},
            {"$set": {"photo_url": tourist_photo}}
        )
        if result.modified_count > 0:
            updated_tourist += 1
    
    print(f"Photos guides mises à jour: {updated_guide}, Photos tourists mises à jour: {updated_tourist}")


async def main():
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    try:
        await client.admin.command("ping")
        db = client[settings.DATABASE_NAME]
        await seed_destinations(db)
        await seed_guides(db)
        await seed_user_photos(db)
        print("Seed termine avec succes.")
    finally:
        client.close()


if __name__ == "__main__":
    asyncio.run(main())