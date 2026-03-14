from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class StoryCreate(BaseModel):
    """Schéma pour créer une histoire de visiteur"""
    visiteur_nom: str
    visiteur_prenom: Optional[str] = None
    email_visiteur: Optional[str] = None
    pays_origine: str
    titre_histoire: str
    histoire: str
    destinations_visitees: List[str]
    date_visite: datetime
    duree_sejour_jours: int
    type_voyageur: str = "solo"
    moments_marquants: str
    rencontres_interessantes: Optional[str] = None
    apprentissages: Optional[str] = None
    veut_revenir: bool = True
    conseil_voyageurs: Optional[str] = None


class StoryUpdate(BaseModel):
    """Schéma pour mettre à jour une histoire"""
    titre_histoire: Optional[str] = None
    histoire: Optional[str] = None
    destinations_visitees: Optional[List[str]] = None
    moments_marquants: Optional[str] = None
    rencontres_interessantes: Optional[str] = None
    apprentissages: Optional[str] = None
    veut_revenir: Optional[bool] = None
    conseil_voyageurs: Optional[str] = None


class StoryResponse(BaseModel):
    """Schéma de réponse pour une histoire de visiteur"""
    id: Optional[str] = None
    visiteur_nom: str
    pays_origine: str
    titre_histoire: str
    histoire: str
    date_visite: datetime
    type_voyageur: str
    moments_marquants: str
    veut_revenir: bool
    publie: bool
    mise_en_avant: bool
    date_creation: datetime
    
    class Config:
        populate_by_name = True
