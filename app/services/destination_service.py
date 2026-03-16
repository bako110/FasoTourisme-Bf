from typing import List, Optional
from bson import ObjectId
from app.models.destination import Destination
from app.schemas.destination import DestinationCreate, DestinationUpdate
from app.core.database import get_database
import logging

logger = logging.getLogger(__name__)


class DestinationService:
    """Service pour gérer les destinations"""
    
    def __init__(self, db=None):
        self.db = db
        self.collection_name = "destinations"

    def _get_db(self):
        if self.db is not None:
            return self.db
        return get_database()

    def _format_destination(self, destination: dict) -> dict:
        """Convertir un document MongoDB en dict pour le frontend"""
        if destination:
            # Convertir _id à un string
            destination["_id"] = str(destination["_id"])
            # Assigner explicitement à id pour éviter confusion avec alias Pydantic
            destination["id"] = destination["_id"]
            
            # Normaliser les champs d'images
            # Récupérer image principale: image (nouveau) ou image_principale (ancien)
            main_image = destination.get("image") or destination.get("image_principale")
            if main_image:
                if isinstance(main_image, str):
                    destination["image"] = main_image
                elif isinstance(main_image, dict) and "url" in main_image:
                    destination["image"] = main_image["url"]
                else:
                    destination["image"] = str(main_image) if main_image else None
            else:
                destination["image"] = None
            
            # Récupérer toutes les images: images (nouveau) ou galerie_images (ancien) ou images
            all_images = destination.get("images") or destination.get("galerie_images") or []
            if isinstance(all_images, list) and len(all_images) > 0:
                # Convertir les dicts en strings
                destination["images"] = [
                    img["url"] if isinstance(img, dict) and "url" in img else str(img) if not isinstance(img, str) else img
                    for img in all_images
                ]
            else:
                destination["images"] = []
            
            # Pour backward compatibility
            destination["image_principale"] = destination.get("image")
            destination["galerie_images"] = destination.get("images", [])
            
        return destination
    
    async def create_destination(self, destination: DestinationCreate) -> str:
        """Créer une nouvelle destination"""
        try:
            db = self._get_db()
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
            db = self._get_db()
            # Valider l'ObjectId
            if not destination_id or destination_id == 'undefined':
                logger.warning(f"ID de destination invalide: {destination_id}")
                return None
            
            try:
                object_id = ObjectId(destination_id)
            except Exception as e:
                logger.warning(f"ID invalide au format ObjectId: {destination_id}, erreur: {e}")
                return None
            
            destination = await db[self.collection_name].find_one({"_id": object_id})
            return self._format_destination(destination) if destination else None
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de la destination: {e}")
            raise
    
    async def get_all_destinations(self, skip: int = 0, limit: int = 10) -> List[dict]:
        """Récupérer toutes les destinations"""
        try:
            db = self._get_db()
            destinations = []
            async for destination in db[self.collection_name].find({}).skip(skip).limit(limit):
                destinations.append(self._format_destination(destination))
            return destinations
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des destinations: {e}")
            raise
    
    async def get_destinations_by_region(self, region: str) -> List[dict]:
        """Récupérer les destinations par région"""
        try:
            db = self._get_db()
            destinations = []
            async for destination in db[self.collection_name].find({"region": region}):
                destinations.append(self._format_destination(destination))
            return destinations
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des destinations par région: {e}")
            raise
    
    async def get_destinations_by_type(self, type_destination: str) -> List[dict]:
        """Récupérer les destinations par type"""
        try:
            db = self._get_db()
            destinations = []
            async for destination in db[self.collection_name].find({"type_destination": type_destination}):
                destinations.append(self._format_destination(destination))
            return destinations
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des destinations par type: {e}")
            raise
    
    async def update_destination(self, destination_id: str, destination_update: DestinationUpdate) -> bool:
        """Mettre à jour une destination"""
        try:
            db = self._get_db()
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
            db = self._get_db()
            result = await db[self.collection_name].delete_one({"_id": ObjectId(destination_id)})
            logger.info(f"Destination supprimée: {destination_id}")
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Erreur lors de la suppression de la destination: {e}")
            raise
    
    async def search_destinations(self, query: str) -> List[dict]:
        """Rechercher les destinations"""
        try:
            db = self._get_db()
            destinations = []
            async for destination in db[self.collection_name].find({
                "$text": {"$search": query}
            }):
                destinations.append(self._format_destination(destination))
            return destinations
        except Exception as e:
            logger.error(f"Erreur lors de la recherche des destinations: {e}")
            raise
    
    async def get_top_rated_destinations(self, limit: int = 5) -> List[dict]:
        """Récupérer les destinations les mieux notées"""
        try:
            db = self._get_db()
            destinations = []
            async for destination in db[self.collection_name].find({"publie": True}).sort("note_moyenne", -1).limit(limit):
                destinations.append(self._format_destination(destination))
            return destinations
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des meilleures destinations: {e}")
            raise
