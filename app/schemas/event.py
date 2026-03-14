from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class EventCreate(BaseModel):
    """Schéma pour créer un événement local"""
    nom: str
    description: str
    type_evenement: str
    ville: str
    region: str
    province: str
    localite: str
    lieu: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    date_debut: datetime
    date_fin: datetime
    recurrence: Optional[str] = None
    gratuit: bool = True
    tarif_entree_fcfa: Optional[float] = None
    description_culturelle: str
    communaute_hote: str
    activites: List[str] = []
    conseil_visite: Optional[str] = None


class EventUpdate(BaseModel):
    """Schéma pour mettre à jour un événement local"""
    nom: Optional[str] = None
    description: Optional[str] = None
    type_evenement: Optional[str] = None
    ville: Optional[str] = None
    date_debut: Optional[datetime] = None
    date_fin: Optional[datetime] = None
    gratuit: Optional[bool] = None
    tarif_entree_fcfa: Optional[float] = None
    description_culturelle: Optional[str] = None
    activites: Optional[List[str]] = None
    conseil_visite: Optional[str] = None


class EventResponse(BaseModel):
    """Schéma de réponse pour un événement"""
    id: Optional[str] = None
    nom: str
    description: str
    type_evenement: str
    ville: str
    region: str
    date_debut: datetime
    date_fin: datetime
    gratuit: bool
    description_culturelle: str
    activites: List[str]
    image_principale: Optional[str]
    
    class Config:
        populate_by_name = True
