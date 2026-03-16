from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class Hotel(BaseModel):
    """Modèle pour les hôtels et hébergements"""
    
    id: Optional[str] = Field(None, alias="_id")
    nom: str = Field(..., description="Nom de l'hôtel")
    description: str = Field(..., description="Description de l'établissement")
    
    # Localisation
    ville: str = Field(..., description="Ville où se trouve l'hôtel")
    region: str = Field(..., description="Région")
    adresse: str = Field(..., description="Adresse complète")
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    
    # Classification
    categorie: str = Field(
        ..., 
        description="Catégorie: luxe, haut_standing, standard, budget, auberge"
    )
    nombre_etoiles: int = Field(1, ge=1, le=5, description="Nombre d'étoiles")
    
    # Chambres
    nombre_chambres: int = Field(..., description="Nombre total de chambres")
    types_chambres: List[str] = Field(
        default=[], 
        description="Types de chambres: simple, double, suite, duplex, etc."
    )
    
    # Tarifs
    tarif_nuit_min_fcfa: float = Field(..., description="Tarif minimum par nuit en FCFA")
    tarif_nuit_max_fcfa: float = Field(..., description="Tarif maximum par nuit en FCFA")
    petit_dejeuner_inclus: bool = Field(False)
    
    # Services et équipements
    services: List[str] = Field(
        default=[],
        description="Services: wifi, parking, restaurant, bar, piscine, gym, spa, etc."
    )
    equipements: List[str] = Field(
        default=[],
        description="Équipements: climatisation, chauffage, tv, minibar, etc."
    )
    
    # Contact
    telephone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    
    # Images
    image: Optional[str] = None
    images: List[str] = Field(default=[])
    
    # Évaluations
    note_moyenne: float = Field(default=0, ge=0, le=5)
    nombre_evaluations: int = Field(default=0)
    
    # Métadonnées
    publie: bool = Field(True)
    date_creation: datetime = Field(default_factory=datetime.utcnow)
    date_modification: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "nom": "Hôtel Splendid",
                "description": "Hôtel haut standing au cœur de Ouagadougou",
                "ville": "Ouagadougou",
                "region": "Kadiogo",
                "adresse": "Avenue Kléber, Ouagadougou",
                "categorie": "haut_standing",
                "nombre_etoiles": 4,
                "nombre_chambres": 50,
                "tarif_nuit_min_fcfa": 35000,
                "tarif_nuit_max_fcfa": 100000,
                "services": ["wifi", "restaurant", "bar", "piscine", "gym"]
            }
        }
