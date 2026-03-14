from typing import List, Dict, Any
from datetime import datetime
from bson.objectid import ObjectId
from app.models.health_advisory import HealthAdvisory
from app.schemas.health_advisory import HealthAdvisoryCreate, HealthAdvisoryUpdate
from app.core.database import get_database


class HealthAdvisoryService:
    
    def __init__(self):
        self.collection_name = "health_advisories"

    async def create_advisory(self, advisory: HealthAdvisoryCreate) -> str:
        """Créer un conseil ou alerte sanitaire"""
        db = get_database()
        advisory_dict = advisory.model_dump()
        advisory_dict["date_creation"] = datetime.utcnow()
        advisory_dict["date_modification"] = datetime.utcnow()
        advisory_dict["active"] = True
        result = await db[self.collection_name].insert_one(advisory_dict)
        return str(result.inserted_id)

    async def get_advisory(self, advisory_id: str) -> Dict[str, Any] | None:
        """Récupérer un conseil sanitaire"""
        db = get_database()
        try:
            obj_id = ObjectId(advisory_id)
            advisory = await db[self.collection_name].find_one({"_id": obj_id})
            if advisory:
                advisory["_id"] = str(advisory["_id"])
            return advisory
        except:
            return None

    async def get_all_advisories(self, skip: int = 0, limit: int = 50) -> List[Dict[str, Any]]:
        """Récupérer tous les conseils sanitaires"""
        db = get_database()
        advisories = await db[self.collection_name].find({}).skip(skip).limit(limit).to_list(limit)
        return [{**a, "_id": str(a["_id"])} for a in advisories]

    async def update_advisory(self, advisory_id: str, advisory: HealthAdvisoryUpdate) -> bool:
        """Mettre à jour un conseil"""
        db = get_database()
        try:
            obj_id = ObjectId(advisory_id)
            update_dict = advisory.model_dump(exclude_unset=True)
            update_dict["date_modification"] = datetime.utcnow()
            result = await db[self.collection_name].update_one(
                {"_id": obj_id},
                {"$set": update_dict}
            )
            return result.modified_count > 0
        except:
            return False

    async def delete_advisory(self, advisory_id: str) -> bool:
        """Supprimer un conseil"""
        db = get_database()
        try:
            obj_id = ObjectId(advisory_id)
            result = await db[self.collection_name].delete_one({"_id": obj_id})
            return result.deleted_count > 0
        except:
            return False

    async def get_active_advisories(self) -> List[Dict[str, Any]]:
        """Récupérer les conseils ACTIFS"""
        db = get_database()
        advisories = await db[self.collection_name].find({"active": True}).to_list(None)
        return [{**a, "_id": str(a["_id"])} for a in advisories]

    async def get_advisories_by_region(self, region: str) -> List[Dict[str, Any]]:
        """Récupérer les conseils d'une région"""
        db = get_database()
        advisories = await db[self.collection_name].find({
            "regions_affectees": region,
            "active": True
        }).to_list(None)
        return [{**a, "_id": str(a["_id"])} for a in advisories]

    async def get_epidemics(self) -> List[Dict[str, Any]]:
        """Récupérer les alertes sur les épidémies"""
        db = get_database()
        advisories = await db[self.collection_name].find({
            "type": "epidemie",
            "active": True
        }).to_list(None)
        return [{**a, "_id": str(a["_id"])} for a in advisories]

    async def get_vaccination_requirements(self) -> List[Dict[str, Any]]:
        """Récupérer les exigences de vaccination"""
        db = get_database()
        advisories = await db[self.collection_name].find({
            "type": "vaccination"
        }).to_list(None)
        return [{**a, "_id": str(a["_id"])} for a in advisories]

    async def get_high_risk_advisories(self) -> List[Dict[str, Any]]:
        """Récupérer les conseils à haut risque"""
        db = get_database()
        advisories = await db[self.collection_name].find({
            "niveau_risque": {"$in": ["eleve", "tres_eleve"]},
            "active": True
        }).sort("niveau_risque", -1).to_list(None)
        return [{**a, "_id": str(a["_id"])} for a in advisories]

    async def get_endemic_diseases(self, region: str = None) -> List[Dict[str, Any]]:
        """Récupérer les maladies endémiques"""
        db = get_database()
        query = {"type": "maladie_endemique"}
        if region:
            query["regions_affectees"] = region
        advisories = await db[self.collection_name].find(query).to_list(None)
        return [{**a, "_id": str(a["_id"])} for a in advisories]

    async def deactivate_advisory(self, advisory_id: str, raison: str) -> bool:
        """Désactiver un conseil (situation résolue)"""
        db = get_database()
        try:
            obj_id = ObjectId(advisory_id)
            result = await db[self.collection_name].update_one(
                {"_id": obj_id},
                {
                    "$set": {
                        "active": False,
                        "raison_desactivation": raison,
                        "date_desactivation": datetime.utcnow()
                    }
                }
            )
            return result.modified_count > 0
        except:
            return False
