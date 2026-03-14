from pydantic import BaseModel
from typing import Optional, List


class RoadCreate(BaseModel):
    """Schéma pour créer une condition de route"""
    nom_route: str
    point_depart_ville: str
    point_arrivee_ville: str
    etat_route: str = "bon"
    type_route: str = "asphaltée"
    distance_km: Optional[float] = None


class RoadUpdate(BaseModel):
    """Schéma pour mettre à jour une condition de route"""
    etat_route: Optional[str] = None
    type_route: Optional[str] = None
    distance_km: Optional[float] = None


class RoadResponse(BaseModel):
    """Schéma de réponse pour une condition de route"""
    id: Optional[str] = None
    nom_route: str
    point_depart_ville: str
    point_arrivee_ville: str
    etat_route: str
    type_route: str
    distance_km: Optional[float]
    temps_trajet_normal_heures: Optional[float]
    zone_a_risque: bool
    note_moyenne: float
    
    class Config:
        populate_by_name = True
