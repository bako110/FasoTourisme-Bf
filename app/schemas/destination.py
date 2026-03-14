from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class DestinationCreate(BaseModel):
    """Schéma pour créer une destination"""
    nom: str
    description: str
    region: str
    province: str
    localite: str
    type_destination: str
    categorie: List[str] = []
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    altitude: Optional[float] = None
    temps_acces_heures: Optional[float] = None
    meilleure_saison: List[str] = []
    acces_securise: bool = True
    tarif_entree_fcfa: Optional[float] = None
    tarif_guide_fcfa: Optional[float] = None
    image_principale: Optional[str] = None
    galerie_images: List[str] = []
    video_url: Optional[str] = None


class DestinationUpdate(BaseModel):
    """Schéma pour mettre à jour une destination"""
    nom: Optional[str] = None
    description: Optional[str] = None
    region: Optional[str] = None
    province: Optional[str] = None
    localite: Optional[str] = None
    type_destination: Optional[str] = None
    categorie: Optional[List[str]] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    altitude: Optional[float] = None
    temps_acces_heures: Optional[float] = None
    meilleure_saison: Optional[List[str]] = None
    acces_securise: Optional[bool] = None
    tarif_entree_fcfa: Optional[float] = None
    tarif_guide_fcfa: Optional[float] = None
    image_principale: Optional[str] = None
    galerie_images: Optional[List[str]] = None
    video_url: Optional[str] = None
    note_moyenne: Optional[float] = None
    publie: Optional[bool] = None


class DestinationResponse(BaseModel):
    """Schéma de réponse pour une destination"""
    id: Optional[str] = Field(None, alias="_id")
    nom: str
    description: str
    region: str
    province: str
    localite: str
    type_destination: str
    categorie: List[str]
    latitude: Optional[float]
    longitude: Optional[float]
    altitude: Optional[float]
    temps_acces_heures: Optional[float]
    meilleure_saison: List[str]
    acces_securise: bool
    tarif_entree_fcfa: Optional[float]
    tarif_guide_fcfa: Optional[float]
    image_principale: Optional[str]
    galerie_images: List[str]
    video_url: Optional[str]
    note_moyenne: float
    nombre_evaluations: int
    publie: bool
    date_creation: datetime
    date_modification: datetime
    
    class Config:
        populate_by_name = True
