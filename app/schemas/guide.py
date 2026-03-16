from pydantic import BaseModel, Field
from typing import Optional, List


class GuideProfileCreate(BaseModel):
    """Schéma pour créer/compléter le profil guide depuis mobile"""
    user_id: str
    nom_complet: str
    bio: Optional[str] = None
    telephone: str
    langues_parlees: List[str]
    specialites: List[str] = []
    tarif_journee: float
    experience_annees: int
    certifications: List[str] = []
    regions_couvertes: List[str] = []

    disponible: bool = True
    photo: Optional[str] = None
    possede_vehicule: bool = False
    type_vehicule: Optional[str] = None
    tours_proposes: List[str] = []


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
    tours_proposes: List[str] = []


class GuideUpdate(BaseModel):
    """Schéma pour mettre à jour un guide"""
    nom: Optional[str] = None
    prenom: Optional[str] = None
    telephone: Optional[str] = None
    email: Optional[str] = None
    photo: Optional[str] = None
    ville: Optional[str] = None
    region: Optional[str] = None
    langues: Optional[List[str]] = Field(None, alias="langues_parlees")
    specialites: Optional[List[str]] = None
    licence_guide: Optional[bool] = None
    articles_guides: Optional[str] = None
    annees_experience: Optional[int] = Field(None, alias="experience_annees")
    destinations_principales: Optional[List[str]] = Field(None, alias="regions_couvertes")
    tarif_journee_fcfa: Optional[float] = Field(None, alias="tarif_journee")
    tarif_demi_journee_fcfa: Optional[float] = None
    biographie: Optional[str] = Field(None, alias="bio")
    possede_vehicule: Optional[bool] = None
    type_vehicule: Optional[str] = None
    disponible: Optional[bool] = None

    jours_disponibilite: Optional[List[str]] = None
    note_moyenne: Optional[float] = None
    actif: Optional[bool] = None
    certifications: Optional[List[str]] = None
    tours_proposes: Optional[List[str]] = None
    
    class Config:
        populate_by_name = True  # Accepter à la fois "langues" et "langues_parlees"


class GuideResponse(BaseModel):
    """Schéma de réponse pour un guide"""
    id: Optional[str] = None
    nom: str
    prenom: str
    nom_complet: Optional[str] = None
    telephone: str
    email: Optional[str]
    photo: Optional[str] = None  # URL de la photo du guide
    photo_profil: Optional[str] = None  # URL de la photo du guide
    ville: str
    region: str
    langues: List[str] = Field(default_factory=list, alias="langues_parlees")
    specialites: List[str] = Field(default_factory=list)
    licence_guide: bool
    articles_guides: Optional[str]
    annees_experience: int = Field(alias="experience_annees")
    destinations_principales: List[str] = Field(default_factory=list, alias="regions_couvertes")
    tarif_journee_fcfa: float = Field(alias="tarif_journee")
    tarif_demi_journee_fcfa: Optional[float]
    biographie: Optional[str] = Field(None, alias="bio")
    possede_vehicule: bool
    type_vehicule: Optional[str]
    disponible: bool
    jours_disponibilite: List[str]
    note_moyenne: float
    nombre_avis: int
    nombre_clients_satisfaits: int
    certifications: List[str] = Field(default_factory=list)

    actif: bool
    verified: bool
    tours_proposes: List[str] = []
    
    class Config:
        populate_by_name = True
        from_attributes = True
        extra = "allow"  # Permettre les champs supplémentaires du MongoDB
