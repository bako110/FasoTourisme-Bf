from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class RoadCondition(BaseModel):
    """Modèle pour l'état des routes et conditions de transport"""
    
    id: Optional[str] = Field(None, alias="_id")
    
    # Identification de la route
    nom_route: str = Field(..., description="Nom ou numéro de la route")
    route_principale: bool = Field(True, description="Route principale?")
    
    # Points de départ et arrivée
    point_depart_ville: str = Field(...)
    point_arrivee_ville: str = Field(...)
    distance_km: Optional[float] = None
    temps_trajet_normal_heures: Optional[float] = None
    
    # État actuel
    etat_route: str = Field(
        default="bon",
        description="excellent, bon, acceptable, mauvais, très_mauvais"
    )
    
    # Détails routes
    type_route: str = Field(
        default="asphaltée",
        description="asphaltée, piste, partiellement_asphaltée, gravier"
    )
    largeur_route: Optional[str] = Field(None, description="large, normale, étroite")
    nombre_voies: Optional[int] = None
    
    # Problèmes spécifiques
    problemes: List[str] = Field(
        default=[],
        description="Nids_de_poule, crevasses, inondations, glissements, débris, travaux, etc."
    )
    
    # Conditions climat
    affectée_par_pluies: bool = Field(False)
    periode_fermee_pluies: Optional[List[str]] = Field(None, description="Mois de fermeture possibles")
    saison_pluies_risque: Optional[str] = Field(None, description="Min-Max (Ex: mai-septembre)")
    
    # Sécurité routière
    eclairage_route: str = Field(
        default="faible",
        description="excellent, bon, faible, absent"
    )
    signalisation: str = Field(
        default="insuffisante",
        description="complète, partielle, insuffisante"
    )
    accidents_frequents: bool = Field(False)
    nombre_accidents_par_an: Optional[int] = None
    
    # Péages et frais
    peage: bool = Field(False)
    cout_peage_fcfa: Optional[float] = None
    
    # Contrôles policiers
    controles_frequents: bool = Field(False)
    type_controles: Optional[List[str]] = None
    problemes_controles: Optional[str] = Field(None, description="Pots-de-vin, demandes anormales, etc.")
    
    # Banditisme/Sécurité
    zone_a_risque: bool = Field(False)
    type_risque: Optional[List[str]] = Field(
        None,
        description="vol, banditisme, piratage, kidnapping"
    )
    horaires_dangereux: Optional[str] = Field(None, description="Ex: après 18:00")
    conseils_securite: Optional[List[str]] = None
    
    # Stations essence/Services
    stations_essence: Optional[int] = Field(None, description="Nombres de stations sur le trajet")
    restaurants_motels: Optional[int] = Field(None, description="Points de repos disponibles")
    absence_services: bool = Field(False, description="Long trajet sans services?")
    distance_station_essence_km: Optional[float] = None
    
    # Transports en commun
    autobus_disponibles: bool = Field(False)
    frequence_autobus: Optional[str] = None
    cout_autobus_fcfa: Optional[float] = None
    
    # Taxis/Cars
    taxis_collectifs: bool = Field(True)
    fiabilite_taxis: str = Field(default="bonne", description="fiable, acceptable, mauvaise")
    prix_taxi_fcfa: Optional[float] = None
    
    # Location véhicules
    location_possible: bool = Field(True)
    type_vehicule_requis: Optional[str] = Field(None, description="4x4, voiture normale, etc.")
    prix_location_jour_fcfa: Optional[float] = None
    
    # Avis voyageurs
    note_moyenne: float = Field(default=0, ge=0, le=5)
    nombre_avis: int = Field(default=0)
    avis_positifs_pourcent: Optional[float] = None
    
    # Recommandations
    recommandation_generale: str = Field(
        default="acceptable",
        description="facilement_recommandée, avec_precautions, difficile_recommander, non_recommandée"
    )
    meilleures_heures_trajet: Optional[str] = Field(None, description="Heures recommandées")
    conseils_traversee: Optional[List[str]] = None
    
    # Statut
    actif: bool = Field(True)
    derniere_mise_a_jour: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "nom_route": "RN1 Ouagadougou-Bobo",
                "route_principale": True,
                "point_depart_ville": "Ouagadougou",
                "point_arrivee_ville": "Bobo-Dioulasso",
                "distance_km": 370,
                "temps_trajet_normal_heures": 5.5,
                "etat_route": "bon",
                "type_route": "asphaltée",
                "problemes": [],
                "eclairage_route": "faible",
                "signalisation": "partielle",
                "accidents_frequents": False,
                "zone_a_risque": False,
                "autobus_disponibles": True,
                "taxis_collectifs": True,
                "note_moyenne": 4.2
            }
        }
