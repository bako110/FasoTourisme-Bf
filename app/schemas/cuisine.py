from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class CuisineCreate(BaseModel):
    """Schéma pour créer un restaurant local"""
    nom: str
    description: str
    type_restaurant: str
    ville: str
    region: str
    province: str
    localite: str
    adresse: str
    specialites: List[str]
    cuisine_type: str
    budget_moyen_fcfa: float
    proprietaire_nom: str
    utilise_produits_locaux: bool = True
    visite_atelier_possible: bool = True
    employes_locaux: int = 0
    apprentissage_jeunes: bool = False


class CuisineUpdate(BaseModel):
    """Schéma pour mettre à jour un restaurant"""
    nom: Optional[str] = None
    description: Optional[str] = None
    type_restaurant: Optional[str] = None
    specialites: Optional[List[str]] = None
    cuisine_type: Optional[str] = None
    budget_moyen_fcfa: Optional[float] = None
    proprietaire_nom: Optional[str] = None
    utilise_produits_locaux: Optional[bool] = None
    employes_locaux: Optional[int] = None
    apprentissage_jeunes: Optional[bool] = None


class CuisineResponse(BaseModel):
    """Schéma de réponse pour un restaurant"""
    id: Optional[str] = None
    nom: str
    type_restaurant: str
    ville: str
    specialites: List[str]
    cuisine_type: str
    budget_moyen_fcfa: float
    proprietaire_nom: str
    utilise_produits_locaux: bool
    note_moyenne: float
    plat_populaire: Optional[str]
    
    class Config:
        populate_by_name = True
