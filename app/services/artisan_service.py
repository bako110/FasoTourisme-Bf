from typing import List, Optional
from bson import ObjectId
from app.schemas.artisan import ArtisanCreate, ArtisanUpdate
from app.core.database import get_database
import logging

logger = logging.getLogger(__name__)


class ArtisanService:
    """Service pour gérer les artisans locaux"""
    
    def __init__(self):
        self.collection_name = "artisans"
    
    async def create_artisan(self, artisan: ArtisanCreate) -> str:
        """Créer un profil d'artisan"""
        try:
            db = get_database()
            artisan_dict = artisan.model_dump()
            result = await db[self.collection_name].insert_one(artisan_dict)
            logger.info(f"Artisan créé: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Erreur lors de la création d'un artisan: {e}")
            raise
    
    async def get_artisans_by_type(self, type_artisan: str) -> List[dict]:
        """Récupérer les artisans par type"""
        try:
            artisans = []
            async for artisan in self.collection.find({
                "type_artisan": type_artisan,
                "actif": True
            }):
                artisan["id"] = str(artisan["_id"])
                artisans.append(artisan)
            return artisans
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des artisans: {e}")
            raise
    
    async def get_artisans_by_city(self, ville: str) -> List[dict]:
        """Récupérer les artisans par ville"""
        try:
            artisans = []
            async for artisan in self.collection.find({
                "ville": ville,
                "actif": True
            }):
                artisan["id"] = str(artisan["_id"])
                artisans.append(artisan)
            return artisans
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des artisans par ville: {e}")
            raise
    
    async def get_artisans_with_visits(self) -> List[dict]:
        """Récupérer les artisans offrant des visites d'atelier"""
        try:
            artisans = []
            async for artisan in self.collection.find({
                "visite_atelier_possible": True,
                "actif": True
            }):
                artisan["id"] = str(artisan["_id"])
                artisans.append(artisan)
            return artisans
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des artisans avec visite: {e}")
            raise
    
    async def get_top_rated_artisans(self, limit: int = 5) -> List[dict]:
        """Récupérer les artisans les mieux notés"""
        try:
            artisans = []
            async for artisan in self.collection.find({
                "actif": True,
                "verified": True
            }).sort("note_moyenne", -1).limit(limit):
                artisan["id"] = str(artisan["_id"])
                artisans.append(artisan)
            return artisans
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des meilleurs artisans: {e}")
            raise
