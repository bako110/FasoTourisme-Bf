from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class HealthCreate(BaseModel):
    """Schéma pour créer une installation sanitaire"""
    nom: str
    type_etablissement: str
    ville: str
    region: str
    province: str
    localite: str
    adresse: str
    latitude: float
    longitude: float
    telephone_principal: str
    horaires_ouverture: str
    services: List[str]
    ouvert_24h: bool = False
    equipements: List[str] = []


class HealthUpdate(BaseModel):
    """Schéma pour mettre à jour une installation sanitaire"""
    nom: Optional[str] = None
    type_etablissement: Optional[str] = None
    telephone_principal: Optional[str] = None
    horaires_ouverture: Optional[str] = None
    services: Optional[List[str]] = None
    ouvert_24h: Optional[bool] = None
    equipements: Optional[List[str]] = None


class HealthResponse(BaseModel):
    """Schéma de réponse pour une installation sanitaire"""
    id: Optional[str] = None
    nom: str
    type_etablissement: str
    ville: str
    region: str
    adresse: str
    telephone_principal: str
    latitude: float
    longitude: float
    services: List[str]
    ouvert_24h: bool
    urgence_disponible: bool
    
    class Config:
        populate_by_name = True
