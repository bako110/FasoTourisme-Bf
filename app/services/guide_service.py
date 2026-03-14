from typing import List, Optional
from bson import ObjectId
from app.schemas.guide import GuideCreate, GuideUpdate
from app.core.database import get_database
import logging

logger = logging.getLogger(__name__)


class GuideService:
    """Service pour gérer les guides touristiques"""
    
    def __init__(self):
        self.collection_name = "guides"
    
    async def create_guide(self, guide: GuideCreate) -> str:
        """Créer un nouveau guide"""
        try:
            guide_dict = guide.model_dump()
            result = await self.collection.insert_one(guide_dict)
            logger.info(f"Guide créé: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Erreur lors de la création d'un guide: {e}")
            raise
    
    async def get_guide(self, guide_id: str) -> Optional[dict]:
        """Récupérer un guide par ID"""
        try:
            guide = await self.collection.find_one({"_id": ObjectId(guide_id)})
            if guide:
                guide["id"] = str(guide["_id"])
            return guide
        except Exception as e:
            logger.error(f"Erreur lors de la récupération du guide: {e}")
            raise
    
    async def get_all_guides(self, skip: int = 0, limit: int = 10) -> List[dict]:
        """Récupérer tous les guides"""
        try:
            guides = []
            async for guide in self.collection.find({"actif": True}).skip(skip).limit(limit):
                guide["id"] = str(guide["_id"])
                guides.append(guide)
            return guides
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des guides: {e}")
            raise
    
    async def get_guides_by_city(self, ville: str) -> List[dict]:
        """Récupérer les guides par ville"""
        try:
            guides = []
            async for guide in self.collection.find({"ville": ville, "actif": True}):
                guide["id"] = str(guide["_id"])
                guides.append(guide)
            return guides
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des guides par ville: {e}")
            raise
    
    async def get_guides_by_language(self, langue: str) -> List[dict]:
        """Récupérer les guides parlant une langue"""
        try:
            guides = []
            async for guide in self.collection.find({
                "langues": langue,
                "actif": True
            }):
                guide["id"] = str(guide["_id"])
                guides.append(guide)
            return guides
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des guides par langue: {e}")
            raise
    
    async def get_guides_by_specialty(self, specialite: str) -> List[dict]:
        """Récupérer les guides par spécialité"""
        try:
            guides = []
            async for guide in self.collection.find({
                "specialites": specialite,
                "actif": True
            }):
                guide["id"] = str(guide["_id"])
                guides.append(guide)
            return guides
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des guides par spécialité: {e}")
            raise
    
    async def get_guides_with_vehicle(self) -> List[dict]:
        """Récupérer les guides disposant d'un véhicule"""
        try:
            guides = []
            async for guide in self.collection.find({
                "possede_vehicule": True,
                "actif": True
            }):
                guide["id"] = str(guide["_id"])
                guides.append(guide)
            return guides
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des guides avec véhicule: {e}")
            raise
    
    async def update_guide(self, guide_id: str, guide_update: GuideUpdate) -> bool:
        """Mettre à jour un guide"""
        try:
            update_data = guide_update.model_dump(exclude_unset=True)
            if update_data:
                result = await self.collection.update_one(
                    {"_id": ObjectId(guide_id)},
                    {"$set": update_data}
                )
                logger.info(f"Guide mis à jour: {guide_id}")
                return result.modified_count > 0
            return False
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour du guide: {e}")
            raise
    
    async def delete_guide(self, guide_id: str) -> bool:
        """Supprimer un guide"""
        try:
            result = await self.collection.delete_one({"_id": ObjectId(guide_id)})
            logger.info(f"Guide supprimé: {guide_id}")
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Erreur lors de la suppression du guide: {e}")
            raise
    
    async def get_top_rated_guides(self, limit: int = 5) -> List[dict]:
        """Récupérer les guides les mieux notés"""
        try:
            guides = []
            async for guide in self.collection.find({"actif": True, "verified": True}).sort("note_moyenne", -1).limit(limit):
                guide["id"] = str(guide["_id"])
                guides.append(guide)
            return guides
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des meilleurs guides: {e}")
            raise
