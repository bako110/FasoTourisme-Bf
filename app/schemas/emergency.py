from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class EmergencyCreate(BaseModel):
    """Schéma pour créer un service d'urgence"""
    type_urgence: str
    nom_organisme: str
    ville_siege: str
    region_siege: str
    adresse_siege: str
    numero_urgence_principal: str
    zones_couvertes: List[str]
    disponible_24h: bool = True


class EmergencyUpdate(BaseModel):
    """Schéma pour mettre à jour un service d'urgence"""
    type_urgence: Optional[str] = None
    nom_organisme: Optional[str] = None
    numero_urgence_principal: Optional[str] = None
    zones_couvertes: Optional[List[str]] = None
    disponible_24h: Optional[bool] = None


class EmergencyResponse(BaseModel):
    """Schéma de réponse pour un service d'urgence"""
    id: Optional[str] = None
    type_urgence: str
    nom_organisme: str
    numero_urgence_principal: str
    disponible_24h: bool
    zones_couvertes: List[str]
    temps_reponse_moyen_minutes: Optional[int]
    
    class Config:
        populate_by_name = True
