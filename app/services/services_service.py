from typing import List, Dict, Any
from datetime import datetime
from bson.objectid import ObjectId
from app.models.services import EssentialService
from app.schemas.services import EssentialServiceCreate, EssentialServiceUpdate
from app.core.database import get_database


class EssentialServiceService:
    
    def __init__(self):
        self.collection_name = "essential_services"

    async def create_service(self, service: EssentialServiceCreate) -> str:
        """Créer un service essentiel (eau, électricité, internet, etc)"""
        db = get_database()
        service_dict = service.model_dump()
        service_dict["date_creation"] = datetime.utcnow()
        service_dict["date_modification"] = datetime.utcnow()
        result = await db[self.collection_name].insert_one(service_dict)
        return str(result.inserted_id)

    async def get_service(self, service_id: str) -> Dict[str, Any] | None:
        """Récupérer un service essentiel"""
        db = get_database()
        try:
            obj_id = ObjectId(service_id)
            service = await db[self.collection_name].find_one({"_id": obj_id})
            if service:
                service["_id"] = str(service["_id"])
            return service
        except:
            return None

    async def get_all_services(self, skip: int = 0, limit: int = 50) -> List[Dict[str, Any]]:
        """Récupérer tous les services essentiels"""
        db = get_database()
        services = await db[self.collection_name].find({}).skip(skip).limit(limit).to_list(limit)
        return [{**s, "_id": str(s["_id"])} for s in services]

    async def update_service(self, service_id: str, service: EssentialServiceUpdate) -> bool:
        """Mettre à jour un service essentiel"""
        db = get_database()
        try:
            obj_id = ObjectId(service_id)
            update_dict = service.model_dump(exclude_unset=True)
            update_dict["date_modification"] = datetime.utcnow()
            result = await db[self.collection_name].update_one(
                {"_id": obj_id},
                {"$set": update_dict}
            )
            return result.modified_count > 0
        except:
            return False

    async def delete_service(self, service_id: str) -> bool:
        """Supprimer un service"""
        db = get_database()
        try:
            obj_id = ObjectId(service_id)
            result = await db[self.collection_name].delete_one({"_id": obj_id})
            return result.deleted_count > 0
        except:
            return False

    async def get_services_by_type(self, type_service: str) -> List[Dict[str, Any]]:
        """Récupérer les services par type (eau, électricité, internet, etc)"""
        db = get_database()
        services = await db[self.collection_name].find({"type": type_service}).to_list(None)
        return [{**s, "_id": str(s["_id"])} for s in services]

    async def get_services_by_city(self, ville: str) -> List[Dict[str, Any]]:
        """Récupérer les services d'une ville"""
        db = get_database()
        services = await db[self.collection_name].find({"ville": ville}).to_list(None)
        return [{**s, "_id": str(s["_id"])} for s in services]

    async def get_reliable_internet_providers(self, ville: str) -> List[Dict[str, Any]]:
        """Récupérer les fournisseurs internet fiables d'une ville"""
        db = get_database()
        services = await db[self.collection_name].find({
            "type": "internet",
            "ville": ville,
            "stabilite": {"$gte": 0.7}
        }).sort("stabilite", -1).to_list(None)
        return [{**s, "_id": str(s["_id"])} for s in services]

    async def get_water_info(self, ville: str) -> Dict[str, Any] | None:
        """Récupérer les infos sur l'eau dans une ville"""
        db = get_database()
        service = await db[self.collection_name].find_one({
            "type": "eau",
            "ville": ville
        })
        if service:
            service["_id"] = str(service["_id"])
        return service

    async def get_electricity_stability(self, ville: str) -> Dict[str, Any] | None:
        """Récupérer la stabilité électrique d'une ville"""
        db = get_database()
        service = await db[self.collection_name].find_one({
            "type": "electricite",
            "ville": ville
        })
        if service:
            service["_id"] = str(service["_id"])
        return service

    async def get_banking_locations(self, ville: str) -> List[Dict[str, Any]]:
        """Récupérer les emplacements bancaires d'une ville"""
        db = get_database()
        services = await db[self.collection_name].find({
            "type": "banque",
            "ville": ville
        }).to_list(None)
        return [{**s, "_id": str(s["_id"])} for s in services]
