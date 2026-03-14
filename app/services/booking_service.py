from typing import List, Optional
from bson import ObjectId
from app.schemas.booking import BookingCreate, BookingUpdate
from app.core.database import get_database
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BookingService:
    """Service pour gérer les réservations"""
    
    def __init__(self):
        self.collection_name = "bookings"
    
    async def create_booking(self, booking: BookingCreate) -> str:
        """Créer une réservation"""
        try:
            booking_dict = booking.model_dump()
            result = await self.collection.insert_one(booking_dict)
            logger.info(f"Réservation créée: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Erreur lors de la création d'une réservation: {e}")
            raise
    
    async def get_booking(self, booking_id: str) -> Optional[dict]:
        """Récupérer une réservation par ID"""
        try:
            booking = await self.collection.find_one({"_id": ObjectId(booking_id)})
            if booking:
                booking["id"] = str(booking["_id"])
            return booking
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de la réservation: {e}")
            raise
    
    async def get_bookings_by_client(self, email_client: str) -> List[dict]:
        """Récupérer les réservations d'un client"""
        try:
            bookings = []
            async for booking in self.collection.find({"client_email": email_client}):
                booking["id"] = str(booking["_id"])
                bookings.append(booking)
            return bookings
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des réservations du client: {e}")
            raise
    
    async def get_bookings_by_resource(self, ressource_id: str) -> List[dict]:
        """Récupérer les réservations pour une ressource"""
        try:
            bookings = []
            async for booking in self.collection.find({"ressource_id": ressource_id}):
                booking["id"] = str(booking["_id"])
                bookings.append(booking)
            return bookings
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des réservations: {e}")
            raise
    
    async def get_bookings_by_status(self, statut: str) -> List[dict]:
        """Récupérer les réservations par statut"""
        try:
            bookings = []
            async for booking in self.collection.find({"statut_reservation": statut}):
                booking["id"] = str(booking["_id"])
                bookings.append(booking)
            return bookings
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des réservations par statut: {e}")
            raise
    
    async def update_booking(self, booking_id: str, booking_update: BookingUpdate) -> bool:
        """Mettre à jour une réservation"""
        try:
            update_data = booking_update.model_dump(exclude_unset=True)
            if update_data:
                result = await self.collection.update_one(
                    {"_id": ObjectId(booking_id)},
                    {"$set": update_data}
                )
                return result.modified_count > 0
            return False
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour de la réservation: {e}")
            raise
    
    async def cancel_booking(self, booking_id: str, raison: str) -> bool:
        """Annuler une réservation"""
        try:
            result = await self.collection.update_one(
                {"_id": ObjectId(booking_id)},
                {"$set": {
                    "statut_reservation": "annulee",
                    "date_annulation": datetime.utcnow(),
                    "raison_annulation": raison
                }}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Erreur lors de l'annulation de la réservation: {e}")
            raise
    
    async def get_revenue_by_date_range(self, date_start: datetime, date_end: datetime) -> float:
        """Calcul des revenus pour une plage de dates"""
        try:
            result = await self.collection.aggregate([
                {
                    "$match": {
                        "date_creation": {"$gte": date_start, "$lte": date_end},
                        "statut_paiement": "paye"
                    }
                },
                {
                    "$group": {
                        "_id": None,
                        "total": {"$sum": "$montant_final_fcfa"}
                    }
                }
            ]).to_list(None)
            return result[0]["total"] if result else 0
        except Exception as e:
            logger.error(f"Erreur lors du calcul des revenus: {e}")
            raise
