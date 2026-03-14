from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class LocalCuisine(BaseModel):
    """Modèle pour les restaurants et cuisines locales"""
    
    id: Optional[str] = Field(None, alias="_id")
    
    # Informations basiques
    nom: str = Field(..., description="Nom du restaurant/point de vente")
    description: str = Field(..., description="Description du restaurant")
    type_restaurant: str = Field(
        ...,
        description="petit_restaurant, restaurant_traditionnel, kebab, cafe, maquis, etc."
    )
    
    # Localisation
    ville: str = Field(...)
    region: str = Field(...)
    province: str = Field(...)
    localite: str = Field(...)
    adresse: str = Field(...)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    
    # Contact
    telephone: Optional[str] = None
    email: Optional[str] = None
    
    # Spécialités
    specialites: List[str] = Field(
        ...,
        description="Plats spécialisés du restaurant"
    )
    cuisine_type: str = Field(
        ...,
        description="ouest_africaine, burkinabe, moderne, fusion, etc."
    )
    
    # Produits locaux
    utilise_produits_locaux: bool = Field(
        True,
        description="Utilise des produits locaux?"
    )
    produits_sources: Optional[str] = Field(
        None,
        description="Source des produits locaux"
    )
    bio_ou_organiques: bool = Field(
        False,
        description="Produits bio/organiques?"
    )
    
    # Tarifs
    budget_moyen_fcfa: float = Field(
        ...,
        description="Budget moyen pour repas en FCFA"
    )
    prix_min_fcfa: Optional[float] = None
    prix_max_fcfa: Optional[float] = None
    
    # Ambiance et services
    ambiance: List[str] = Field(
        default=[],
        description="intime, famille, groupe, touristique, lounge, etc."
    )
    services: List[str] = Field(
        default=[],
        description="wifi, parking, terrasse, livraison, etc."
    )
    capacite: Optional[int] = Field(None, description="Nombre de places")
    
    # Horaires
    horaires_ouverture: Optional[str] = Field(None, description="Horaires d'ouverture")
    ferme_dimanche: Optional[bool] = None
    ferme_jours: Optional[List[str]] = None
    livraison_possible: bool = Field(False)
    
    # Propriétaire/Personnel
    proprietaire_nom: str = Field(..., description="Nom du propriétaire")
    proprietaire_histoire: Optional[str] = Field(
        None,
        description="Histoires du propriétaire et sa passion pour la cuisine"
    )
    generations: int = Field(
        default=1,
        description="Depuis combien de générations?"
    )
    
    # Chef cuisinier
    chef_nom: Optional[str] = Field(None, description="Nom du chef")
    chef_experience: Optional[int] = None
    chef_specialites: Optional[List[str]] = None
    
    # Recettes traditionnelles
    recettes_traditionelles: bool = Field(
        True,
        description="Utilise les recettes traditionnelles?"
    )
    recette_histoire: Optional[str] = Field(
        None,
        description="Histoire et signification des recettes"
    )
    transmission_jeunes: Optional[str] = Field(
        None,
        description="Comment les recettes sont transmises aux jeunes?"
    )
    
    # Médias
    photo_restaur: Optional[str] = None
    galerie_plats: List[str] = Field(default=[])
    video_preparation: Optional[str] = None
    
    # Événements et groupes
    accepte_groupes: bool = Field(True, description="Accepte les groupes?")
    taille_groupe_min: Optional[int] = None
    taille_groupe_max: Optional[int] = None
    reservation_groupe_requise: bool = Field(False)
    events_privees: bool = Field(False, description="Peut accueillir des événements privés?")
    
    # Impact communautaire
    employes_locaux: int = Field(default=0, description="Nombre d'employés locaux")
    apprentissage_jeunes: bool = Field(
        False,
        description="Accepte les apprentis?"
    )
    partenariat_producteurs: Optional[str] = Field(
        None,
        description="Partenariats avec producteurs locaux"
    )
    
    # Certifications
    hygiene_certifiee: bool = Field(False)
    normes_sanitaires: bool = Field(True)
    
    # Évaluations
    note_moyenne: float = Field(default=0, ge=0, le=5)
    nombre_avis: int = Field(default=0)
    plat_populaire: Optional[str] = Field(None, description="Plat le plus apprécié")
    
    # Statut
    actif: bool = Field(True)
    publie: bool = Field(True)
    date_creation: datetime = Field(default_factory=datetime.utcnow)
    date_modification: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "nom": "Maquis de Mère Salimata",
                "description": "Authentique maquis familial avec excellente cuisine traditionnelle",
                "type_restaurant": "maquis",
                "ville": "Ouagadougou",
                "region": "Kadiogo",
                "specialites": ["riz gras", "pâte d'arachide", "brochettes", "bissap"],
                "cuisine_type": "burkinabe",
                "utilise_produits_locaux": True,
                "budget_moyen_fcfa": 3000,
                "proprietaire_nom": "Salimata Ouedraogo",
                "proprietaire_histoire": "Salimata prépare les recettes de sa mère depuis 30 ans",
                "generations": 2,
                "recettes_traditionelles": True,
                "employes_locaux": 4,
                "apprentissage_jeunes": True,
                "note_moyenne": 4.7
            }
        }
