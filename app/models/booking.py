from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class Booking(BaseModel):
    """Modèle pour les réservations de destinations, hôtels, activités"""
    
    id: Optional[str] = Field(None, alias="_id")
    
    # Identifiants
    type_reservation: str = Field(..., description="destination, hotel, ou activity")
    ressource_id: str = Field(..., description="ID de la ressource (destination/hotel/activity)")
    client_nom: str = Field(..., description="Nom du client")
    client_email: str = Field(..., description="Email du client")
    client_telephone: str = Field(..., description="Téléphone du client")
    
    # Réservation
    date_arrivee: datetime = Field(..., description="Date d'arrivée")
    date_depart: Optional[datetime] = Field(None, description="Date de départ (pour hôtels)")
    nombre_personnes: int = Field(..., ge=1, description="Nombre de personnes")
    nombre_chambres: Optional[int] = Field(None, description="Nombre de chambres (hôtels)")
    
    # Détails
    notes_speciales: Optional[str] = Field(None, description="Demandes spéciales du client")
    preferences_repas: Optional[List[str]] = Field(None, description="Préférences alimentaires")
    guide_requis: Optional[bool] = Field(None, description="Guide touristique requis?")
    guide_id: Optional[str] = Field(None, description="ID du guide assigné")
    
    # Tarification
    tarif_unitaire_fcfa: float = Field(..., description="Tarif unitaire en FCFA")
    nombre_nuits_ou_jours: float = Field(default=1, description="Nombre de jours/nuits")
    montant_total_fcfa: float = Field(..., description="Montant total en FCFA")
    reduction_pourcent: float = Field(default=0, ge=0, le=100, description="Réduction appliquée (%)")
    montant_final_fcfa: float = Field(..., description="Montant final à payer")
    
    # Paiement
    statut_paiement: str = Field(
        default="attente",
        description="attente, acompte, paye, rembourse"
    )
    date_paiement: Optional[datetime] = None
    methode_paiement: Optional[str] = Field(
        None,
        description="virement, mobile_money, especes, carte"
    )
    reference_paiement: Optional[str] = Field(None, description="Référence du paiement")
    
    # Statut
    statut_reservation: str = Field(
        default="confirmee",
        description="confirmee, en_attente, annulee, completee"
    )
    date_annulation: Optional[datetime] = None
    raison_annulation: Optional[str] = None
    
    # Métadonnées
    date_creation: datetime = Field(default_factory=datetime.utcnow)
    date_modification: datetime = Field(default_factory=datetime.utcnow)
    source_reservation: str = Field(
        default="web",
        description="web, mobile, telephone, agence"
    )
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "type_reservation": "activity",
                "ressource_id": "activity_123",
                "client_nom": "Alassane Diallo",
                "client_email": "alassane@example.com",
                "client_telephone": "+226 70 11 22 33",
                "date_arrivee": "2024-04-15T08:00:00",
                "nombre_personnes": 4,
                "notes_speciales": "Nous aimerions de l'eau et des fruits frais",
                "tarif_unitaire_fcfa": 25000,
                "nombre_nuits_ou_jours": 1,
                "montant_total_fcfa": 100000,
                "montant_final_fcfa": 85000,
                "reduction_pourcent": 15
            }
        }
