from typing import List, Optional
from bson import ObjectId
from app.schemas.event import EventCreate, EventUpdate
from app.core.database import get_database
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class EventService:
    """Service pour gérer les événements locaux"""
    
    def __init__(self):
        self.collection_name = "events"
    
    async def create_event(self, event: EventCreate) -> str:
        """Créer un événement"""
        try:
            db = get_database()
            event_dict = event.model_dump()
            result = await db[self.collection_name].insert_one(event_dict)
            logger.info(f"Événement créé: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Erreur lors de la création d'un événement: {e}")
            raise
    
    async def get_upcoming_events(self, limit: int = 10) -> List[dict]:
        """Récupérer les événements à venir"""
        try:
            events = []
            async for event in self.collection.find({
                "date_debut": {"$gte": datetime.utcnow()},
                "publie": True
            }).sort("date_debut", 1).limit(limit):
                event["id"] = str(event["_id"])
                events.append(event)
            return events
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des événements à venir: {e}")
            raise
    
    async def get_events_by_region(self, region: str) -> List[dict]:
        """Récupérer les événements par région"""
        try:
            events = []
            async for event in self.collection.find({
                "region": region,
                "publie": True
            }).sort("date_debut", 1):
                event["id"] = str(event["_id"])
                events.append(event)
            return events
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des événements par région: {e}")
            raise
    
    async def get_events_by_type(self, type_evenement: str) -> List[dict]:
        """Récupérer les événements par type"""
        try:
            events = []
            async for event in self.collection.find({
                "type_evenement": type_evenement,
                "publie": True
            }).sort("date_debut", 1):
                event["id"] = str(event["_id"])
                events.append(event)
            return events
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des événements par type: {e}")
            raise
    
    async def get_event(self, event_id: str) -> Optional[dict]:
        """Récupérer un événement par ID"""
        try:
            event = await self.collection.find_one({"_id": ObjectId(event_id)})
            if event:
                event["id"] = str(event["_id"])
            return event
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de l'événement: {e}")
            raise
