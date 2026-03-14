from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ReviewCreate(BaseModel):
    """Schéma pour créer un avis"""
    type_ressource: str
    ressource_id: str
    client_nom: str
    client_email: Optional[str] = None
    pays_origine: Optional[str] = None
    note: int
    titre_avis: str
    commentaire: str
    note_accueil: Optional[int] = None
    note_qualite: Optional[int] = None
    note_service: Optional[int] = None
    note_prix: Optional[int] = None
    date_experience: Optional[datetime] = None
    photos: List[str] = []


class ReviewUpdate(BaseModel):
    """Schéma pour mettre à jour un avis"""
    note: Optional[int] = None
    titre_avis: Optional[str] = None
    commentaire: Optional[str] = None
    note_accueil: Optional[int] = None
    note_qualite: Optional[int] = None
    note_service: Optional[int] = None
    note_prix: Optional[int] = None
    photos: Optional[List[str]] = None


class ReviewResponse(BaseModel):
    """Schéma de réponse pour un avis"""
    id: Optional[str] = None
    type_ressource: str
    ressource_id: str
    client_nom: str
    note: int
    titre_avis: str
    commentaire: str
    date_creation: datetime
    approuve: bool
    utile_count: int
    
    class Config:
        populate_by_name = True
