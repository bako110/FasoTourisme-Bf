from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class TouristInfo(BaseModel):
    """Modèle pour les informations pratiques utiles aux touristes"""
    
    id: Optional[str] = Field(None, alias="_id")
    
    # Information catégorie
    categorie: str = Field(
        ...,
        description="visa, douane, documents, monnaie, langue, culture, coutumes, lois, fêtes, etc."
    )
    
    # Titres
    titre: str = Field(..., description="Titre court de l'info")
    titre_long: Optional[str] = None
    
    # Contenu
    description: str = Field(..., description="Contenu détaillé")
    conseils_pratiques: List[str] = Field(..., description="Conseils pratiques")
    
    # Applicabilité
    zone_applicabilite: Optional[str] = Field(
        None,
        description="tout_le_pays, region_specifique, etc."
    )
    regions_concernees: Optional[List[str]] = None
    
    # Visa et documents
    visa_requis: Optional[bool] = None
    duree_validite_visa_jours: Optional[int] = None
    cout_visa_fcfa: Optional[float] = None
    ou_demander_visa: Optional[List[str]] = None
    documents_requis: Optional[List[str]] = None
    
    # Douane
    restrictions_douane: Optional[List[str]] = None
    Articles_interdits: Optional[List[str]] = None
    limite_devises: Optional[float] = None
    limite_alcool_litre: Optional[float] = None
    limite_tabac_paquets: Optional[int] = None
    
    # Monnaie
    monnaie: Optional[str] = Field(None, description="FCFA (franc CFA)")
    taux_change_approximatif: Optional[str] = None
    meilleure_facon_changer: Optional[List[str]] = None
    zones_dechange: Optional[List[str]] = Field(None, description="IDs des banques/ATM")
    
    # Langue
    langues_principales: Optional[List[str]] = None
    langues_parlees_toutes_regions: Optional[List[str]] = None
    langues_tourisme: Optional[List[str]] = None
    phrases_utiles: Optional[dict] = Field(None, description="Traductions utiles")
    
    # Jours fériés et périodes
    jours_feries: Optional[List[str]] = None
    périodes_importantes: Optional[List[str]] = None
    periodes_fermeture_services: Optional[List[str]] = None
    
    # Coutumes et respect
    coutumes_importantes: Optional[List[str]] = None
    respect_culture: Optional[str] = None
    code_vestimentaire: Optional[str] = None
    interdictions_culturelles: Optional[List[str]] = None
    
    # Religion
    religions_principales: Optional[List[str]] = None
    respect_religion: Optional[List[str]] = None
    lieux_culte_visitable: Optional[bool] = None
    jours_sabbat: Optional[List[str]] = None
    
    # Lois et règlementations
    lois_specifiques: Optional[List[str]] = None
    peines_infractions: Optional[dict] = None
    comportements_illegaux: Optional[List[str]] = None
    tolerance_localisation: Optional[str] = None
    
    # Électricité et voltages
    voltage_electricite: Optional[int] = Field(None, description="En volts")
    prises_electriques: Optional[str] = None
    necessites_adaptateurs: Optional[bool] = None
    
    # Climat et packing
    meilleure_periode: Optional[str] = None
    periode_pluie: Optional[str] = None
    temperature_moyenne: Optional[str] = None
    articles_a_emporter: Optional[List[str]] = None
    Articles_a_eviter: Optional[List[str]] = None
    
    # Santé
    vaccins_recommandes: Optional[List[str]] = None
    maladies_endémiques: Optional[List[str]] = None
    assurance_voyage_recommandee: Optional[bool] = None
    
    # Transport
    permis_conduire_international: Optional[bool] = None
    cote_circulation: Optional[str] = Field(None, description="Côté droit ou gauche")
    limitations_vitesse: Optional[str] = None
    essence_disponible: Optional[bool] = None
    
    # Pourboires
    pourcentage_recommande: Optional[float] = None
    situations_pourboire: Optional[List[str]] = None
    
    # Photographie
    restrictions_photo: Optional[List[str]] = None
    zones_interdites_photo: Optional[List[str]] = None
    demander_avant_photo: Optional[bool] = None
    
    # Contact utile
    ambassade_consulat_france: Optional[str] = None
    numero_urgence_france: Optional[str] = None
    site_gouvernement: Optional[str] = None
    
    # Statut
    important: bool = Field(False, description="Information importante à signaler?")
    date_creation: datetime = Field(default_factory=datetime.utcnow)
    date_modification: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "categorie": "visa",
                "titre": "Visa pour le Burkina Faso",
                "description": "Les ressortissants de certains pays n'ont pas besoin de visa...",
                "visa_requis": True,
                "cout_visa_fcfa": 50000,
                "documents_requis": ["passeport valide 6 mois", "formulaire", "photo"],
                "conseils_pratiques": ["Faire la demande 2 semaines avant", "Amener tous les documents"]
            }
        }
