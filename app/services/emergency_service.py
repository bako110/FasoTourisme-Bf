from typing import List, Dict, Any
from datetime import datetime
from bson.objectid import ObjectId
from app.models.emergency import EmergencyService
from app.schemas.emergency import EmergencyCreate, EmergencyUpdate
from app.core.database import get_database


class EmergencyServiceService:
    
    def __init__(self):
        self.collection_name = "emergency_services"

    async def create_service(self, service: EmergencyCreate) -> str:
        """Créer un service d'urgence"""
        db = get_database()
        service_dict = service.model_dump()
        service_dict["date_creation"] = datetime.utcnow()
        service_dict["date_modification"] = datetime.utcnow()
        service_dict["operationnel"] = True
        result = await db[self.collection_name].insert_one(service_dict)
        return str(result.inserted_id)

    async def get_service(self, service_id: str) -> Dict[str, Any] | None:
        """Récupérer un service d'urgence"""
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
        """Récupérer tous les services d'urgence"""
        db = get_database()
        services = await db[self.collection_name].find({}).skip(skip).limit(limit).to_list(limit)
        return [{**s, "_id": str(s["_id"])} for s in services]

    async def update_service(self, service_id: str, service: EmergencyUpdate) -> bool:
        """Mettre à jour un service"""
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
        """Récupérer les services par type (police, ambulance, pompiers)"""
        db = get_database()
        services = await db[self.collection_name].find({"type": type_service}).to_list(None)
        return [{**s, "_id": str(s["_id"])} for s in services]

    async def get_services_by_region(self, region: str) -> List[Dict[str, Any]]:
        """Récupérer les services d'une région"""
        db = get_database()
        services = await db[self.collection_name].find({
            "zones_couvertes": region
        }).to_list(None)
        return [{**s, "_id": str(s["_id"])} for s in services]

    async def get_operational_services(self) -> List[Dict[str, Any]]:
        """Récupérer TOUS les services opérationnels"""
        db = get_database()
        services = await db[self.collection_name].find({"operationnel": True}).to_list(None)
        return [{**s, "_id": str(s["_id"])} for s in services]

    async def get_fastest_response(self, service_type: str) -> Dict[str, Any] | None:
        """Récupérer le service avec le temps de réponse le plus court"""
        db = get_database()
        service = await db[self.collection_name].find_one(
            {"type": service_type, "operationnel": True},
            sort=[("temps_response_moyen_minutes", 1)]
        )
        if service:
            service["_id"] = str(service["_id"])
        return service

    async def update_response_time(self, service_id: str, new_time_minutes: int) -> bool:
        """Mettre à jour le temps de réponse moyen"""
        db = get_database()
        try:
            obj_id = ObjectId(service_id)
            result = await db[self.collection_name].update_one(
                {"_id": obj_id},
                {"$set": {"temps_response_moyen_minutes": new_time_minutes}}
            )
            return result.modified_count > 0
        except:
            return False
