from pydantic import BaseModel
from typing import Optional, List


class TouristInfoCreate(BaseModel):
    """Schéma pour créer une info touristique"""
    categorie: str
    titre: str
    description: str
    conseils_pratiques: List[str]
    zone_applicabilite: Optional[str] = None
    regions_concernees: Optional[List[str]] = None


class TouristInfoUpdate(BaseModel):
    """Schéma pour mettre à jour une info touristique"""
    titre: Optional[str] = None
    description: Optional[str] = None
    conseils_pratiques: Optional[List[str]] = None
    zone_applicabilite: Optional[str] = None
    regions_concernees: Optional[List[str]] = None


class TouristInfoResponse(BaseModel):
    """Schéma de réponse pour une info touristique"""
    id: Optional[str] = None
    categorie: str
    titre: str
    titre_long: Optional[str]
    description: str
    conseils_pratiques: List[str]
    zone_applicabilite: Optional[str]
    important: bool
    
    class Config:
        populate_by_name = True
