from typing import List, Dict, Any
from datetime import datetime
from bson.objectid import ObjectId
from app.models.roads import RoadCondition
from app.schemas.roads import RoadCreate, RoadUpdate
from app.core.database import get_database


class RoadService:
    
    def __init__(self):
        self.collection_name = "road_conditions"

    async def create_condition(self, condition: RoadCreate) -> str:
        """Créer un report sur l'état d'une route"""
        db = get_database()
        condition_dict = condition.model_dump()
        condition_dict["date_creation"] = datetime.utcnow()
        condition_dict["date_modification"] = datetime.utcnow()
        result = await db[self.collection_name].insert_one(condition_dict)
        return str(result.inserted_id)

    async def get_condition(self, condition_id: str) -> Dict[str, Any] | None:
        """Récupérer un report routier"""
        db = get_database()
        try:
            obj_id = ObjectId(condition_id)
            condition = await db[self.collection_name].find_one({"_id": obj_id})
            if condition:
                condition["_id"] = str(condition["_id"])
            return condition
        except:
            return None

    async def get_all_conditions(self, skip: int = 0, limit: int = 50) -> List[Dict[str, Any]]:
        """Récupérer tous les rapports routiers"""
        db = get_database()
        conditions = await db[self.collection_name].find({}).skip(skip).limit(limit).to_list(limit)
        return [{**c, "_id": str(c["_id"])} for c in conditions]

    async def update_condition(self, condition_id: str, condition: RoadUpdate) -> bool:
        """Mettre à jour un report"""
        db = get_database()
        try:
            obj_id = ObjectId(condition_id)
            update_dict = condition.model_dump(exclude_unset=True)
            update_dict["date_modification"] = datetime.utcnow()
            result = await db[self.collection_name].update_one(
                {"_id": obj_id},
                {"$set": update_dict}
            )
            return result.modified_count > 0
        except:
            return False

    async def delete_condition(self, condition_id: str) -> bool:
        """Supprimer un report"""
        db = get_database()
        try:
            obj_id = ObjectId(condition_id)
            result = await db[self.collection_name].delete_one({"_id": obj_id})
            return result.deleted_count > 0
        except:
            return False

    async def get_dangerous_routes(self) -> List[Dict[str, Any]]:
        """Récupérer les ROUTES DANGEREUSES"""
        db = get_database()
        conditions = await db[self.collection_name].find({
            "note_securite": {"$lte": 3}
        }).sort("note_securite", 1).to_list(None)
        return [{**c, "_id": str(c["_id"])} for c in conditions]

    async def get_routes_by_from_to(self, from_city: str, to_city: str) -> List[Dict[str, Any]]:
        """Récupérer les conditions entre deux villes"""
        db = get_database()
        conditions = await db[self.collection_name].find({
            "$or": [
                {"ville_depart": from_city, "ville_arrivee": to_city},
                {"ville_depart": to_city, "ville_arrivee": from_city}
            ]
        }).to_list(None)
        return [{**c, "_id": str(c["_id"])} for c in conditions]

    async def get_routes_with_accidents(self) -> List[Dict[str, Any]]:
        """Récupérer les routes avec historique d'accidents"""
        db = get_database()
        conditions = await db[self.collection_name].find({
            "frequence_accidents": {"$gte": 5}
        }).sort("frequence_accidents", -1).to_list(None)
        return [{**c, "_id": str(c["_id"])} for c in conditions]

    async def get_banditry_risks_by_hour(self, heure: int) -> List[Dict[str, Any]]:
        """Récupérer les risques de banditisme pour une heure spécifique"""
        db = get_database()
        conditions = await db[self.collection_name].find({
            "heures_risque_banditisme": heure
        }).to_list(None)
        return [{**c, "_id": str(c["_id"])} for c in conditions]

    async def get_best_safe_routes(self) -> List[Dict[str, Any]]:
        """Récupérer les meilleures routes sûres"""
        db = get_database()
        conditions = await db[self.collection_name].find({
            "note_securite": {"$gte": 4}
        }).sort("note_securite", -1).to_list(None)
        return [{**c, "_id": str(c["_id"])} for c in conditions]

    async def get_routes_by_surface_type(self, surface_type: str) -> List[Dict[str, Any]]:
        """Récupérer les routes par type de surface"""
        db = get_database()
        conditions = await db[self.collection_name].find({
            "type_surface": surface_type
        }).to_list(None)
        return [{**c, "_id": str(c["_id"])} for c in conditions]
