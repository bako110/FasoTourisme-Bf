"""
Schémas Pydantic pour la gestion de la disponibilité des guides
"""
from datetime import datetime, time
from typing import Optional, List
from pydantic import BaseModel, Field, validator
from app.models.guide_availability import AvailabilityStatus


class AvailabilitySlotCreate(BaseModel):
    """Créer une plage de disponibilité"""
    date: str  # YYYY-MM-DD
    start_time: str  # HH:MM
    end_time: str  # HH:MM
    notes: Optional[str] = None
    
    @validator('date')
    def validate_date_format(cls, v):
        """Valider le format de date"""
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Format de date invalide. Utilisez YYYY-MM-DD')
    
    @validator('start_time', 'end_time')
    def validate_time_format(cls, v):
        """Valider le format d'heure"""
        try:
            datetime.strptime(v, '%H:%M')
            return v
        except ValueError:
            raise ValueError('Format d\'heure invalide. Utilisez HH:MM')
    
    @validator('end_time')
    def validate_end_after_start(cls, v, values):
        """Vérifier que l'heure de fin est après l'heure de début"""
        if 'start_time' in values:
            start = datetime.strptime(values['start_time'], '%H:%M').time()
            end = datetime.strptime(v, '%H:%M').time()
            if end <= start:
                raise ValueError('L\'heure de fin doit être après l\'heure de début')
        return v


class AvailabilitySlotUpdate(BaseModel):
    """Mettre à jour une plage de disponibilité"""
    date: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    status: Optional[AvailabilityStatus] = None
    notes: Optional[str] = None
    
    @validator('date')
    def validate_date_format(cls, v):
        """Valider le format de date"""
        if v is not None:
            try:
                datetime.strptime(v, '%Y-%m-%d')
                return v
            except ValueError:
                raise ValueError('Format de date invalide. Utilisez YYYY-MM-DD')
        return v
    
    @validator('start_time', 'end_time')
    def validate_time_format(cls, v):
        """Valider le format d'heure"""
        if v is not None:
            try:
                datetime.strptime(v, '%H:%M')
                return v
            except ValueError:
                raise ValueError('Format d\'heure invalide. Utilisez HH:MM')
        return v


class AvailabilitySlotResponse(BaseModel):
    """Réponse d'une plage de disponibilité"""
    id: str
    guide_id: str
    date: str
    start_time: str
    end_time: str
    status: AvailabilityStatus
    booking_id: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class BulkAvailabilityCreate(BaseModel):
    """Créer plusieurs plages de disponibilité en une fois"""
    dates: List[str]  # Liste de dates YYYY-MM-DD
    start_time: str  # HH:MM
    end_time: str  # HH:MM
    notes: Optional[str] = None
    
    @validator('dates')
    def validate_dates(cls, v):
        """Valider les formats de dates"""
        for date_str in v:
            try:
                datetime.strptime(date_str, '%Y-%m-%d')
            except ValueError:
                raise ValueError(f'Format de date invalide: {date_str}. Utilisez YYYY-MM-DD')
        return v
    
    @validator('start_time', 'end_time')
    def validate_time_format(cls, v):
        """Valider le format d'heure"""
        try:
            datetime.strptime(v, '%H:%M')
            return v
        except ValueError:
            raise ValueError('Format d\'heure invalide. Utilisez HH:MM')


class AvailabilityCheckRequest(BaseModel):
    """Vérifier la disponibilité d'un guide"""
    guide_id: str
    date: str  # YYYY-MM-DD
    start_time: str  # HH:MM
    end_time: str  # HH:MM


class AvailabilityCheckResponse(BaseModel):
    """Réponse de vérification de disponibilité"""
    available: bool
    conflicting_slots: List[AvailabilitySlotResponse] = []
    message: str
