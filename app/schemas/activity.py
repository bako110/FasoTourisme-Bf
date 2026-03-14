from pydantic import BaseModel
from typing import Optional, List


class ActivityCreate(BaseModel):
    """Schéma pour créer une activité"""
    nom: str
    description: str
    type_activite: str
    categorie: List[str] = []
    destination_id: Optional[str] = None
    ville: str
    region: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    duree_heures: float
    heure_debut: Optional[str] = None
    heure_fin: Optional[str] = None
    jours_activite: List[str] = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
    tarif_personne_fcfa: float
    tarif_groupe_fcfa: Optional[float] = None
    reduction_enfants_pourcent: Optional[float] = None
    nb_minimum_participants: int = 1
    nb_maximum_participants: Optional[int] = None
    niveau_difficulte: str = "moyen"
    equipement_requis: List[str] = []
    vetements_recommandes: List[str] = []
    restrictions_sante: List[str] = []
    guide_fourni: bool = True
    langue_guide: List[str] = ["français", "mooré", "dioula"]
    transport_inclus: bool = False
    repas_inclus: bool = False
    image_principale: Optional[str] = None
    galerie_images: List[str] = []
    video_url: Optional[str] = None


class ActivityUpdate(BaseModel):
    """Schéma pour mettre à jour une activité"""
    nom: Optional[str] = None
    description: Optional[str] = None
    type_activite: Optional[str] = None
    categorie: Optional[List[str]] = None
    destination_id: Optional[str] = None
    ville: Optional[str] = None
    region: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    duree_heures: Optional[float] = None
    heure_debut: Optional[str] = None
    heure_fin: Optional[str] = None
    jours_activite: Optional[List[str]] = None
    tarif_personne_fcfa: Optional[float] = None
    tarif_groupe_fcfa: Optional[float] = None
    reduction_enfants_pourcent: Optional[float] = None
    nb_minimum_participants: Optional[int] = None
    nb_maximum_participants: Optional[int] = None
    niveau_difficulte: Optional[str] = None
    equipement_requis: Optional[List[str]] = None
    vetements_recommandes: Optional[List[str]] = None
    restrictions_sante: Optional[List[str]] = None
    guide_fourni: Optional[bool] = None
    langue_guide: Optional[List[str]] = None
    transport_inclus: Optional[bool] = None
    repas_inclus: Optional[bool] = None
    image_principale: Optional[str] = None
    galerie_images: Optional[List[str]] = None
    video_url: Optional[str] = None
    note_moyenne: Optional[float] = None
    publie: Optional[bool] = None


class ActivityResponse(BaseModel):
    """Schéma de réponse pour une activité"""
    id: Optional[str] = None
    nom: str
    description: str
    type_activite: str
    categorie: List[str]
    destination_id: Optional[str]
    ville: str
    region: str
    latitude: Optional[float]
    longitude: Optional[float]
    duree_heures: float
    heure_debut: Optional[str]
    heure_fin: Optional[str]
    jours_activite: List[str]
    tarif_personne_fcfa: float
    tarif_groupe_fcfa: Optional[float]
    reduction_enfants_pourcent: Optional[float]
    nb_minimum_participants: int
    nb_maximum_participants: Optional[int]
    niveau_difficulte: str
    equipement_requis: List[str]
    vetements_recommandes: List[str]
    restrictions_sante: List[str]
    guide_fourni: bool
    langue_guide: List[str]
    transport_inclus: bool
    repas_inclus: bool
    image_principale: Optional[str]
    galerie_images: List[str]
    video_url: Optional[str]
    note_moyenne: float
    nombre_evaluations: int
    publie: bool
    
    class Config:
        populate_by_name = True
