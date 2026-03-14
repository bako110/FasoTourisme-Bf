from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class BookingCreate(BaseModel):
    """Schéma pour créer une réservation"""
    type_reservation: str
    ressource_id: str
    client_nom: str
    client_email: str
    client_telephone: str
    date_arrivee: datetime
    date_depart: Optional[datetime] = None
    nombre_personnes: int
    nombre_chambres: Optional[int] = None
    notes_speciales: Optional[str] = None
    preferences_repas: Optional[List[str]] = None
    guide_requis: Optional[bool] = None
    guide_id: Optional[str] = None
    tarif_unitaire_fcfa: float
    nombre_nuits_ou_jours: float = 1
    montant_total_fcfa: float
    reduction_pourcent: float = 0
    montant_final_fcfa: float
    methode_paiement: Optional[str] = None


class BookingUpdate(BaseModel):
    """Schéma pour mettre à jour une réservation"""
    statut_reservation: Optional[str] = None
    statut_paiement: Optional[str] = None
    methode_paiement: Optional[str] = None
    reference_paiement: Optional[str] = None
    date_paiement: Optional[datetime] = None
    guide_id: Optional[str] = None
    notes_speciales: Optional[str] = None
    date_annulation: Optional[datetime] = None
    raison_annulation: Optional[str] = None


class BookingResponse(BaseModel):
    """Schéma de réponse pour une réservation"""
    id: Optional[str] = None
    type_reservation: str
    ressource_id: str
    client_nom: str
    client_email: str
    client_telephone: str
    date_arrivee: datetime
    date_depart: Optional[datetime]
    nombre_personnes: int
    montant_final_fcfa: float
    statut_reservation: str
    statut_paiement: str
    date_creation: datetime
    
    class Config:
        populate_by_name = True
