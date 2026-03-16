from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class LocalEvent(BaseModel):
    """Modèle pour les événements locaux, festivals et fêtes"""
    
    id: Optional[str] = Field(None, alias="_id")
    
    # Informations basiques
    nom: str = Field(..., description="Nom de l'événement")
    description: str = Field(..., description="Description détaillée")
    type_evenement: str = Field(
        ...,
        description="festival, cérémonie, marché, exposition, spectacle, fête, etc."
    )
    
    # Localisation
    ville: str = Field(..., description="Ville de l'événement")
    region: str = Field(..., description="Région")
    province: str = Field(..., description="Province")
    localite: str = Field(..., description="Localité précise")
    lieu: str = Field(..., description="Lieu/Nom du site")
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    
    # Dates
    date_debut: datetime = Field(..., description="Date/heure de début")
    date_fin: datetime = Field(..., description="Date/heure de fin")
    recurrence: Optional[str] = Field(None, description="annuelle, mensuelle, hebdomadaire, etc.")
    
    # Accès
    gratuit: bool = Field(True, description="Événement gratuit?")
    tarif_entree_fcfa: Optional[float] = Field(None, description="Tarif d'entrée en FCFA")
    capacite_max: Optional[int] = Field(None, description="Capacité maximale de participants")
    
    # Contenu culturel
    description_culturelle: str = Field(
        ...,
        description="Importance culturelle, traditions, histoire de l'événement"
    )
    tradition_associee: Optional[str] = Field(None, description="Tradition associée")
    origine_historique: Optional[str] = None
    signification_locale: Optional[str] = Field(
        None,
        description="Comment cet événement est important pour la communauté"
    )
    
    # Communauté
    communaute_hote: str = Field(..., description="Communauté qui organise l'événement")
    contact_communaute: Optional[str] = Field(None, description="Contact de la communauté")
    nombre_participants_attendus: Optional[int] = None
    
    # Activités et attractions
    activites: List[str] = Field(
        default=[],
        description="Danse, musique, gastronomie, arts, artisanat, etc."
    )
    artisans_locaux: List[str] = Field(
        default=[],
        description="IDs des artisans locaux qui participent"
    )
    restaurants_locaux: List[str] = Field(
        default=[],
        description="IDs des restaurants qui proposent des spécialités"
    )
    
    # Médias
    image: Optional[str] = None
    images: List[str] = Field(default=[])
    video_url: Optional[str] = None
    
    # Recommandations
    meilleure_periode_visite: Optional[str] = Field(None, description="Meilleure heure/jour pour visiter")
    conseil_visite: Optional[str] = Field(None, description="Conseils pratiques pour les visiteurs")
    tenue_recommandee: Optional[str] = Field(None, description="Tenue recommandée")
    
    # Accessibilité
    accessible_pmr: bool = Field(False, description="Accessible aux PMR?")
    parking_disponible: bool = Field(False)
    transports_publics: bool = Field(False, description="Transports publics à proximité?")
    
    # Statut
    publie: bool = Field(True)
    date_creation: datetime = Field(default_factory=datetime.utcnow)
    date_modification: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "nom": "Fête de l'Indépendance du Burkina Faso",
                "description": "Grande célébration nationale avec parades, spectacles et festivités",
                "type_evenement": "fête",
                "ville": "Ouagadougou",
                "region": "Kadiogo",
                "province": "Kadiogo",
                "localite": "Centre-ville",
                "lieu": "Place de la Nation",
                "date_debut": "2024-08-04T08:00:00",
                "date_fin": "2024-08-04T22:00:00",
                "recurrence": "annuelle",
                "gratuit": True,
                "description_culturelle": "Célébration de l'indépendance du Burkina Faso depuis 1960",
                "communaute_hote": "Gouvernement du Burkina Faso",
                "activites": ["danse", "musique", "spectacles", "gastronomie"],
                "conseil_visite": "Arriver tôt pour avoir une bonne place"
            }
        }
