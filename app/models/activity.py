from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, time


class Activity(BaseModel):
    """Modèle pour les activités touristiques"""
    
    id: Optional[str] = Field(None, alias="_id")
    nom: str = Field(..., description="Nom de l'activité")
    description: str = Field(..., description="Description détaillée")
    
    # Classification
    type_activite: str = Field(
        ...,
        description="Type: randonnée, visite_guidée, excursion, atelier_artisanal, safari, etc."
    )
    categorie: List[str] = Field(
        default=[],
        description="Catégories: nature, culture, sport, gastronomie, etc."
    )
    
    # Destination associée
    destination_id: Optional[str] = Field(None, description="ID de la destination associée")
    
    # Localisation
    ville: str = Field(..., description="Ville où se déroule l'activité")
    region: str = Field(..., description="Région")
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    
    # Durée et horaires
    duree_heures: float = Field(..., ge=0.5, description="Durée en heures")
    heure_debut: Optional[str] = Field(None, description="Heure de début (HH:MM)")
    heure_fin: Optional[str] = Field(None, description="Heure de fin (HH:MM)")
    jours_activite: List[str] = Field(
        default=["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"],
        description="Jours de l'activité"
    )
    
    # Tarifs
    tarif_personne_fcfa: float = Field(..., description="Tarif par personne en FCFA")
    tarif_groupe_fcfa: Optional[float] = Field(None, description="Tarif groupe (à partir de 10 personnes)")
    reduction_enfants_pourcent: Optional[float] = Field(None, ge=0, le=100)
    
    # Participants
    nb_minimum_participants: int = Field(default=1)
    nb_maximum_participants: Optional[int] = None
    
    # Niveau de difficulté
    niveau_difficulte: str = Field(
        default="moyen",
        description="facile, moyen, difficile"
    )
    
    # Équipement et préparation
    equipement_requis: List[str] = Field(default=[], description="Équipement à apporter")
    vetements_recommandes: List[str] = Field(default=[])
    restrictions_sante: List[str] = Field(default=[], description="Restrictions de santé")
    
    # Guide et services
    guide_fourni: bool = Field(True)
    langue_guide: List[str] = Field(default=["français", "mooré", "dioula"])
    transport_inclus: bool = Field(False)
    repas_inclus: bool = Field(False)
    
    # Images et médias
    image: Optional[str] = None
    images: List[str] = Field(default=[])
    video_url: Optional[str] = None
    
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
                "nom": "Randonnée au Parc du W",
                "description": "Excursion de 2 jours dans le Parc du W",
                "type_activite": "randonnée",
                "categorie": ["nature", "faune"],
                "ville": "Niamey",
                "region": "Tillabéry",
                "duree_heures": 8,
                "tarif_personne_fcfa": 25000,
                "niveau_difficulte": "moyen",
                "guide_fourni": True,
                "langue_guide": ["français", "dioula"]
            }
        }
