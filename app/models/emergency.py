from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class EmergencyService(BaseModel):
    """Modèle pour les services d'urgence (police, pompiers, ambulance, etc.)"""
    
    id: Optional[str] = Field(None, alias="_id")
    
    # Type de service
    type_urgence: str = Field(
        ...,
        description="police, gendarmerie, pompiers, ambulance, secours_montagne, bateau_sauvetage, etc."
    )
    nom_organisme: str = Field(...)
    
    # Localisation du siège
    ville_siege: str = Field(...)
    region_siege: str = Field(...)
    adresse_siege: str = Field(...)
    latitude_siege: Optional[float] = None
    longitude_siege: Optional[float] = None
    
    # Contact urgence
    numero_urgence_principal: str = Field(...)
    numero_urgence_secondaire: Optional[str] = None
    email_contact: Optional[str] = None
    radio_frequence: Optional[str] = None
    
    # Disponibilité
    disponible_24h: bool = Field(True)
    temps_reponse_moyen_minutes: Optional[int] = None
    temps_reponse_max_minutes: Optional[int] = None
    
    # Couverture géographique
    zones_couvertes: List[str] = Field(
        ...,
        description="Listes des zones/régions couvertes"
    )
    points_presence: List[dict] = Field(
        default=[],
        description="Points de présence (postes, stations) avec adresse et coordonnées"
    )
    
    # Ressources
    nombre_vehicules: Optional[int] = None
    type_vehicules: Optional[List[str]] = Field(None, description="ambulances, camions pompiers, etc.")
    nombre_personnel: Optional[int] = None
    qualifications_personnel: Optional[List[str]] = None
    
    # Équipements
    equipements_speciaux: Optional[List[str]] = Field(
        None,
        description="Pour pompiers: échelles, pont aérien; pour ambulances: réanimation, etc."
    )
    capacite_medicale: Optional[str] = Field(None, description="Premiers secours, réanimation, etc.")
    
    # Communication
    parle_langues_etrangeres: Optional[List[str]] = None
    interpreteur_disponible: bool = Field(False)
    
    # Protocoles
    protocole_pour_touristes: Optional[str] = Field(
        None,
        description="Instructions spéciales pour touristes"
    )
    procedure_appel: Optional[str] = Field(
        None,
        description="Comment appeler, informations à donner"
    )
    accepte_appels_etrangers: bool = Field(True)
    
    # Performance et fiabilité
    taux_reussite_interventions: Optional[float] = Field(None, ge=0, le=100)
    nombre_interventions_par_an: Optional[int] = None
    type_incidents_geres: Optional[List[str]] = None
    
    # Facilités
    accueil_touristes: bool = Field(True)
    point_rencontre_possible: bool = Field(False)
    assistance_consulaire: Optional[bool] = None
    
    # Évacuation médicale
    evacuation_medicale_possible: bool = Field(False)
    helicoptere_disponible: Optional[bool] = None
    partenaires_evacuation: Optional[List[str]] = None
    
    # Coût
    tarif_intervention_fcfa: Optional[float] = None
    gratuit: Optional[bool] = None
    frais_ambulance_fcfa: Optional[float] = None
    couvert_assurance: Optional[bool] = None
    
    # Information additionnelle
    historique_fiabilite: Optional[str] = Field(None, description="Réputation et fiabilité")
    informations_importantes: Optional[List[str]] = None
    
    # Problèmes connus
    limitations_connues: Optional[List[str]] = None
    equipements_insuffisants: Optional[bool] = None
    manque_personnel: Optional[bool] = None
    manque_formation: Optional[bool] = None
    
    # Recommandations aux touristes
    recommandations_preventivement: Optional[List[str]] = None
    quoi_faire_en_cas_urgence: Optional[str] = None
    contact_autorites_pays_touristes: Optional[List[str]] = None
    
    # Statut
    operationnel: bool = Field(True)
    verified: bool = Field(False)
    last_verification: Optional[datetime] = None
    
    # Métadonnées
    date_creation: datetime = Field(default_factory=datetime.utcnow)
    date_modification: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "type_urgence": "ambulance",
                "nom_organisme": "Croix-Rouge Burkinabé - Ambulance",
                "ville_siege": "Ouagadougou",
                "region_siege": "Kadiogo",
                "numero_urgence_principal": "+226 50 00 00 00",
                "disponible_24h": True,
                "temps_reponse_moyen_minutes": 15,
                "zones_couvertes": ["Ouagadougou", "banlieue"],
                "nombre_vehicules": 8,
                "type_vehicules": ["ambulances", "ambulances_type_B"],
                "parle_langues_etrangeres": ["français", "anglais"],
                "accepte_appels_etrangers": True,
                "evacuation_medicale_possible": True,
                "helicoptere_disponible": False
            }
        }
