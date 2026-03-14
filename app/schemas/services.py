from pydantic import BaseModel
from typing import Optional, List


class EssentialServiceCreate(BaseModel):
    """Schéma pour créer un service essentiel"""
    type_service: str
    provider_name: str
    ville: str
    region: str
    province: str
    localite: str
    est_operationnel: bool = True
    qualite_service: str = "moyenne"
    accessible_touristes: bool = True


class EssentialServiceUpdate(BaseModel):
    """Schéma pour mettre à jour un service essentiel"""
    type_service: Optional[str] = None
    provider_name: Optional[str] = None
    est_operationnel: Optional[bool] = None
    qualite_service: Optional[str] = None
    accessible_touristes: Optional[bool] = None


class EssentialServiceResponse(BaseModel):
    """Schéma de réponse pour un service essentiel"""
    id: Optional[str] = None
    type_service: str
    provider_name: str
    ville: str
    region: str
    est_operationnel: bool
    qualite_service: str
    taux_disponibilite_pourcent: Optional[float]
    
    class Config:
        populate_by_name = True
