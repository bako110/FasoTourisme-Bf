from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from bson import ObjectId


class Destination(BaseModel):
    """Modèle pour les destinations touristiques du Burkina Faso"""
    
    id: Optional[str] = Field(None, alias="_id")
    nom: str = Field(..., description="Nom de la destination")
    description: str = Field(..., description="Description détaillée")
    region: str = Field(..., description="Région du Burkina Faso")
    province: str = Field(..., description="Province")
    localite: str = Field(..., description="Localité/Commune")
    
    # Informations touristiques
    type_destination: str = Field(
        ..., 
        description="Type: parc_national, musée, cascade, site_historique, etc."
    )
    categorie: List[str] = Field(default=[], description="Catégories: nature, culture, histoire, etc.")
    
    # Localisation
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    altitude: Optional[float] = None
    
    # Accès et facilités
    temps_acces_heures: Optional[float] = Field(None, description="Temps d'accès depuis la capitale en heures")
    meilleure_saison: List[str] = Field(default=[], description="Meilleures saisons pour visiter")
    acces_securise: bool = Field(True, description="L'accès est-il sécurisé?")
    
    # Tarifs
    tarif_entree_fcfa: Optional[float] = Field(None, description="Tarif d'entrée en FCFA")
    tarif_guide_fcfa: Optional[float] = Field(None, description="Tarif du guide en FCFA")
    
    # Images et médias
    image: Optional[str] = Field(None, description="URL de l'image principale")
    images: List[str] = Field(default=[], description="URLs des images supplémentaires")
    video_url: Optional[str] = Field(None, description="URL d'une vidéo")
    
    # Évaluations
    note_moyenne: float = Field(default=0, ge=0, le=5)
    nombre_evaluations: int = Field(default=0)
    
    # Métadonnées
    publie: bool = Field(True, description="La destination est-elle publiée?")
    date_creation: datetime = Field(default_factory=datetime.utcnow)
    date_modification: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "nom": "Cascade de Banfora",
                "description": "Spectaculaire cascade dans la région boucle du Mouhoun",
                "region": "Hauts-Bassins",
                "province": "Cascades",
                "localite": "Banfora",
                "type_destination": "cascade",
                "categorie": ["nature", "randonnée"],
                "latitude": 10.6347,
                "longitude": -4.7596,
                "meilleure_saison": ["septembre", "octobre", "novembre"],
                "acces_securise": True,
                "tarif_entree_fcfa": 2000.0
            }
        }
