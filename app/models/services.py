from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class EssentialService(BaseModel):
    """Modèle pour les services essentiels (électricité, eau, transport, etc.)"""
    
    id: Optional[str] = Field(None, alias="_id")
    
    # Type de service
    type_service: str = Field(
        ...,
        description="eau, electricite, gaz, internet, telephone, transport_public, carburant, banque, atm, poste, etc."
    )
    provider_name: str = Field(..., description="Nom du prestataire")
    
    # Localisation
    ville: str = Field(...)
    region: str = Field(...)
    province: str = Field(...)
    localite: str = Field(...)
    
    # Pour services physiques (stations, bureaux, ATM, etc.)
    adresse_physique: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    
    # Disponibilité et fiabilité
    est_operationnel: bool = Field(True)
    taux_disponibilite_pourcent: Optional[float] = Field(
        None,
        ge=0,
        le=100,
        description="Pourcentage de disponibilité du service"
    )
    coupures_frequentes: bool = Field(False, description="Y a-t-il des coupures fréquentes?")
    nombre_coupures_par_mois: Optional[int] = None
    duree_moyenne_coupure_heures: Optional[float] = None
    
    # Horaires
    horaires_ouverture: Optional[str] = None
    ouvert_24h: bool = Field(False)
    ouvert_weekend: bool = Field(False)
    fermé_jours: Optional[List[str]] = None
    
    # Contact
    telephone_contact: Optional[str] = None
    email_contact: Optional[str] = None
    numero_urgence: Optional[str] = None
    
    # Qualité du service
    qualite_service: str = Field(
        default="moyenne",
        description="excellente, bonne, moyenne, mauvaise"
    )
    vitesse_service: Optional[str] = Field(
        None,
        description="rapide, normal, lent"
    )
    
    # Détails spécifiques par type
    
    # Eau
    eau_potable: Optional[bool] = None
    qualite_eau: Optional[str] = None
    pression_eau: Optional[str] = Field(None, description="forte, normale, faible, intermittente")
    
    # Electricité
    tension_stable: Optional[bool] = None
    puissance_disponible_kwh: Optional[float] = None
    
    # Internet/Téléphone
    vitesse_internet_mbps: Optional[float] = None
    type_connexion: Optional[str] = Field(None, description="fibre, 4G, 3G, ADSL, etc.")
    stabilite_connexion: Optional[str] = Field(None, description="stable, instable, intermittente")
    couverture_zone: Optional[bool] = None
    
    # Transport
    type_transport: Optional[str] = Field(
        None,
        description="bus, taxi, mototaxi, locations_voitures, etc."
    )
    horaire_debut_service: Optional[str] = None
    horaire_fin_service: Optional[str] = None
    frequence_passages: Optional[str] = Field(None, description="Fréquence des passages (toutes les X minutes)")
    
    # Banque/ATM
    devise_principales: Optional[List[str]] = None
    retrait_max_fcfa: Optional[float] = None
    frais_retrait_pourcent: Optional[float] = None
    change_possible: Optional[bool] = None
    taux_change_favorable: Optional[bool] = None
    
    # Carburant
    type_carburant: Optional[List[str]] = None
    prix_litre_fcfa: Optional[float] = None
    qualite_carburant: Optional[str] = None
    
    # Fiabilité
    frequence_problemes: str = Field(
        default="rare",
        description="rare, occasionnel, frequent, very_frequent"
    )
    temps_resolution_problemes_heures: Optional[float] = None
    
    # Accessibilité
    accessible_touristes: bool = Field(True)
    parle_langues_etrangeres: bool = Field(False)
    identification_facile: bool = Field(True, description="Service facile à localiser?")
    
    # Sécurité
    securite: str = Field(
        default="bonne",
        description="excellente, bonne, acceptable, mauvaise"
    )
    zone_securisee: bool = Field(False)
    eclairage_suffisant: Optional[bool] = None
    
    # Recommandations
    conseil_utilisation: Optional[str] = Field(
        None,
        description="Conseils pratiques pour utiliser ce service"
    )
    horaire_optimal: Optional[str] = Field(
        None,
        description="Meilleur moment pour utiliser le service"
    )
    alternative_proximite: Optional[str] = Field(
        None,
        description="Service alternatif si celui-ci n'est pas dispo"
    )
    
    # Tarification
    tarifs: Optional[str] = Field(None, description="Description des tarifs")
    tarif_approximatif_fcfa: Optional[float] = None
    methodes_paiement: Optional[List[str]] = Field(
        None,
        description="especes, carte, mobile_money, cheque, etc."
    )
    
    # Statut
    actif: bool = Field(True)
    verified: bool = Field(False)
    last_update: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "type_service": "electricite",
                "provider_name": "SONABEL",
                "ville": "Ouagadougou",
                "region": "Kadiogo",
                "est_operationnel": True,
                "taux_disponibilite_pourcent": 85,
                "coupures_frequentes": True,
                "nombre_coupures_par_mois": 3,
                "duree_moyenne_coupure_heures": 2,
                "tension_stable": False,
                "qualite_service": "moyenne",
                "conseil_utilisation": "Prévoir une lampe torche et batterie externe"
            }
        }
