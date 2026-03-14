from typing import List, Dict, Any
from datetime import datetime
from bson.objectid import ObjectId
from app.models.security import SecurityAlert
from app.schemas.security import SecurityCreate, SecurityUpdate
from app.core.database import get_database


class SecurityService:
    
    def __init__(self):
        self.collection_name = "security_alerts"

    async def create_alert(self, alert: SecurityCreate) -> str:
        """Créer une alerte de sécurité (CRITIQUE)"""
        db = get_database()
        alert_dict = alert.model_dump()
        alert_dict["date_creation"] = datetime.utcnow()
        alert_dict["date_modification"] = datetime.utcnow()
        alert_dict["verifiee"] = False
        alert_dict["active"] = True
        result = await db[self.collection_name].insert_one(alert_dict)
        return str(result.inserted_id)

    async def get_alert(self, alert_id: str) -> Dict[str, Any] | None:
        """Récupérer une alerte"""
        db = get_database()
        try:
            obj_id = ObjectId(alert_id)
            alert = await db[self.collection_name].find_one({"_id": obj_id})
            if alert:
                alert["_id"] = str(alert["_id"])
            return alert
        except:
            return None

    async def get_all_alerts(self, skip: int = 0, limit: int = 50) -> List[Dict[str, Any]]:
        """Récupérer toutes les alertes"""
        db = get_database()
        alerts = await db[self.collection_name].find({}).skip(skip).limit(limit).to_list(limit)
        return [{**a, "_id": str(a["_id"])} for a in alerts]

    async def update_alert(self, alert_id: str, alert: SecurityUpdate) -> bool:
        """Mettre à jour une alerte"""
        db = get_database()
        try:
            obj_id = ObjectId(alert_id)
            update_dict = alert.model_dump(exclude_unset=True)
            update_dict["date_modification"] = datetime.utcnow()
            result = await db[self.collection_name].update_one(
                {"_id": obj_id},
                {"$set": update_dict}
            )
            return result.modified_count > 0
        except:
            return False

    async def delete_alert(self, alert_id: str) -> bool:
        """Supprimer une alerte"""
        db = get_database()
        try:
            obj_id = ObjectId(alert_id)
            result = await db[self.collection_name].delete_one({"_id": obj_id})
            return result.deleted_count > 0
        except:
            return False

    async def get_active_alerts(self) -> List[Dict[str, Any]]:
        """Récupérer les alertes ACTIVES (temps réel)"""
        db = get_database()
        alerts = await db[self.collection_name].find({"active": True}).to_list(None)
        return [{**a, "_id": str(a["_id"])} for a in alerts]

    async def get_alerts_by_region(self, region: str) -> List[Dict[str, Any]]:
        """Récupérer les alertes d'une région"""
        db = get_database()
        alerts = await db[self.collection_name].find({
            "regions_affectees": region,
            "active": True
        }).to_list(None)
        return [{**a, "_id": str(a["_id"])} for a in alerts]

    async def get_high_risk_alerts(self) -> List[Dict[str, Any]]:
        """Récupérer les alertes à HAUT RISQUE"""
        db = get_database()
        alerts = await db[self.collection_name].find({
            "niveau_risque": {"$in": ["eleve", "tres_eleve"]},
            "active": True
        }).to_list(None)
        return [{**a, "_id": str(a["_id"])} for a in alerts]

    async def verify_alert(self, alert_id: str, verified_by: str) -> bool:
        """Vérifier une alerte (modération ADMIN)"""
        db = get_database()
        try:
            obj_id = ObjectId(alert_id)
            result = await db[self.collection_name].update_one(
                {"_id": obj_id},
                {
                    "$set": {
                        "verifiee": True,
                        "verifiee_par": verified_by,
                        "date_verification": datetime.utcnow()
                    }
                }
            )
            return result.modified_count > 0
        except:
            return False

    async def deactivate_alert(self, alert_id: str, raison: str) -> bool:
        """Désactiver une alerte (situation résolue)"""
        db = get_database()
        try:
            obj_id = ObjectId(alert_id)
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

    async def get_alerts_by_source_reliability(self, min_score: float = 0.7) -> List[Dict[str, Any]]:
        """Récupérer les alertes de sources fiables"""
        db = get_database()
        alerts = await db[self.collection_name].find({
            "fiabilite_source": {"$gte": min_score},
            "active": True
        }).sort("fiabilite_source", -1).to_list(None)
        return [{**a, "_id": str(a["_id"])} for a in alerts]
