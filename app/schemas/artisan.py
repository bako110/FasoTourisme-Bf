from pydantic import BaseModel
from typing import Optional, List


class ArtisanCreate(BaseModel):
    """Schéma pour créer un profil d'artisan"""
    nom: str
    prenom: Optional[str] = None
    type_artisan: str
    nom_entreprise: str
    ville: str
    region: str
    province: str
    localite: str
    telephone: str
    email: Optional[str] = None
    description: str
    histoire_artisan: str
    annees_experience: int
    produits: List[str]
    matiere_premiere_locale: bool = True
    visite_atelier_possible: bool = True
    tarif_visite: Optional[float] = None
    demonstration_possible: bool = True
    employes: int = 1


class ArtisanUpdate(BaseModel):
    """Schéma pour mettre à jour un artisan"""
    nom: Optional[str] = None
    type_artisan: Optional[str] = None
    nom_entreprise: Optional[str] = None
    description: Optional[str] = None
    histoire_artisan: Optional[str] = None
    telephone: Optional[str] = None
    email: Optional[str] = None
    produits: Optional[List[str]] = None
    tarif_visite: Optional[float] = None
    employes: Optional[int] = None


class ArtisanResponse(BaseModel):
    """Schéma de réponse pour un artisan"""
    id: Optional[str] = None
    nom: str
    type_artisan: str
    nom_entreprise: str
    ville: str
    region: str
    telephone: str
    description: str
    histoire_artisan: str
    annees_experience: int
    produits: List[str]
    visite_atelier_possible: bool
    demonstration_possible: bool
    note_moyenne: float
    
    class Config:
        populate_by_name = True
