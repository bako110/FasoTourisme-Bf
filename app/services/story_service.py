from typing import List, Optional
from bson import ObjectId
from app.schemas.story import StoryCreate, StoryUpdate
from app.core.database import get_database
import logging

logger = logging.getLogger(__name__)


class StoryService:
    """Service pour gérer les histoires de visiteurs"""
    
    def __init__(self):
        self.collection_name = "stories"
    
    async def create_story(self, story: StoryCreate) -> str:
        """Créer une histoire de visiteur"""
        try:
            db = get_database()
            story_dict = story.model_dump()
            result = await db[self.collection_name].insert_one(story_dict)
            logger.info(f"Histoire créée: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Erreur lors de la création de l'histoire: {e}")
            raise
    
    async def get_published_stories(self, skip: int = 0, limit: int = 10) -> List[dict]:
        """Récupérer les histoires publiées"""
        try:
            stories = []
            async for story in self.collection.find({
                "publie": True,
                "approuve": True
            }).sort("date_creation", -1).skip(skip).limit(limit):
                story["id"] = str(story["_id"])
                stories.append(story)
            return stories
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des histoires: {e}")
            raise
    
    async def get_featured_stories(self, limit: int = 5) -> List[dict]:
        """Récupérer les histoires mises en avant"""
        try:
            stories = []
            async for story in self.collection.find({
                "publie": True,
                "approuve": True,
                "mise_en_avant": True
            }).sort("date_creation", -1).limit(limit):
                story["id"] = str(story["_id"])
                stories.append(story)
            return stories
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des histoires en avant: {e}")
            raise
    
    async def get_stories_by_origin(self, pays: str) -> List[dict]:
        """Récupérer les histoires par pays d'origine"""
        try:
            stories = []
            async for story in self.collection.find({
                "pays_origine": pays,
                "publie": True,
                "approuve": True
            }):
                story["id"] = str(story["_id"])
                stories.append(story)
            return stories
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des histoires par pays: {e}")
            raise
    
    async def get_stories_by_traveler_type(self, type_voyageur: str) -> List[dict]:
        """Récupérer les histoires par type de voyageur"""
        try:
            stories = []
            async for story in self.collection.find({
                "type_voyageur": type_voyageur,
                "publie": True,
                "approuve": True
            }):
                story["id"] = str(story["_id"])
                stories.append(story)
            return stories
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des histoires: {e}")
            raise
    
    async def get_stories_by_destination(self, destination_id: str) -> List[dict]:
        """Récupérer les histoires pour une destination"""
        try:
            stories = []
            async for story in self.collection.find({
                "destinations_visitees": destination_id,
                "publie": True,
                "approuve": True
            }):
                story["id"] = str(story["_id"])
                stories.append(story)
            return stories
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des histoires: {e}")
            raise
