from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class HealthAdvisoryCreate(BaseModel):
    """Schéma pour créer un avis de santé"""
    type_alerte: str
    nom_maladie: str
    niveau_gravite: str
    villes_affectees: List[str]
    regions: List[str]
    mode_transmission: Optional[List[str]] = None
    mesures_prevention: List[str]
    source: str
    date_information: datetime


class HealthAdvisoryUpdate(BaseModel):
    """Schéma pour mettre à jour un avis de santé"""
    type_alerte: Optional[str] = None
    nom_maladie: Optional[str] = None
    niveau_gravite: Optional[str] = None
    villes_affectees: Optional[List[str]] = None
    regions: Optional[List[str]] = None
    mesures_prevention: Optional[List[str]] = None


class HealthAdvisoryResponse(BaseModel):
    """Schéma de réponse pour un avis de santé"""
    id: Optional[str] = None
    type_alerte: str
    nom_maladie: str
    niveau_gravite: str
    villes_affectees: List[str]
    regions: List[str]
    risque_pour_touristes: str
    vaccin_disponible: Optional[bool]
    mesures_prevention: List[str]
    actif: bool
    
    class Config:
        populate_by_name = True
