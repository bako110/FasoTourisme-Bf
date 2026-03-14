from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum


class ProviderType(str, Enum):
    """Types de prestataires de services touristiques"""
    HOTEL = "hotel"
    RESTAURANT = "restaurant"
    ARTISAN = "artisan"
    TRANSPORT = "transport"
    PHARMACIE = "pharmacie"
    AGENCE = "agence"
    LOCATION = "location"
    COMMERCE = "commerce"
    SERVICE = "service"


class Provider(BaseModel):
    """
    Modèle Provider UNIFIÉ pour tous les prestataires touristiques
    Support de 9 types de services : Hôtels, Restaurants, Artisans, Transport, 
    Pharmacies, Agences, Location, Commerce, Services
    """
    id: Optional[str] = Field(None, alias="_id")
    
    # Informations de base
    nom_entreprise: str = Field(..., min_length=3, max_length=200)
    type_service: ProviderType  # Type de service touristique
    description: str = Field(..., min_length=10, max_length=2000)
    
    # Propriétaire (liaison avec User)
    owner_id: str  # ID du User propriétaire
    owner_email: EmailStr
    owner_phone: Optional[str] = None
    
    # Localisation
    ville: str
    region: str
    province: str
    localite: str
    adresse: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    
    # Services/Produits (adaptatif selon type)
    produits_services: List[str] = []  # Services proposés selon le type de provider
    specialites: Optional[str] = None  # Description libre des spécialités
    
    # Contact & Horaires
    telephone: str
    horaires_ouverture: Optional[str] = None  # "Lun-Sam: 9h-18h, Dim: 12h-17h"
    website: Optional[str] = None
    
    # Tarification (générique pour tous types)
    tarif_base: Optional[float] = None  # Tarif de base du service
    
    # Champs génériques (optionnels selon type)
    annees_experience: Optional[int] = None
    employes: Optional[int] = None
    utilise_produits_locaux: Optional[bool] = None
    
    # Champs spécialisés (legacy - optionnels)
    budget_moyen_fcfa: Optional[float] = None  # Pour restaurants
    tarif_visite_fcfa: Optional[float] = None  # Pour artisans
    matiere_premiere_locale: Optional[bool] = None  # Pour artisans
    demonstration_possible: Optional[bool] = None  # Pour artisans
    cuisine_type: Optional[str] = None  # Pour restaurants
    employes_locaux: Optional[int] = None  # Pour restaurants
    apprentissage_jeunes: Optional[bool] = None  # Pour restaurants
    
    # Vérification & Notation
    verified: bool = False  # Vérifié par ADMIN
    note_moyenne: float = 0.0
    nombre_avis: int = 0
    
    # Engagement/Valeurs
    description_culturelle: Optional[str] = None
    engagement_communaute: Optional[str] = None
    
    # Métadonnées
    date_creation: datetime = Field(default_factory=datetime.utcnow)
    date_modification: datetime = Field(default_factory=datetime.utcnow)
    actif: bool = True
    publie: bool = False
    
    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ProviderCreate(BaseModel):
    """Schéma création provider - Compatible avec frontend TypeScript"""
    nom_entreprise: str = Field(..., min_length=3)
    type_service: ProviderType
    description: str = Field(..., min_length=10)
    ville: str
    region: str
    province: str
    localite: str
    adresse: str
    produits_services: List[str]
    telephone: str
    owner_phone: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    horaires_ouverture: Optional[str] = None
    website: Optional[str] = None
    
    # Champs existants du frontend (legacy)
    budget_moyen_fcfa: Optional[float] = None
    tarif_visite_fcfa: Optional[float] = None
    annees_experience: Optional[int] = None
    matiere_premiere_locale: Optional[bool] = None
    employes: Optional[int] = None
    cuisine_type: Optional[str] = None
    utilise_produits_locaux: Optional[bool] = None
    employes_locaux: Optional[int] = None
    description_culturelle: Optional[str] = None


class ProviderUpdate(BaseModel):
    """Schéma mise à jour provider - Compatible avec frontend TypeScript"""
    nom_entreprise: Optional[str] = None
    description: Optional[str] = None
    produits_services: Optional[List[str]] = None
    telephone: Optional[str] = None
    horaires_ouverture: Optional[str] = None
    website: Optional[str] = None
    budget_moyen_fcfa: Optional[float] = None
    tarif_visite_fcfa: Optional[float] = None
    employes: Optional[int] = None
    utilise_produits_locaux: Optional[bool] = None
    employes_locaux: Optional[int] = None
    description_culturelle: Optional[str] = None
    actif: Optional[bool] = None


class ProviderResponse(BaseModel):
    """Réponse provider pour API publique"""
    id: str
    nom_entreprise: str
    type_service: ProviderType
    description: str
    ville: str
    region: str
    adresse: str
    produits_services: List[str]
    telephone: str
    note_moyenne: float
    nombre_avis: int
    verified: bool
    actif: bool
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    
    class Config:
        populate_by_name = True
