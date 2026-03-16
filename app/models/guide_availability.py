"""
Modèle pour la gestion de la disponibilité des guides
"""
from datetime import datetime, time
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum


class AvailabilityStatus(str, Enum):
    """Statut de disponibilité"""
    AVAILABLE = "available"  # Disponible
    BOOKED = "booked"  # Réservé
    BLOCKED = "blocked"  # Bloqué par le guide


class GuideAvailability(BaseModel):
    """
    Représente une plage de disponibilité d'un guide
    """
    id: Optional[str] = Field(None, alias="_id")
    guide_id: str  # ID du guide
    date: str  # Date au format YYYY-MM-DD
    start_time: str  # Heure de début (format HH:MM)
    end_time: str  # Heure de fin (format HH:MM)
    status: AvailabilityStatus = AvailabilityStatus.AVAILABLE
    booking_id: Optional[str] = None  # ID de la réservation si status=BOOKED
    notes: Optional[str] = None  # Notes optionnelles
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "guide_id": "507f1f77bcf86cd799439011",
                "date": "2026-03-20",
                "start_time": "09:00",
                "end_time": "17:00",
                "status": "available",
                "notes": "Disponible pour visites touristiques"
            }
        }
