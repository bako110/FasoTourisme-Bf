from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class HealthFacility(BaseModel):
    """Modèle pour les installations de santé (pharmacies, hôpitaux, cliniques)"""
    
    id: Optional[str] = Field(None, alias="_id")
    
    # Informations basiques
    nom: str = Field(..., description="Nom de l'établissement")
    type_etablissement: str = Field(
        ...,
        description="pharmacie, hopital, clinique, centre_sante, maternite, dentiste, optometrie, etc."
    )
    classification: Optional[str] = Field(
        None,
        description="Gouvernemental, privé, ONG"
    )
    
    # Localisation
    ville: str = Field(...)
    region: str = Field(...)
    province: str = Field(...)
    localite: str = Field(...)
    adresse: str = Field(...)
    latitude: float = Field(...)
    longitude: float = Field(...)
    
    # Contact
    telephone_principal: str = Field(...)
    telephone_urgence: Optional[str] = None
    email: Optional[str] = None
    
    # Horaires
    horaires_ouverture: str = Field(..., description="Exemple: '08:00-18:00'")
    ouvert_24h: bool = Field(False)
    ouvert_dimanche: bool = Field(False)
    fermeture_week_end: bool = Field(False)
    
    # Services proposés
    services: List[str] = Field(
        ...,
        description="Consultation générale, urgence, chirurgie, maternité, pédiatrie, etc."
    )
    services_pharmacie: Optional[List[str]] = Field(
        None,
        description="Pour pharmacies: médicaments génériques, marques, produits biologiques, etc."
    )
    
    # Ressources et capacités
    nombre_lits: Optional[int] = None
    nombre_medecins: Optional[int] = None
    nombre_infirmiers: Optional[int] = None
    nombre_pharmaciens: Optional[int] = None
    
    # Équipements
    equipements: List[str] = Field(
        default=[],
        description="Radiologie, laboratoire, scanner, IRM, urgence 24h, ambulance, etc."
    )
    
    # Capacités d'urgence
    urgence_disponible: bool = Field(False)
    ambulance_disponible: bool = Field(False)
    capacite_urgence_par_jour: Optional[int] = None
    
    # Tarification
    consultation_urgence_fcfa: Optional[float] = None
    consultation_normal_fcfa: Optional[float] = None
    frais_urgence_fcfa: Optional[float] = None
    accepte_assurance: bool = Field(False)
    types_assurance: Optional[List[str]] = None
    
    # Ressources en médicaments essentiels
    medicaments_urgence: List[str] = Field(
        default=[],
        description="Liste des médicaments d'urgence disponibles"
    )
    stocks_adequats: bool = Field(True, description="Stocks adéquats de médicaments?")
    refrigeration_disponible: bool = Field(True)
    
    # Hygiène et normes
    certification_sante: bool = Field(False)
    normes_hygiene_respectees: bool = Field(True)
    dernier_controle: Optional[datetime] = None
    resultat_controle: Optional[str] = None
    
    # Accessibilité
    accessible_pmr: bool = Field(False)
    parking: bool = Field(False)
    transport_public: bool = Field(False)
    
    # Info pour touristes
    parle_langues_etrangeres: Optional[List[str]] = None
    guide_possible: bool = Field(False)
    guide_disponible: Optional[str] = None
    
    # Évacuation
    evacuation_possible: bool = Field(False)
    evacuation_destination: Optional[str] = None
    temps_evacuation_heures: Optional[float] = None
    
    # Communication
    connection_internet: bool = Field(False)
    telephone_international: bool = Field(False)
    
    # Statut
    actif: bool = Field(True)
    verified: bool = Field(False)
    date_verification: Optional[datetime] = None
    
    # Métadonnées
    date_creation: datetime = Field(default_factory=datetime.utcnow)
    date_modification: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "nom": "Pharmacie Centrale Ouagadougou",
                "type_etablissement": "pharmacie",
                "classification": "privé",
                "ville": "Ouagadougou",
                "region": "Kadiogo",
                "adresse": "Avenue Kléber",
                "latitude": 12.3656,
                "longitude": -1.5197,
                "telephone_principal": "+226 70 00 00 00",
                "horaires_ouverture": "07:00-22:00",
                "ouvert_24h": False,
                "services": ["vente_medicaments", "conseil_pharmacien"],
                "accepte_assurance": True,
                "certificat_sante": True
            }
        }
