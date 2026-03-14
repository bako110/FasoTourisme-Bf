from typing import List, Optional
from bson import ObjectId
from app.schemas.cuisine import CuisineCreate, CuisineUpdate
from app.core.database import get_database
import logging

logger = logging.getLogger(__name__)


class CuisineService:
    """Service pour gérer les restaurants et plats locaux"""
    
    def __init__(self):
        self.collection_name = "cuisines"
    
    async def create_restaurant(self, cuisine: CuisineCreate) -> str:
        """Créer un profil de restaurant"""
        try:
            db = get_database()
            cuisine_dict = cuisine.model_dump()
            result = await db[self.collection_name].insert_one(cuisine_dict)
            logger.info(f"Restaurant créé: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Erreur lors de la création du restaurant: {e}")
            raise
    
    async def get_restaurants_by_city(self, ville: str) -> List[dict]:
        """Récupérer les restaurants par ville"""
        try:
            restaurants = []
            async for restaurant in self.collection.find({
                "ville": ville,
                "actif": True
            }):
                restaurant["id"] = str(restaurant["_id"])
                restaurants.append(restaurant)
            return restaurants
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des restaurants: {e}")
            raise
    
    async def get_restaurants_by_type(self, type_restaurant: str) -> List[dict]:
        """Récupérer les restaurants par type"""
        try:
            restaurants = []
            async for restaurant in self.collection.find({
                "type_restaurant": type_restaurant,
                "actif": True
            }):
                restaurant["id"] = str(restaurant["_id"])
                restaurants.append(restaurant)
            return restaurants
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des restaurants par type: {e}")
            raise
    
    async def get_restaurants_by_budget(self, max_budget: float) -> List[dict]:
        """Récupérer les restaurants selon le budget"""
        try:
            restaurants = []
            async for restaurant in self.collection.find({
                "budget_moyen_fcfa": {"$lte": max_budget},
                "actif": True
            }):
                restaurant["id"] = str(restaurant["_id"])
                restaurants.append(restaurant)
            return restaurants
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des restaurants par budget: {e}")
            raise
    
    async def get_authentic_local_restaurants(self) -> List[dict]:
        """Récupérer les restaurants authentiques utilisant des produits locaux"""
        try:
            restaurants = []
            async for restaurant in self.collection.find({
                "utilise_produits_locaux": True,
                "recettes_traditionelles": True,
                "actif": True
            }).sort("note_moyenne", -1):
                restaurant["id"] = str(restaurant["_id"])
                restaurants.append(restaurant)
            return restaurants
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des restaurants authentiques: {e}")
            raise
    
    async def get_top_rated_restaurants(self, limit: int = 10) -> List[dict]:
        """Récupérer les restaurants les mieux notés"""
        try:
            restaurants = []
            async for restaurant in self.collection.find({
                "actif": True
            }).sort("note_moyenne", -1).limit(limit):
                restaurant["id"] = str(restaurant["_id"])
                restaurants.append(restaurant)
            return restaurants
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des meilleurs restaurants: {e}")
            raise
