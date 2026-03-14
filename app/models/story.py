from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class VisitorStory(BaseModel):
    """Modèle pour les témoignages et histoires de visiteurs"""
    
    id: Optional[str] = Field(None, alias="_id")
    
    # Visiteur
    visiteur_nom: str = Field(..., description="Nom du visiteur")
    visiteur_prenom: Optional[str] = None
    email_visiteur: Optional[str] = None
    photo_visiteur: Optional[str] = None
    pays_origine: str = Field(..., description="Pays d'origine")
    profession: Optional[str] = None
    
    # Expérience
    titre_histoire: str = Field(..., description="Titre captivant de l'histoire")
    histoire: str = Field(..., description="Grande histoire détaillée (500+ caractères)")
    
    # Contexte
    destinations_visitees: List[str] = Field(
        ...,
        description="IDs des destinations/hôtels/activités mentionnées"
    )
    date_visite: datetime = Field(..., description="Date de la visite")
    duree_sejour_jours: int = Field(..., ge=1, description="Durée du séjour en jours")
    type_voyageur: str = Field(
        default="solo",
        description="solo, couple, famille, groupe, business"
    )
    groupe_taille: Optional[int] = Field(None, description="Taille du groupe")
    
    # Points marquants
    moments_marquants: str = Field(
        ...,
        description="Les moments les plus mémorables de la visite"
    )
    rencontres_interessantes: Optional[str] = Field(
        None,
        description="Rencontres intéressantes avec les habitants locaux"
    )
    apprentissages: Optional[str] = Field(
        None,
        description="Ce qu'il a appris sur la culture burkinabé"
    )
    
    # Impacts et changements
    impact_personnel: Optional[str] = Field(
        None,
        description="Comment cette visite l'a changé personnellement"
    )
    recommande_a_qui: Optional[str] = Field(
        None,
        description="À qui recommande-t-il le Burkina?"
    )
    veut_revenir: bool = Field(True, description="Veut-il revenir?")
    prochaine_visite_plan: Optional[str] = None
    
    # Connexion émotionnelle
    lien_emactionnel: Optional[str] = Field(
        None,
        description="Lien émotionnel créé avec le destination/communauté"
    )
    a_change_perception: bool = Field(
        False,
        description="A changé sa perception du Burkina?"
    )
    
    # Conseils aux voyageurs
    conseil_voyageurs: Optional[str] = Field(
        None,
        description="Conseils aux futurs voyageurs"
    )
    meilleure_periode: Optional[str] = Field(
        None,
        description="Meilleure période pour visiter selon lui"
    )
    essentiels_a_apporter: Optional[List[str]] = None
    
    # Médias
    photos: List[str] = Field(default=[], description="Photos de l'histoire")
    video_teemoignage: Optional[str] = None
    
    # Statut
    approuve: bool = Field(True, description="Approuvé pour publication?")
    publie: bool = Field(True)
    mise_en_avant: bool = Field(
        False,
        description="Mettre en avant sur la page d'accueil?"
    )
    
    # Engagement
    consentement_partage: bool = Field(
        True,
        description="Consentement pour partager l'histoire?"
    )
    consentement_contact: bool = Field(
        False,
        description="D'accord pour être contacté?"
    )
    
    # Métadonnées
    date_creation: datetime = Field(default_factory=datetime.utcnow)
    date_modification: datetime = Field(default_factory=datetime.utcnow)
    langue: str = Field(default="fr")
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "visiteur_nom": "Martin",
                "visiteur_prenom": "Jean-Luc",
                "pays_origine": "France",
                "titre_histoire": "Mon voyage transformateur au cœur du Burkina",
                "histoire": "C'était ma première fois en Afrique de l'Ouest. J'ai visité plusieurs destinations magnifiques...",
                "destinations_visitees": ["dest_123", "dest_456"],
                "date_visite": "2024-02-15",
                "duree_sejour_jours": 10,
                "type_voyageur": "solo",
                "moments_marquants": "La rencontre avec les artisans locaux et les couchers de soleil",
                "rencontres_interessantes": "J'ai rencontré Ibrahim qui m'a appris le tissage traditionnel",
                "apprentissages": "La richesse culturelle et la simplicité de la vie locale",
                "veut_revenir": True,
                "conseil_voyageurs": "Prenez le temps de parler avec les habitants, ils ont beaucoup à partager"
            }
        }
