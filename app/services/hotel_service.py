from typing import List, Optional
from bson import ObjectId
from app.schemas.hotel import HotelCreate, HotelUpdate
from app.core.database import get_database
import logging

logger = logging.getLogger(__name__)


class HotelService:
    """Service pour gérer les hôtels"""
    
    def __init__(self, db=None):
        self.collection_name = "hotels"
        db = db or get_database()
        self.collection = db[self.collection_name]

    def _to_response_dict(self, hotel: dict) -> dict:
        """Normalise un document hôtel pour le schéma de réponse."""
        if not hotel:
            return hotel

        if "_id" in hotel:
            hotel["id"] = str(hotel["_id"])

        hotel.setdefault("types_chambres", [])
        hotel.setdefault("services", [])
        hotel.setdefault("equipements", [])
        hotel.setdefault("galerie_images", [])
        hotel.setdefault("note_moyenne", 0.0)
        hotel.setdefault("nombre_evaluations", 0)
        hotel.setdefault("publie", True)
        return hotel
    
    async def create_hotel(self, hotel: HotelCreate, owner_id: Optional[str] = None) -> str:
        """Créer un nouvel hôtel"""
        try:
            hotel_dict = hotel.model_dump()
            hotel_dict["owner_id"] = owner_id
            hotel_dict.setdefault("note_moyenne", 0.0)
            hotel_dict.setdefault("nombre_evaluations", 0)
            hotel_dict.setdefault("publie", True)
            result = await self.collection.insert_one(hotel_dict)
            logger.info(f"Hôtel créé: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Erreur lors de la création d'un hôtel: {e}")
            raise
    
    async def get_hotel(self, hotel_id: str) -> Optional[dict]:
        """Récupérer un hôtel par ID"""
        try:
            hotel = await self.collection.find_one({"_id": ObjectId(hotel_id)})
            return self._to_response_dict(hotel) if hotel else None
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de l'hôtel: {e}")
            raise
    
    async def get_all_hotels(self, skip: int = 0, limit: int = 10) -> List[dict]:
        """Récupérer tous les hôtels"""
        try:
            hotels = []
            async for hotel in self.collection.find({}).skip(skip).limit(limit):
                hotels.append(self._to_response_dict(hotel))
            return hotels
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des hôtels: {e}")
            raise
    
    async def get_hotels_by_city(self, ville: str) -> List[dict]:
        """Récupérer les hôtels par ville"""
        try:
            hotels = []
            async for hotel in self.collection.find({"ville": ville}):
                hotels.append(self._to_response_dict(hotel))
            return hotels
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des hôtels par ville: {e}")
            raise
    
    async def get_hotels_by_category(self, categorie: str) -> List[dict]:
        """Récupérer les hôtels par catégorie"""
        try:
            hotels = []
            async for hotel in self.collection.find({"categorie": categorie}):
                hotels.append(self._to_response_dict(hotel))
            return hotels
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des hôtels par catégorie: {e}")
            raise
    
    async def get_hotels_by_price_range(self, min_price: float, max_price: float) -> List[dict]:
        """Récupérer les hôtels par gamme de prix"""
        try:
            hotels = []
            async for hotel in self.collection.find({
                "tarif_nuit_min_fcfa": {"$gte": min_price},
                "tarif_nuit_max_fcfa": {"$lte": max_price}
            }):
                hotels.append(self._to_response_dict(hotel))
            return hotels
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des hôtels par prix: {e}")
            raise
    
    async def update_hotel(self, hotel_id: str, hotel_update: HotelUpdate) -> bool:
        """Mettre à jour un hôtel"""
        try:
            update_data = hotel_update.model_dump(exclude_unset=True)
            if update_data:
                result = await self.collection.update_one(
                    {"_id": ObjectId(hotel_id)},
                    {"$set": update_data}
                )
                logger.info(f"Hôtel mis à jour: {hotel_id}")
                return result.modified_count > 0
            return False
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour de l'hôtel: {e}")
            raise
    
    async def delete_hotel(self, hotel_id: str) -> bool:
        """Supprimer un hôtel"""
        try:
            result = await self.collection.delete_one({"_id": ObjectId(hotel_id)})
            logger.info(f"Hôtel supprimé: {hotel_id}")
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Erreur lors de la suppression de l'hôtel: {e}")
            raise
    
    async def get_top_rated_hotels(self, limit: int = 5) -> List[dict]:
        """Récupérer les hôtels les mieux notés"""
        try:
            hotels = []
            async for hotel in self.collection.find({"publie": True}).sort("note_moyenne", -1).limit(limit):
                hotels.append(self._to_response_dict(hotel))
            return hotels
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des meilleurs hôtels: {e}")
            raise
