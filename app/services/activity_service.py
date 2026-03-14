from typing import List, Optional
from bson import ObjectId
from app.schemas.activity import ActivityCreate, ActivityUpdate
from app.core.database import get_database
import logging

logger = logging.getLogger(__name__)


class ActivityService:
    """Service pour gérer les activités"""
    
    def __init__(self):
        self.collection_name = "activities"
    
    async def create_activity(self, activity: ActivityCreate) -> str:
        """Créer une nouvelle activité"""
        try:
            activity_dict = activity.model_dump()
            result = await self.collection.insert_one(activity_dict)
            logger.info(f"Activité créée: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Erreur lors de la création d'une activité: {e}")
            raise
    
    async def get_activity(self, activity_id: str) -> Optional[dict]:
        """Récupérer une activité par ID"""
        try:
            activity = await self.collection.find_one({"_id": ObjectId(activity_id)})
            if activity:
                activity["id"] = str(activity["_id"])
            return activity
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de l'activité: {e}")
            raise
    
    async def get_all_activities(self, skip: int = 0, limit: int = 10) -> List[dict]:
        """Récupérer toutes les activités"""
        try:
            activities = []
            async for activity in self.collection.find({}).skip(skip).limit(limit):
                activity["id"] = str(activity["_id"])
                activities.append(activity)
            return activities
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des activités: {e}")
            raise
    
    async def get_activities_by_destination(self, destination_id: str) -> List[dict]:
        """Récupérer les activités par destination"""
        try:
            activities = []
            async for activity in self.collection.find({"destination_id": destination_id}):
                activity["id"] = str(activity["_id"])
                activities.append(activity)
            return activities
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des activités par destination: {e}")
            raise
    
    async def get_activities_by_type(self, type_activite: str) -> List[dict]:
        """Récupérer les activités par type"""
        try:
            activities = []
            async for activity in self.collection.find({"type_activite": type_activite}):
                activity["id"] = str(activity["_id"])
                activities.append(activity)
            return activities
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des activités par type: {e}")
            raise
    
    async def get_activities_by_city(self, ville: str) -> List[dict]:
        """Récupérer les activités par ville"""
        try:
            activities = []
            async for activity in self.collection.find({"ville": ville}):
                activity["id"] = str(activity["_id"])
                activities.append(activity)
            return activities
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des activités par ville: {e}")
            raise
    
    async def get_activities_by_difficulty(self, niveau_difficulte: str) -> List[dict]:
        """Récupérer les activités par niveau de difficulté"""
        try:
            activities = []
            async for activity in self.collection.find({"niveau_difficulte": niveau_difficulte}):
                activity["id"] = str(activity["_id"])
                activities.append(activity)
            return activities
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des activités par difficulté: {e}")
            raise
    
    async def update_activity(self, activity_id: str, activity_update: ActivityUpdate) -> bool:
        """Mettre à jour une activité"""
        try:
            update_data = activity_update.model_dump(exclude_unset=True)
            if update_data:
                result = await self.collection.update_one(
                    {"_id": ObjectId(activity_id)},
                    {"$set": update_data}
                )
                logger.info(f"Activité mise à jour: {activity_id}")
                return result.modified_count > 0
            return False
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour de l'activité: {e}")
            raise
    
    async def delete_activity(self, activity_id: str) -> bool:
        """Supprimer une activité"""
        try:
            result = await self.collection.delete_one({"_id": ObjectId(activity_id)})
            logger.info(f"Activité supprimée: {activity_id}")
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Erreur lors de la suppression de l'activité: {e}")
            raise
    
    async def get_top_rated_activities(self, limit: int = 5) -> List[dict]:
        """Récupérer les activités les mieux notées"""
        try:
            activities = []
            async for activity in self.collection.find({"publie": True}).sort("note_moyenne", -1).limit(limit):
                activity["id"] = str(activity["_id"])
                activities.append(activity)
            return activities
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des meilleures activités: {e}")
            raise
