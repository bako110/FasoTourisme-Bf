from typing import List, Optional
from bson import ObjectId
from app.models.destination import Destination
from app.schemas.destination import DestinationCreate, DestinationUpdate
from app.core.database import get_database
import logging

logger = logging.getLogger(__name__)


class DestinationService:
    """Service pour gérer les destinations"""
    
    def __init__(self):
        self.collection_name = "destinations"
    
    async def create_destination(self, destination: DestinationCreate) -> str:
        """Créer une nouvelle destination"""
        try:
            db = get_database()
            destination_dict = destination.model_dump()
            result = await db[self.collection_name].insert_one(destination_dict)
            logger.info(f"Destination créée: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Erreur lors de la création d'une destination: {e}")
            raise
    
    async def get_destination(self, destination_id: str) -> Optional[dict]:
        """Récupérer une destination par ID"""
        try:
            db = get_database()
            destination = await db[self.collection_name].find_one({"_id": ObjectId(destination_id)})
            if destination:
                destination["id"] = str(destination["_id"])
            return destination
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de la destination: {e}")
            raise
    
    async def get_all_destinations(self, skip: int = 0, limit: int = 10) -> List[dict]:
        """Récupérer toutes les destinations"""
        try:
            db = get_database()
            destinations = []
            async for destination in db[self.collection_name].find({}).skip(skip).limit(limit):
                destination["id"] = str(destination["_id"])
                destinations.append(destination)
            return destinations
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des destinations: {e}")
            raise
    
    async def get_destinations_by_region(self, region: str) -> List[dict]:
        """Récupérer les destinations par région"""
        try:
            db = get_database()
            destinations = []
            async for destination in db[self.collection_name].find({"region": region}):
                destination["id"] = str(destination["_id"])
                destinations.append(destination)
            return destinations
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des destinations par région: {e}")
            raise
    
    async def get_destinations_by_type(self, type_destination: str) -> List[dict]:
        """Récupérer les destinations par type"""
        try:
            db = get_database()
            destinations = []
            async for destination in db[self.collection_name].find({"type_destination": type_destination}):
                destination["id"] = str(destination["_id"])
                destinations.append(destination)
            return destinations
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des destinations par type: {e}")
            raise
    
    async def update_destination(self, destination_id: str, destination_update: DestinationUpdate) -> bool:
        """Mettre à jour une destination"""
        try:
            db = get_database()
            update_data = destination_update.model_dump(exclude_unset=True)
            if update_data:
                result = await db[self.collection_name].update_one(
                    {"_id": ObjectId(destination_id)},
                    {"$set": update_data}
                )
                logger.info(f"Destination mise à jour: {destination_id}")
                return result.modified_count > 0
            return False
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour de la destination: {e}")
            raise
    
    async def delete_destination(self, destination_id: str) -> bool:
        """Supprimer une destination"""
        try:
            db = get_database()
            result = await db[self.collection_name].delete_one({"_id": ObjectId(destination_id)})
            logger.info(f"Destination supprimée: {destination_id}")
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Erreur lors de la suppression de la destination: {e}")
            raise
    
    async def search_destinations(self, query: str) -> List[dict]:
        """Rechercher les destinations"""
        try:
            db = get_database()
            destinations = []
            async for destination in db[self.collection_name].find({
                "$text": {"$search": query}
            }):
                destination["id"] = str(destination["_id"])
                destinations.append(destination)
            return destinations
        except Exception as e:
            logger.error(f"Erreur lors de la recherche des destinations: {e}")
            raise
    
    async def get_top_rated_destinations(self, limit: int = 5) -> List[dict]:
        """Récupérer les destinations les mieux notées"""
        try:
            destinations = []
            async for destination in self.collection.find({"publie": True}).sort("note_moyenne", -1).limit(limit):
                destination["id"] = str(destination["_id"])
                destinations.append(destination)
            return destinations
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des meilleures destinations: {e}")
            raise
