from pydantic import BaseModel
from typing import Optional, List


class GuideCreate(BaseModel):
    """Schéma pour créer un guide"""
    nom: str
    prenom: str
    telephone: str
    email: Optional[str] = None
    photo: Optional[str] = None
    ville: str
    region: str
    langues: List[str]
    specialites: List[str] = []
    licence_guide: bool = True
    articles_guides: Optional[str] = None
    annees_experience: int
    destinations_principales: List[str] = []
    tarif_journee_fcfa: float
    tarif_demi_journee_fcfa: Optional[float] = None
    biographie: Optional[str] = None
    possede_vehicule: bool = False
    type_vehicule: Optional[str] = None
    disponible: bool = True
    jours_disponibilite: List[str] = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]


class GuideUpdate(BaseModel):
    """Schéma pour mettre à jour un guide"""
    nom: Optional[str] = None
    prenom: Optional[str] = None
    telephone: Optional[str] = None
    email: Optional[str] = None
    photo: Optional[str] = None
    ville: Optional[str] = None
    region: Optional[str] = None
    langues: Optional[List[str]] = None
    specialites: Optional[List[str]] = None
    licence_guide: Optional[bool] = None
    articles_guides: Optional[str] = None
    annees_experience: Optional[int] = None
    destinations_principales: Optional[List[str]] = None
    tarif_journee_fcfa: Optional[float] = None
    tarif_demi_journee_fcfa: Optional[float] = None
    biographie: Optional[str] = None
    possede_vehicule: Optional[bool] = None
    type_vehicule: Optional[str] = None
    disponible: Optional[bool] = None
    jours_disponibilite: Optional[List[str]] = None
    note_moyenne: Optional[float] = None
    actif: Optional[bool] = None


class GuideResponse(BaseModel):
    """Schéma de réponse pour un guide"""
    id: Optional[str] = None
    nom: str
    prenom: str
    telephone: str
    email: Optional[str]
    photo: Optional[str]
    ville: str
    region: str
    langues: List[str]
    specialites: List[str]
    licence_guide: bool
    articles_guides: Optional[str]
    annees_experience: int
    destinations_principales: List[str]
    tarif_journee_fcfa: float
    tarif_demi_journee_fcfa: Optional[float]
    biographie: Optional[str]
    possede_vehicule: bool
    type_vehicule: Optional[str]
    disponible: bool
    jours_disponibilite: List[str]
    note_moyenne: float
    nombre_avis: int
    nombre_clients_satisfaits: int
    actif: bool
    verified: bool
    
    class Config:
        populate_by_name = True
