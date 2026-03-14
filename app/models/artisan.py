from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class LocalArtisan(BaseModel):
    """Modèle pour les artisans et entrepreneurs locaux du tourisme"""
    
    id: Optional[str] = Field(None, alias="_id")
    
    # Informations personnelles
    nom: str = Field(..., description="Nom de l'artisan ou de l'entreprise")
    prenom: Optional[str] = Field(None, description="Prénom de l'artisan")
    type_artisan: str = Field(
        ...,
        description="tissage, sculpture, poterie, joaillerie, gastronomie, textile, etc."
    )
    
    # Localisation
    ville: str = Field(..., description="Ville")
    region: str = Field(..., description="Région")
    province: str = Field(..., description="Province")
    localite: str = Field(..., description="Localité")
    adresse: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    
    # Contact
    telephone: str = Field(..., description="Numéro de téléphone principal")
    email: Optional[str] = None
    whatsapp: Optional[str] = None
    
    # Entreprise
    nom_entreprise: str = Field(..., description="Nom de l'entreprise/atelier")
    description: str = Field(..., description="Description détaillée de l'activité")
    
    # Histoire personnelle
    histoire_artisan: str = Field(
        ...,
        description="Histoire de l'artisan, son parcours, sa passion pour son métier"
    )
    annees_experience: int = Field(..., ge=0, description="Années d'expérience")
    formation: Optional[str] = Field(None, description="Formation reçue")
    
    # Produits/Services
    produits: List[str] = Field(
        ...,
        description="Liste des produits/services proposés"
    )
    categories_produits: List[str] = Field(
        default=[],
        description="Catégories: art, gastronomie, textile, etc."
    )
    prix_moyen_fcfa: Optional[float] = Field(None, description="Prix moyen en FCFA")
    
    # Spécificités locales
    matiere_premiere_locale: bool = Field(
        True,
        description="Utilise des matières premières locales?"
    )
    description_sources: Optional[str] = Field(
        None,
        description="D'où proviennent les matières premières?"
    )
    
    # Certifications et reconnaissances
    certifie: bool = Field(False, description="Artisan certifié?")
    memberships: List[str] = Field(
        default=[],
        description="Appartenance à des associations, guildes, etc."
    )
    prix_ou_reconnaissances: List[str] = Field(
        default=[],
        description="Prix ou reconnaissances reçus"
    )
    
    # Hébergement/Ateliers
    visite_atelier_possible: bool = Field(
        True,
        description="Les touristes peuvent-ils visiter l'atelier?"
    )
    atelier_adresse: Optional[str] = None
    horaires_reception: Optional[str] = Field(None, description="Horaires de réception")
    tarif_visite: Optional[float] = Field(None, description="Tarif de visite en FCFA")
    
    # Atelier et démonstrations
    demonstration_possible: bool = Field(True, description="Peut faire des démonstrations?")
    atelier_enfants: bool = Field(False, description="Ateliers enfants disponibles?")
    cours_disponibles: bool = Field(False, description="Cours/formations disponibles?")
    
    # Vente en ligne/Export
    vente_enligne: bool = Field(False, description="Vend en ligne?")
    website: Optional[str] = None
    plateforme_enligne: Optional[List[str]] = Field(None, description="Plateformes de vente")
    export_possible: bool = Field(False, description="Export possible?")
    
    # Médias
    photo_artisan: Optional[str] = None
    photo_atelier: Optional[str] = None
    galerie_produits: List[str] = Field(default=[])
    video_demonstration: Optional[str] = None
    
    # Histoires de clients
    temoignages_clients: List[str] = Field(
        default=[],
        description="IDs des avis clients"
    )
    nombre_clients_satisfaits: int = Field(default=0)
    
    # Impact social
    employes: int = Field(default=1, description="Nombre d'employés")
    soutien_communaute: Optional[str] = Field(
        None,
        description="Comment l'artisan soutient la communauté"
    )
    formations_dispensees: Optional[str] = Field(
        None,
        description="Formations dispensées aux jeunes?"
    )
    
    # Statut
    actif: bool = Field(True)
    verified: bool = Field(False, description="Profil vérifié?")
    note_moyenne: float = Field(default=0, ge=0, le=5)
    nombre_avis: int = Field(default=0)
    
    # Métadonnées
    date_inscription: datetime = Field(default_factory=datetime.utcnow)
    date_modification: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "nom": "Kone",
                "prenom": "Ibrahim",
                "type_artisan": "tissage",
                "nom_entreprise": "Atelier Kone Tissage Traditionnel",
                "ville": "Ouagadougou",
                "region": "Kadiogo",
                "telephone": "+226 70 22 33 44",
                "description": "Atelier de tissage traditionnel burkinabé",
                "histoire_artisan": "Ibrahim a appris le tissage de son père depuis l'âge de 12 ans. Ses tissus sont reconnus pour leur qualité et leurs motifs traditionnels.",
                "annees_experience": 25,
                "produits": ["pagnes", "tissus décorés", "écharpes", "vêtements"],
                "matiere_premiere_locale": True,
                "visite_atelier_possible": True,
                "tarif_visite": 2000,
                "demonstration_possible": True,
                "atelier_enfants": True,
                "employes": 3,
                "soutien_communaute": "Forme des jeunes du quartier au tissage traditionnel",
                "formations_dispensees": "Oui, 2 jeunes en apprentissage par an"
            }
        }
