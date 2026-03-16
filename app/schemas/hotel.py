from pydantic import BaseModel, EmailStr
from typing import Optional, List


class HotelCreate(BaseModel):
    """Schéma pour créer un hôtel"""
    nom: str
    description: str
    ville: str
    region: str
    adresse: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    categorie: str
    nombre_etoiles: int
    nombre_chambres: int
    types_chambres: List[str] = []
    tarif_nuit_min_fcfa: float
    tarif_nuit_max_fcfa: float
    petit_dejeuner_inclus: bool = False
    services: List[str] = []
    equipements: List[str] = []
    telephone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    image: Optional[str] = None
    images: List[str] = []


class HotelUpdate(BaseModel):
    """Schéma pour mettre à jour un hôtel"""
    nom: Optional[str] = None
    description: Optional[str] = None
    ville: Optional[str] = None
    region: Optional[str] = None
    adresse: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    categorie: Optional[str] = None
    nombre_etoiles: Optional[int] = None
    nombre_chambres: Optional[int] = None
    types_chambres: Optional[List[str]] = None
    tarif_nuit_min_fcfa: Optional[float] = None
    tarif_nuit_max_fcfa: Optional[float] = None
    petit_dejeuner_inclus: Optional[bool] = None
    services: Optional[List[str]] = None
    equipements: Optional[List[str]] = None
    telephone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    image: Optional[str] = None
    images: Optional[List[str]] = None
    note_moyenne: Optional[float] = None
    publie: Optional[bool] = None


class HotelResponse(BaseModel):
    """Schéma de réponse pour un hôtel"""
    id: Optional[str] = None
    nom: str
    description: str
    ville: str
    region: str
    adresse: str
    latitude: Optional[float]
    longitude: Optional[float]
    categorie: str
    nombre_etoiles: int
    nombre_chambres: int
    types_chambres: List[str]
    tarif_nuit_min_fcfa: float
    tarif_nuit_max_fcfa: float
    petit_dejeuner_inclus: bool
    services: List[str]
    equipements: List[str]
    telephone: Optional[str]
    email: Optional[str]
    website: Optional[str]
    image_principale: Optional[str]
    galerie_images: List[str]
    note_moyenne: float
    nombre_evaluations: int
    publie: bool
    
    class Config:
        populate_by_name = True
