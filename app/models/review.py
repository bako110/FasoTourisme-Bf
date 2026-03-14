from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class Review(BaseModel):
    """Modèle pour les avis et évaluations"""
    
    id: Optional[str] = Field(None, alias="_id")
    
    # Identifiants
    type_ressource: str = Field(..., description="destination, hotel, activity, ou guide")
    ressource_id: str = Field(..., description="ID de la ressource")
    
    # Client
    client_nom: str = Field(..., description="Nom du client qui évalue")
    client_email: Optional[str] = None
    client_photo: Optional[str] = None
    pays_origine: Optional[str] = Field(None, description="Pays d'origine du visiteur")
    
    # Évaluation
    note: int = Field(..., ge=1, le=5, description="Note de 1 à 5")
    titre_avis: str = Field(..., description="Titre court de l'avis")
    commentaire: str = Field(..., description="Commentaire détaillé")
    
    # Aspects évalués (optionnels selon le type)
    note_accueil: Optional[int] = Field(None, ge=1, le=5)
    note_qualite: Optional[int] = Field(None, ge=1, le=5)
    note_service: Optional[int] = Field(None, ge=1, le=5)
    note_prix: Optional[int] = Field(None, ge=1, le=5)
    note_localisation: Optional[int] = Field(None, ge=1, le=5)
    
    # Images/Médias
    photos: List[str] = Field(default=[], description="URLs des photos de l'expérience")
    video_url: Optional[str] = None
    
    # Vérification
    verification_achat: bool = Field(True, description="Achat vérifiée")
    date_experience: Optional[datetime] = Field(None, description="Date de l'expérience")
    
    # Interactions
    utile_count: int = Field(default=0, description="Nombre de 'utile'")
    inutile_count: int = Field(default=0, description="Nombre de 'non-utile'")
    
    # Modération
    approuve: bool = Field(True, description="Avis approuvé?")
    signale_comme_inapproprie: bool = Field(False)
    reponse_proprietaire: Optional[str] = None
    date_reponse: Optional[datetime] = None
    
    # Métadonnées
    date_creation: datetime = Field(default_factory=datetime.utcnow)
    date_modification: datetime = Field(default_factory=datetime.utcnow)
    langue: str = Field(default="fr", description="Langue de l'avis")
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "type_ressource": "destination",
                "ressource_id": "dest_123",
                "client_nom": "Marie Kone",
                "pays_origine": "Côte d'Ivoire",
                "note": 5,
                "titre_avis": "Une expérience magique!",
                "commentaire": "Les cascades sont spectaculaires et l'accueil des habitants est chaleureux. Une destination à ne pas manquer!",
                "note_accueil": 5,
                "note_qualite": 5,
                "note_service": 4,
                "note_prix": 4,
                "date_experience": "2024-03-10T14:30:00",
                "verification_achat": True
            }
        }
