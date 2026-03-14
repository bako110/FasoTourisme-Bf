from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime


class Guide(BaseModel):
    """Modèle pour les guides touristiques"""
    
    id: Optional[str] = Field(None, alias="_id")
    
    # Informations personnelles
    nom: str = Field(..., description="Nom du guide")
    prenom: str = Field(..., description="Prénom du guide")
    photo: Optional[str] = Field(None, description="Photo du guide")
    
    # Contact
    telephone: str = Field(..., description="Numéro de téléphone")
    email: Optional[str] = Field(None, description="Adresse email")
    
    # Localisation
    ville: str = Field(..., description="Ville de résidence")
    region: str = Field(..., description="Région de résidence")
    
    # Qualification
    langues: List[str] = Field(
        ...,
        description="Langues parlées: français, anglais, mooré, dioula, etc."
    )
    specialites: List[str] = Field(
        default=[],
        description="Spécialités: faune, histoire, culture, géologie, etc."
    )
    
    # Certification et expérience
    licence_guide: bool = Field(True, description="Guide officiellement agréé?")
    date_obtention_licence: Optional[datetime] = None
    articles_guides: Optional[str] = Field(None, description="Articles ou numéro de licence")
    
    # Expérience
    annees_experience: int = Field(..., ge=0, description="Années d'expérience")
    destinations_principales: List[str] = Field(
        default=[],
        description="Destinations principales"
    )
    
    # Services
    tarif_journee_fcfa: float = Field(..., description="Tarif par jour en FCFA")
    tarif_demi_journee_fcfa: Optional[float] = Field(None, description="Tarif demi-journée en FCFA")
    
    biographie: Optional[str] = Field(None, description="Biographie du guide")
    
    # Véhicule personnel
    possede_vehicule: bool = Field(False)
    type_vehicule: Optional[str] = Field(None, description="Type de véhicule si disponible")
    
    # Disponibilité
    disponible: bool = Field(True)
    jours_disponibilite: List[str] = Field(
        default=["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"],
        description="Jours de disponibilité"
    )
    
    # Évaluations
    note_moyenne: float = Field(default=0, ge=0, le=5)
    nombre_avis: int = Field(default=0)
    nombre_clients_satisfaits: int = Field(default=0)
    
    # Relations
    activites_animees: List[str] = Field(default=[], description="IDs des activités animées")
    destinations_reconnues: List[str] = Field(default=[], description="IDs des destinations couvertes")
    
    # Métadonnées
    actif: bool = Field(True, description="Le profil est-il actif?")
    verified: bool = Field(False, description="Profil vérifié par l'administration?")
    date_inscription: datetime = Field(default_factory=datetime.utcnow)
    date_modification: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "nom": "Traore",
                "prenom": "Aminata",
                "telephone": "+226 70 00 00 00",
                "email": "aminata.traore@example.com",
                "ville": "Ouagadougou",
                "region": "Kadiogo",
                "langues": ["français", "mooré", "dioula", "anglais"],
                "specialites": ["faune", "histoire", "culture"],
                "annees_experience": 8,
                "destinations_principales": ["Parc du W", "Cascade de Banfora"],
                "tarif_journee_fcfa": 35000,
                "licence_guide": True,
                "note_moyenne": 4.8
            }
        }
