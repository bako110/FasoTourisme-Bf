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
    image: Optional[str] = None
    images: List[str] = []
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
    image: Optional[str] = None
    images: Optional[List[str]] = None
    video_url: Optional[str] = None
    note_moyenne: Optional[float] = None
    publie: Optional[bool] = None


class DestinationResponse(BaseModel):
    """Schéma de réponse pour une destination"""
    id: Optional[str] = None
    nom: str
    description: str
    region: str
    province: str
    localite: str
    type_destination: str
    categorie: Optional[List[str]] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    altitude: Optional[float] = None
    temps_acces_heures: Optional[float] = None
    meilleure_saison: Optional[List[str]] = None
    acces_securise: Optional[bool] = None
    tarif_entree_fcfa: Optional[float] = None
    tarif_guide_fcfa: Optional[float] = None
    image_principale: Optional[object] = None  # Peut être string ou dict
    galerie_images: Optional[List[object]] = None  # Peut être list de strings ou dicts
    images: Optional[List[object]] = None  # Support pour le format 'images' du seed
    video_url: Optional[str] = None
    note_moyenne: Optional[float] = None
    nombre_evaluations: Optional[int] = None
    publie: Optional[bool] = None
    date_creation: Optional[datetime] = None
    date_modification: Optional[datetime] = None
    _id: Optional[str] = None  # Pour compatibilité MongoDB
    
    class Config:
        populate_by_name = True
        extra = "allow"  # Permets les champs extra du MongoDB
