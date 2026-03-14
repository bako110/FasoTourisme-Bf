from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class SecurityCreate(BaseModel):
    """Schéma pour créer une alerte de sécurité"""
    type_alerte: str
    niveau_risque: str
    ville: str
    region: str
    province: str
    aire_affectee: str
    description_alerte: str
    date_debut: datetime
    recommandation_touristes: str
    source_information: str
    frequence_incidents: str = "ponctuel"


class SecurityUpdate(BaseModel):
    """Schéma pour mettre à jour une alerte de sécurité"""
    type_alerte: Optional[str] = None
    niveau_risque: Optional[str] = None
    aire_affectee: Optional[str] = None
    description_alerte: Optional[str] = None
    recommandation_touristes: Optional[str] = None
    frequence_incidents: Optional[str] = None


class SecurityResponse(BaseModel):
    """Schéma de réponse pour une alerte"""
    id: Optional[str] = None
    type_alerte: str
    niveau_risque: str
    ville: str
    aire_affectee: str
    description_alerte: str
    date_debut: datetime
    recommandation_touristes: str
    actif: bool
    
    class Config:
        populate_by_name = True
