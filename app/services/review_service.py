from typing import List, Optional
from bson import ObjectId
from app.schemas.review import ReviewCreate, ReviewUpdate
from app.core.database import get_database
import logging

logger = logging.getLogger(__name__)


class ReviewService:
    """Service pour gérer les avis clients"""
    
    def __init__(self):
        self.collection_name = "reviews"
    
    async def create_review(self, review: ReviewCreate) -> str:
        """Créer un avis"""
        try:
            review_dict = review.model_dump()
            result = await self.collection.insert_one(review_dict)
            logger.info(f"Avis créé: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Erreur lors de la création d'un avis: {e}")
            raise
    
    async def get_reviews_by_resource(self, type_ressource: str, ressource_id: str) -> List[dict]:
        """Récupérer les avis pour une ressource"""
        try:
            reviews = []
            async for review in self.collection.find({
                "type_ressource": type_ressource,
                "ressource_id": ressource_id,
                "approuve": True
            }).sort("date_creation", -1):
                review["id"] = str(review["_id"])
                reviews.append(review)
            return reviews
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des avis: {e}")
            raise
    
    async def get_average_rating(self, type_ressource: str, ressource_id: str) -> dict:
        """Calculer la note moyenne pour une ressource"""
        try:
            result = await self.collection.aggregate([
                {
                    "$match": {
                        "type_ressource": type_ressource,
                        "ressource_id": ressource_id,
                        "approuve": True
                    }
                },
                {
                    "$group": {
                        "_id": None,
                        "note_moyenne": {"$avg": "$note"},
                        "nombre_avis": {"$sum": 1}
                    }
                }
            ]).to_list(None)
            
            if result:
                return {
                    "note_moyenne": round(result[0]["note_moyenne"], 1),
                    "nombre_avis": result[0]["nombre_avis"]
                }
            return {"note_moyenne": 0, "nombre_avis": 0}
        except Exception as e:
            logger.error(f"Erreur lors du calcul de la note moyenne: {e}")
            raise
    
    async def mark_helpful(self, review_id: str) -> bool:
        """Marquer un avis comme utile"""
        try:
            result = await self.collection.update_one(
                {"_id": ObjectId(review_id)},
                {"$inc": {"utile_count": 1}}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Erreur lors du marquage de l'avis: {e}")
            raise
    
    async def get_top_reviews(self, limit: int = 5) -> List[dict]:
        """Récupérer les meilleurs avis"""
        try:
            reviews = []
            async for review in self.collection.find({"approuve": True}).sort("note", -1).limit(limit):
                review["id"] = str(review["_id"])
                reviews.append(review)
            return reviews
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des meilleurs avis: {e}")
            raise
