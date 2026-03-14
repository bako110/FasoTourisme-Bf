from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    """Rôles utilisateur disponibles"""
    ADMIN = "admin"  # Accès complet, gestion du système, validation providers
    TOURIST = "tourist"  # Visite sites, réserve, publie avis/histoires
    GUIDE = "guide"  # Profil guide touristique
    PROVIDER = "provider"  # Artisan ou Restaurant (prestataires)
    MODERATOR = "moderator"  # Modération contenu sensible


class User(BaseModel):
    """Modèle utilisateur MongoDB"""
    id: Optional[str] = Field(None, alias="_id")
    email: EmailStr
    telephone: Optional[str] = None  # Numéro de téléphone pour connexion alternative
    nom_complet: str
    motdepasse_hash: str  # Jamais stocker en clair!
    role: UserRole = UserRole.TOURIST
    actif: bool = True
    verifiee: bool = False  # Email vérifié
    
    # Pour les GUIDE et PROVIDER : lien vers profil métier
    profil_type: Optional[str] = None  # "guide", "artisan", "restaurant"
    profil_id: Optional[str] = None  # ID du guide/provider associé
    
    # Pour PROVIDER : statut de vérification du profil métier
    profil_verifiee: bool = False  # Vérification du profil business (par ADMIN)
    
    # Métadonnées
    date_creation: datetime = Field(default_factory=datetime.utcnow)
    date_derniere_connexion: Optional[datetime] = None
    adresse_ip_derniere_connexion: Optional[str] = None
    
    # Permissions additionnelles
    permissions_specifiques: List[str] = []
    
    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class UserPublic(BaseModel):
    """Schéma utilisateur pour les réponses publiques"""
    id: Optional[str] = None
    email: str
    telephone: Optional[str] = None
    nom_complet: str
    role: UserRole
    actif: bool
    verifiee: bool
    profil_type: Optional[str] = None
    profil_verifiee: bool = False
    date_creation: datetime
    
    class Config:
        populate_by_name = True
