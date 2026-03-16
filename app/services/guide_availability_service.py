"""
Service pour la gestion de la disponibilité des guides
"""
from datetime import datetime, timedelta
from typing import List, Optional
from bson import ObjectId
from app.core.database import get_database
from app.models.guide_availability import GuideAvailability, AvailabilityStatus
from app.schemas.guide_availability import (
    AvailabilitySlotCreate,
    AvailabilitySlotUpdate,
    BulkAvailabilityCreate,
    AvailabilityCheckRequest
)


class GuideAvailabilityService:
    """Service pour gérer les disponibilités des guides"""
    
    def __init__(self):
        self.collection_name = "guide_availabilities"
    
    async def create_availability_slot(
        self,
        guide_id: str,
        slot_data: AvailabilitySlotCreate
    ) -> str:
        """Créer une nouvelle plage de disponibilité"""
        db = get_database()
        
        # Vérifier s'il y a déjà une plage qui chevauche
        overlapping = await self.check_overlapping_slots(
            guide_id,
            slot_data.date,
            slot_data.start_time,
            slot_data.end_time
        )
        
        if overlapping:
            raise ValueError("Une plage de disponibilité existe déjà pour cette période")
        
        # Créer la nouvelle plage
        availability_data = {
            "guide_id": guide_id,
            "date": slot_data.date,
            "start_time": slot_data.start_time,
            "end_time": slot_data.end_time,
            "status": AvailabilityStatus.AVAILABLE,
            "notes": slot_data.notes,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = await db[self.collection_name].insert_one(availability_data)
        return str(result.inserted_id)
    
    async def create_bulk_availability(
        self,
        guide_id: str,
        bulk_data: BulkAvailabilityCreate
    ) -> List[str]:
        """Créer plusieurs plages de disponibilité en une fois"""
        db = get_database()
        created_ids = []
        
        for date in bulk_data.dates:
            # Vérifier les chevauchements
            overlapping = await self.check_overlapping_slots(
                guide_id,
                date,
                bulk_data.start_time,
                bulk_data.end_time
            )
            
            if not overlapping:
                availability_data = {
                    "guide_id": guide_id,
                    "date": date,
                    "start_time": bulk_data.start_time,
                    "end_time": bulk_data.end_time,
                    "status": AvailabilityStatus.AVAILABLE,
                    "notes": bulk_data.notes,
                    "created_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }
                
                result = await db[self.collection_name].insert_one(availability_data)
                created_ids.append(str(result.inserted_id))
        
        return created_ids
    
    async def get_guide_availability(
        self,
        guide_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        status: Optional[AvailabilityStatus] = None
    ) -> List[dict]:
        """Récupérer les disponibilités d'un guide"""
        db = get_database()
        
        # Construire le filtre
        filter_query = {"guide_id": guide_id}
        
        if start_date and end_date:
            filter_query["date"] = {"$gte": start_date, "$lte": end_date}
        elif start_date:
            filter_query["date"] = {"$gte": start_date}
        elif end_date:
            filter_query["date"] = {"$lte": end_date}
        
        if status:
            filter_query["status"] = status
        
        # Récupérer et trier par date et heure
        cursor = db[self.collection_name].find(filter_query).sort([
            ("date", 1),
            ("start_time", 1)
        ])
        
        availabilities = []
        async for doc in cursor:
            doc["id"] = str(doc["_id"])
            availabilities.append(doc)
        
        return availabilities
    
    async def update_availability_slot(
        self,
        slot_id: str,
        guide_id: str,
        update_data: AvailabilitySlotUpdate
    ) -> bool:
        """Mettre à jour une plage de disponibilité"""
        db = get_database()
        
        # Vérifier que la plage appartient bien au guide
        slot = await db[self.collection_name].find_one({
            "_id": ObjectId(slot_id),
            "guide_id": guide_id
        })
        
        if not slot:
            return False
        
        # Préparer les données de mise à jour
        update_dict = {}
        if update_data.date is not None:
            update_dict["date"] = update_data.date
        if update_data.start_time is not None:
            update_dict["start_time"] = update_data.start_time
        if update_data.end_time is not None:
            update_dict["end_time"] = update_data.end_time
        if update_data.status is not None:
            update_dict["status"] = update_data.status
        if update_data.notes is not None:
            update_dict["notes"] = update_data.notes
        
        update_dict["updated_at"] = datetime.utcnow()
        
        # Mettre à jour
        result = await db[self.collection_name].update_one(
            {"_id": ObjectId(slot_id)},
            {"$set": update_dict}
        )
        
        return result.modified_count > 0
    
    async def delete_availability_slot(
        self,
        slot_id: str,
        guide_id: str
    ) -> bool:
        """Supprimer une plage de disponibilité"""
        db = get_database()
        
        # Vérifier que la plage appartient bien au guide et n'est pas réservée
        slot = await db[self.collection_name].find_one({
            "_id": ObjectId(slot_id),
            "guide_id": guide_id
        })
        
        if not slot:
            return False
        
        if slot.get("status") == AvailabilityStatus.BOOKED:
            raise ValueError("Impossible de supprimer une plage réservée")
        
        result = await db[self.collection_name].delete_one({"_id": ObjectId(slot_id)})
        return result.deleted_count > 0
    
    async def check_overlapping_slots(
        self,
        guide_id: str,
        date: str,
        start_time: str,
        end_time: str,
        exclude_slot_id: Optional[str] = None
    ) -> bool:
        """Vérifier s'il existe des plages qui se chevauchent"""
        db = get_database()
        
        filter_query = {
            "guide_id": guide_id,
            "date": date,
            "$or": [
                # Nouvelle plage commence pendant une plage existante
                {
                    "start_time": {"$lte": start_time},
                    "end_time": {"$gt": start_time}
                },
                # Nouvelle plage se termine pendant une plage existante
                {
                    "start_time": {"$lt": end_time},
                    "end_time": {"$gte": end_time}
                },
                # Nouvelle plage englobe une plage existante
                {
                    "start_time": {"$gte": start_time},
                    "end_time": {"$lte": end_time}
                }
            ]
        }
        
        if exclude_slot_id:
            filter_query["_id"] = {"$ne": ObjectId(exclude_slot_id)}
        
        count = await db[self.collection_name].count_documents(filter_query)
        return count > 0
    
    async def check_availability(
        self,
        check_request: AvailabilityCheckRequest
    ) -> dict:
        """Vérifier si un guide est disponible pour une période donnée"""
        db = get_database()
        
        # Chercher les plages qui chevauchent
        conflicting_slots = await db[self.collection_name].find({
            "guide_id": check_request.guide_id,
            "date": check_request.date,
            "$or": [
                {
                    "start_time": {"$lte": check_request.start_time},
                    "end_time": {"$gt": check_request.start_time}
                },
                {
                    "start_time": {"$lt": check_request.end_time},
                    "end_time": {"$gte": check_request.end_time}
                },
                {
                    "start_time": {"$gte": check_request.start_time},
                    "end_time": {"$lte": check_request.end_time}
                }
            ]
        }).to_list(length=100)
        
        # Convertir les ObjectId
        for slot in conflicting_slots:
            slot["id"] = str(slot["_id"])
        
        # Vérifier s'il y a des conflits
        has_conflicts = any(
            slot["status"] in [AvailabilityStatus.BOOKED, AvailabilityStatus.BLOCKED]
            for slot in conflicting_slots
        )
        
        available_slot_exists = any(
            slot["status"] == AvailabilityStatus.AVAILABLE
            for slot in conflicting_slots
        )
        
        if has_conflicts:
            return {
                "available": False,
                "conflicting_slots": conflicting_slots,
                "message": "Le guide n'est pas disponible pour cette période"
            }
        elif available_slot_exists:
            return {
                "available": True,
                "conflicting_slots": conflicting_slots,
                "message": "Le guide est disponible"
            }
        else:
            return {
                "available": False,
                "conflicting_slots": [],
                "message": "Aucune disponibilité définie pour cette période"
            }
    
    async def mark_slot_as_booked(
        self,
        guide_id: str,
        date: str,
        start_time: str,
        end_time: str,
        booking_id: str
    ) -> bool:
        """Marquer une plage comme réservée"""
        db = get_database()
        
        result = await db[self.collection_name].update_one(
            {
                "guide_id": guide_id,
                "date": date,
                "start_time": start_time,
                "end_time": end_time,
                "status": AvailabilityStatus.AVAILABLE
            },
            {
                "$set": {
                    "status": AvailabilityStatus.BOOKED,
                    "booking_id": booking_id,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        return result.modified_count > 0
    
    async def release_booked_slot(
        self,
        booking_id: str
    ) -> bool:
        """Libérer une plage réservée (annulation de réservation)"""
        db = get_database()
        
        result = await db[self.collection_name].update_one(
            {"booking_id": booking_id},
            {
                "$set": {
                    "status": AvailabilityStatus.AVAILABLE,
                    "booking_id": None,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        return result.modified_count > 0
