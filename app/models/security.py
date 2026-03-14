from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class SecurityAlert(BaseModel):
    """Modèle pour les alertes de sécurité et zones sensibles"""
    
    id: Optional[str] = Field(None, alias="_id")
    
    # Classification
    type_alerte: str = Field(
        ...,
        description="vol, banditisme, manifestation, accident, maladie, construction, etc."
    )
    niveau_risque: str = Field(
        default="moyen",
        description="faible, moyen, elevé, très_elevé"
    )
    
    # Localisation
    ville: str = Field(...)
    region: str = Field(...)
    province: str = Field(...)
    localite: Optional[str] = None
    quartier: Optional[str] = None
    
    aire_affectee: str = Field(
        ...,
        description="Zone géographique décrite (route X à Y, quartier Z, etc.)"
    )
    coordonnees_centre_latitude: Optional[float] = None
    coordonnees_centre_longitude: Optional[float] = None
    rayon_affection_km: Optional[float] = None
    
    # Détails
    description_alerte: str = Field(..., description="Description détaillée du problème")
    cause: Optional[str] = Field(None, description="Cause supposée")
    
    # Temporalité
    date_debut: datetime = Field(..., description="Quand a commencé le problème?")
    date_fin_prevue: Optional[datetime] = None
    heure_debut_alerte: Optional[str] = Field(None, description="Heure du jour (ex: 22:00-05:00)")
    
    # Recommandations
    recommandation_touristes: str = Field(
        ...,
        description="Que doivent faire les touristes: éviter, être prudent, ne pas dépasser certaines heures, etc."
    )
    zones_a_eviter: Optional[List[str]] = None
    horaires_a_eviter: Optional[str] = None
    route_alternative: Optional[str] = None
    
    # Fréquence
    frequence_incidents: str = Field(
        default="ponctuel",
        description="ponctuel, occasionnel, recurrent, permanent"
    )
    incidents_precedents: Optional[int] = Field(None, description="Nombre d'incidents similaires")
    
    # Impact tourisme
    impact_activites: List[str] = Field(
        default=[],
        description="Quelles activités sont affectées"
    )
    impact_destinations: List[str] = Field(
        default=[],
        description="IDs des destinations affectées"
    )
    
    # Ressources de sécurité
    police_proximite: bool = Field(True, description="Police à proximité?")
    gendarmerie_proximite: bool = Field(False)
    pompiers_proximite: bool = Field(True)
    contact_urgence: Optional[str] = None
    
    # Source
    source_information: str = Field(
        ...,
        description="police, témoignage, autorités, médias, habitants, guide"
    )
    journalist_fiable: bool = Field(True, description="Source fiable?")
    
    # Mesures de prévention
    mesures_preventivement: Optional[List[str]] = Field(
        None,
        description="Mesures prises par autorités"
    )
    conseils_preventifs: Optional[List[str]] = None
    
    # Statut
    actif: bool = Field(True, description="Alerte toujours en vigueur?")
    resolu: bool = Field(False)
    date_resolution: Optional[datetime] = None
    
    # Modération
    verifiee: bool = Field(False)
    date_verification: Optional[datetime] = None
    verifiee_par: Optional[str] = None
    
    # Métadonnées
    date_creation: datetime = Field(default_factory=datetime.utcnow)
    date_modification: datetime = Field(default_factory=datetime.utcnow)
    urgence_alerte: str = Field(default="normal", description="urgent, normal, information")
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "type_alerte": "construction",
                "niveau_risque": "moyen",
                "ville": "Ouagadougou",
                "region": "Kadiogo",
                "quartier": "Wemtenga",
                "aire_affectee": "Route de l'ouest entre intersections X et Y",
                "description_alerte": "Travaux de réfection de route en cours",
                "date_debut": "2024-03-01",
                "date_fin_prevue": "2024-04-30",
                "heure_debut_alerte": "06:00-18:00",
                "recommandation_touristes": "Eviter la route le matin, prendre route alternative par le nord",
                "frequence_incidents": "ponctuel",
                "route_alternative": "Route de Tansin via Boulevard de la révolution"
            }
        }
