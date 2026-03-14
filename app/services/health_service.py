from typing import List, Dict, Any
from datetime import datetime
from bson.objectid import ObjectId
from app.models.health import HealthFacility
from app.schemas.health import HealthCreate, HealthUpdate
from app.core.database import get_database


class HealthService:
    
    def __init__(self):
        self.collection_name = "health_facilities"

    async def create_facility(self, facility: HealthCreate) -> str:
        """Créer une new structure sanitaire"""
        db = get_database()
        facility_dict = facility.model_dump()
        facility_dict["date_creation"] = datetime.utcnow()
        facility_dict["date_modification"] = datetime.utcnow()
        facility_dict["verifiee"] = False
        result = await db[self.collection_name].insert_one(facility_dict)
        return str(result.inserted_id)

    async def get_facility(self, facility_id: str) -> Dict[str, Any] | None:
        """Récupérer une structure sanitaire"""
        db = get_database()
        try:
            obj_id = ObjectId(facility_id)
            facility = await db[self.collection_name].find_one({"_id": obj_id})
            if facility:
                facility["_id"] = str(facility["_id"])
            return facility
        except:
            return None

    async def get_all_facilities(self, skip: int = 0, limit: int = 50) -> List[Dict[str, Any]]:
        """Récupérer toutes les structures sanitaires"""
        db = get_database()
        facilities = await db[self.collection_name].find({}).skip(skip).limit(limit).to_list(limit)
        return [{**f, "_id": str(f["_id"])} for f in facilities]

    async def update_facility(self, facility_id: str, facility: HealthUpdate) -> bool:
        """Mettre à jour une structure"""
        db = get_database()
        try:
            obj_id = ObjectId(facility_id)
            update_dict = facility.model_dump(exclude_unset=True)
            update_dict["date_modification"] = datetime.utcnow()
            result = await db[self.collection_name].update_one(
                {"_id": obj_id},
                {"$set": update_dict}
            )
            return result.modified_count > 0
        except:
            return False

    async def delete_facility(self, facility_id: str) -> bool:
        """Supprimer une structure"""
        db = get_database()
        try:
            obj_id = ObjectId(facility_id)
            result = await db[self.collection_name].delete_one({"_id": obj_id})
            return result.deleted_count > 0
        except:
            return False

    async def get_facilities_by_city(self, ville: str) -> List[Dict[str, Any]]:
        """Récupérer les structures d'une ville"""
        db = get_database()
        facilities = await db[self.collection_name].find({"ville": ville}).to_list(None)
        return [{**f, "_id": str(f["_id"])} for f in facilities]

    async def get_pharmacies(self) -> List[Dict[str, Any]]:
        """Récupérer toutes les pharmacies"""
        db = get_database()
        facilities = await db[self.collection_name].find({"type": "pharmacie"}).to_list(None)
        return [{**f, "_id": str(f["_id"])} for f in facilities]

    async def get_emergency_facilities(self) -> List[Dict[str, Any]]:
        """Récupérer les structures avec urgences 24h"""
        db = get_database()
        facilities = await db[self.collection_name].find({
            "urgences_24h": True
        }).to_list(None)
        return [{**f, "_id": str(f["_id"])} for f in facilities]

    async def get_facilities_near_location(self, latitude: float, longitude: float, radius_km: float = 5) -> List[Dict[str, Any]]:
        """Trouver les structures sanitaires proches d'une localisation"""
        db = get_database()
        # Convertir le rayon en degrés (approximation)
        radius_degrees = radius_km / 111
        facilities = await db[self.collection_name].find({
            "latitude": {"$gte": latitude - radius_degrees, "$lte": latitude + radius_degrees},
            "longitude": {"$gte": longitude - radius_degrees, "$lte": longitude + radius_degrees}
        }).to_list(None)
        return [{**f, "_id": str(f["_id"])} for f in facilities]

    async def verify_facility(self, facility_id: str) -> bool:
        """Vérifier une structure (admin)"""
        db = get_database()
        try:
            obj_id = ObjectId(facility_id)
            result = await db[self.collection_name].update_one(
                {"_id": obj_id},
                {"$set": {"verifiee": True, "date_verification": datetime.utcnow()}}
            )
            return result.modified_count > 0
        except:
            return False
