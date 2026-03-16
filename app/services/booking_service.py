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
    
    async def create_booking(self, booking: BookingCreate, client_id: str) -> str:
        """Créer une réservation"""
        try:
            db = get_database()
            booking_dict = booking.model_dump()
            # Ajouter les champs de gestion
            booking_dict["client_id"] = client_id
            booking_dict["statut_reservation"] = "en_attente"
            booking_dict["statut_paiement"] = "non_paye"
            booking_dict["date_creation"] = datetime.utcnow()
            booking_dict["date_modification"] = datetime.utcnow()
            result = await db[self.collection_name].insert_one(booking_dict)
            logger.info(f"Réservation créée: {result.inserted_id} pour client {client_id}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Erreur lors de la création d'une réservation: {e}")
            raise
    
    async def get_booking(self, booking_id: str) -> Optional[dict]:
        """Récupérer une réservation par ID"""
        try:
            db = get_database()
            booking = await db[self.collection_name].find_one({"_id": ObjectId(booking_id)})
            if booking:
                booking["id"] = str(booking["_id"])
            return booking
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de la réservation: {e}")
            raise
    
    async def get_bookings_by_client(self, email_client: str, skip: int = 0, limit: int = 100) -> List[dict]:
        """Récupérer les réservations d'un client (par client_id ou client_email)"""
        try:
            db = get_database()
            bookings = []
            # Chercher par client_id (user_id) OU client_email
            query = {"$or": [{"client_id": email_client}, {"client_email": email_client}]}
            async for booking in db[self.collection_name].find(query).skip(skip).limit(limit):
                booking["id"] = str(booking["_id"])
                bookings.append(booking)
            return bookings
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des réservations du client: {e}")
            raise
    
    async def get_bookings_by_resource(self, ressource_id: str) -> List[dict]:
        """Récupérer les réservations pour une ressource"""
        try:
            db = get_database()
            bookings = []
            async for booking in db[self.collection_name].find({"ressource_id": ressource_id}):
                booking["id"] = str(booking["_id"])
                bookings.append(booking)
            return bookings
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des réservations: {e}")
            raise

    async def get_bookings_by_guide(self, guide_id: str, skip: int = 0, limit: int = 100) -> List[dict]:
        """Récupérer les réservations assignées à un guide."""
        try:
            db = get_database()
            bookings = []

            # Compatibilité: certaines réservations historiques peuvent stocker
            # soit user_id du guide, soit l'id du profil guide dans guide_id/ressource_id.
            profile_id = None
            try:
                guide_doc = await db["guides"].find_one({"user_id": guide_id})
                if guide_doc and guide_doc.get("_id"):
                    profile_id = str(guide_doc["_id"])
            except Exception:
                profile_id = None

            or_conditions = [
                {"guide_id": guide_id},
                {"type_reservation": "guide", "ressource_id": guide_id},
            ]

            if profile_id:
                or_conditions.extend([
                    {"guide_id": profile_id},
                    {"type_reservation": "guide", "ressource_id": profile_id},
                ])

            query = {"$or": or_conditions}

            async for booking in db[self.collection_name].find(query).skip(skip).limit(limit):
                booking["id"] = str(booking["_id"])
                bookings.append(booking)
            return bookings
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des réservations du guide: {e}")
            raise
    
    async def get_bookings_by_status(self, statut: str) -> List[dict]:
        """Récupérer les réservations par statut"""
        try:
            db = get_database()
            bookings = []
            async for booking in db[self.collection_name].find({"statut_reservation": statut}):
                booking["id"] = str(booking["_id"])
                bookings.append(booking)
            return bookings
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des réservations par statut: {e}")
            raise
    
    async def update_booking(self, booking_id: str, booking_update: BookingUpdate) -> bool:
        """Mettre à jour une réservation"""
        try:
            db = get_database()
            update_data = booking_update.model_dump(exclude_unset=True)
            if update_data:
                update_data["date_modification"] = datetime.utcnow()
                result = await db[self.collection_name].update_one(
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
            db = get_database()
            result = await db[self.collection_name].update_one(
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
    
    async def get_all_bookings(self, skip: int = 0, limit: int = 100) -> List[dict]:
        """Récupérer toutes les réservations (ADMIN)"""
        try:
            db = get_database()
            bookings = []
            async for booking in db[self.collection_name].find().skip(skip).limit(limit):
                booking["id"] = str(booking["_id"])
                bookings.append(booking)
            return bookings
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de toutes les réservations: {e}")
            raise

    async def get_high_value_bookings(self, min_amount: float) -> List[dict]:
        """Récupérer les réservations de haute valeur (ADMIN)"""
        try:
            db = get_database()
            bookings = []
            async for booking in db[self.collection_name].find({"montant_final_fcfa": {"$gte": min_amount}}):
                booking["id"] = str(booking["_id"])
                bookings.append(booking)
            return bookings
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des réservations haute valeur: {e}")
            raise

    async def get_revenue_by_date_range(self, date_start: datetime, date_end: datetime) -> float:
        """Calcul des revenus pour une plage de dates"""
        try:
            db = get_database()
            result = await db[self.collection_name].aggregate([
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
