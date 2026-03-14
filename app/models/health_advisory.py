from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class HealthAdvisory(BaseModel):
    """Modèle pour les conseils et mises en garde sanitaires"""
    
    id: Optional[str] = Field(None, alias="_id")
    
    # Type d'alerte
    type_alerte: str = Field(
        ...,
        description="épidémie, maladie_endémique, vaccin, eau_potable, alimentation, hygiène, etc."
    )
    nom_maladie: Optional[str] = Field(..., description="Nom de la maladie/problème sanitaire")
    
    # Gravité
    niveau_gravite: str = Field(
        default="modéré",
        description="bénin, modéré, grave, très_grave"
    )
    
    # Zone affectée
    villes_affectees: List[str] = Field(..., description="Villes/régions affectées")
    regions: List[str] = Field(...)
    zones_sensibles: Optional[List[str]] = Field(None, description="Zones particulièrement touchées")
    
    # Information épidémiologique
    nombre_cas: Optional[int] = Field(None, description="Nombre de cas confirmés")
    nombre_morts: Optional[int] = None
    taux_mortalite_pourcent: Optional[float] = None
    nouvelles_infections_par_semaine: Optional[int] = None
    tendance: Optional[str] = Field(None, description="augmentation, stable, diminution")
    
    # Transmission
    mode_transmission: Optional[List[str]] = Field(
        None,
        description="Contact, alimentaire, hydrique, vecteur (moustique), etc."
    )
    risque_pour_touristes: str = Field(
        default="modéré",
        description="très_faible, faible, modéré, élevé, très_élevé"
    )
    
    # Symptômes
    symptomes: Optional[List[str]] = None
    delai_incubation_jours: Optional[int] = None
    duree_maladie_jours: Optional[int] = None
    
    # Prévention
    mesures_prevention: List[str] = Field(
        ...,
        description="Actions à prendre pour prévenir la maladie"
    )
    vaccin_disponible: Optional[bool] = None
    vaccin_obligatoire: Optional[bool] = None
    vaccin_recommande: Optional[bool] = None
    
    # Traitement
    traitement_disponible: Optional[bool] = None
    medicaments_efficaces: Optional[List[str]] = None
    ou_se_faire_traiter: Optional[List[str]] = Field(None, description="IDs des hôpitaux/cliniques")
    
    # Hygiène alimentaire
    aliments_a_eviter: Optional[List[str]] = None
    eau_potable_safe: Optional[bool] = None
    conseil_eau: Optional[str] = Field(None, description="Boire eau minérale en bouteille, etc.")
    
    # Comportements à risque
    activites_a_risque: Optional[List[str]] = None
    comportements_a_eviter: Optional[List[str]] = None
    
    # Progression temporelle
    date_debut_epidemie: Optional[datetime] = None
    date_fin_prevue: Optional[datetime] = None
    situation_actuelle: Optional[str] = None
    
    # Recommandations officielle
    position_gouvernement: Optional[str] = None
    voyage_deconseille: Optional[bool] = None
    zones_voyage_deconseille: Optional[List[str]] = None
    
    # Contact médical
    centres_sante_referents: Optional[List[str]] = Field(None, description="IDs des cliniques")
    numero_urgence_sante: Optional[str] = None
    ligne_info_epidemie: Optional[str] = None
    
    # Source et crédibilité
    source: str = Field(..., description="OMS, gouvernement, médecin, ONG, etc.")
    date_information: datetime = Field(...)
    information_mise_a_jour: datetime = Field(default_factory=datetime.utcnow)
    credibilite: str = Field(default="moyenne", description="haute, moyenne, basse")
    
    # Ressources
    references_officielles: Optional[List[str]] = Field(None, description="Liens vers sources officielles")
    articles_medecin: Optional[List[str]] = None
    
    # Statut
    actif: bool = Field(True)
    encore_valide: bool = Field(True)
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "type_alerte": "vaccin",
                "nom_maladie": "Fièvre Jaune",
                "niveau_gravite": "grave",
                "villes_affectees": ["Ouagadougou", "Bobo-Dioulasso"],
                "regions": ["Kadiogo", "Haut-Bassins"],
                "mode_transmission": "moustique",
                "vaccin_obligatoire": False,
                "vaccin_recommande": True,
                "mesures_prevention": [
                    "Vaccination avant voyage",
                    "Répellent anti-moustique",
                    "Vêtements longs le soir"
                ],
                "source": "OMS",
                "credibilite": "haute"
            }
        }
