from typing import List, Optional
from bson import ObjectId
from app.models.provider import Provider, ProviderCreate, ProviderUpdate, ProviderType
from app.core.database import get_database
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ProviderService:
    """Service pour gérer les fournisseurs de services (Artisans + Restaurants)"""
    
    def __init__(self):
        self.collection_name = "providers"
    
    async def create_provider(self, provider_data: ProviderCreate, owner_id: str, owner_email: str) -> str:
        """Créer un nouveau prestataire"""
        try:
            db = get_database()
            
            provider_dict = {
                "nom_entreprise": provider_data.nom_entreprise,
                "type_service": provider_data.type_service,
                "description": provider_data.description,
                "owner_id": owner_id,
                "owner_email": owner_email,
                "owner_phone": provider_data.owner_phone,
                "ville": provider_data.ville,
                "region": provider_data.region,
                "province": provider_data.province,
                "localite": provider_data.localite,
                "adresse": provider_data.adresse,
                "latitude": provider_data.latitude,
                "longitude": provider_data.longitude,
                "produits_services": provider_data.produits_services,
                "telephone": provider_data.telephone,
                "horaires_ouverture": provider_data.horaires_ouverture,
                "website": provider_data.website,
                
                # Champs du frontend (legacy)
                "budget_moyen_fcfa": provider_data.budget_moyen_fcfa,
                "tarif_visite_fcfa": provider_data.tarif_visite_fcfa,
                "annees_experience": provider_data.annees_experience,
                "matiere_premiere_locale": provider_data.matiere_premiere_locale,
                "employes": provider_data.employes,
                "cuisine_type": provider_data.cuisine_type,
                "utilise_produits_locaux": provider_data.utilise_produits_locaux,
                "employes_locaux": provider_data.employes_locaux,
                "description_culturelle": provider_data.description_culturelle,
                
                "verified": False,
                "note_moyenne": 0.0,
                "nombre_avis": 0,
                "date_creation": datetime.utcnow(),
                "date_modification": datetime.utcnow(),
                "actif": True,
                "publie": False
            }
            
            result = await db[self.collection_name].insert_one(provider_dict)
            logger.info(f"Provider créé: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Erreur création provider: {e}")
            raise
    
    async def get_provider(self, provider_id: str) -> Optional[dict]:
        """Récupérer un provider par ID"""
        try:
            db = get_database()
            provider = await db[self.collection_name].find_one({"_id": ObjectId(provider_id)})
            if provider:
                provider["id"] = str(provider["_id"])
                del provider["_id"]  # Supprimer l'ObjectId original
            return provider
        except Exception as e:
            logger.error(f"Erreur récupération provider: {e}")
            raise
    
    async def get_providers_by_owner(self, owner_id: str) -> List[dict]:
        """Récupérer tous les providers d'un propriétaire"""
        try:
            db = get_database()
            providers = []
            async for provider in db[self.collection_name].find({"owner_id": owner_id}):
                provider["id"] = str(provider["_id"])
                del provider["_id"]  # Supprimer l'ObjectId original
                providers.append(provider)
            return providers
        except Exception as e:
            logger.error(f"Erreur: {e}")
            raise
    
    async def get_all_providers(self, skip: int = 0, limit: int = 50, verified_only: bool = True) -> List[dict]:
        """Récupérer tous les providers (publics)"""
        try:
            db = get_database()
            query = {"actif": True, "publie": True}
            if verified_only:
                query["verified"] = True
            
            providers = []
            async for provider in db[self.collection_name].find(query).skip(skip).limit(limit):
                provider["id"] = str(provider["_id"])
                del provider["_id"]
                providers.append(provider)
            return providers
        except Exception as e:
            logger.error(f"Erreur: {e}")
            raise
    
    async def get_providers_by_type(self, type_service: ProviderType, skip: int = 0, limit: int = 50) -> List[dict]:
        """Récupérer providers par type (Artisan/Restaurant)"""
        try:
            db = get_database()
            providers = []
            async for provider in db[self.collection_name].find({
                "type_service": type_service,
                "actif": True,
                "publie": True,
                "verified": True
            }).skip(skip).limit(limit):
                provider["id"] = str(provider["_id"])
                del provider["_id"]
                providers.append(provider)
            return providers
        except Exception as e:
            logger.error(f"Erreur: {e}")
            raise
    
    async def search_providers(self, query: str, skip: int = 0, limit: int = 50) -> List[dict]:
        """Rechercher des providers"""
        try:
            db = get_database()
            providers = []
            search_query = {
                "$or": [
                    {"nom_entreprise": {"$regex": query, "$options": "i"}},
                    {"description": {"$regex": query, "$options": "i"}},
                    {"produits_services": {"$regex": query, "$options": "i"}},
                    {"ville": {"$regex": query, "$options": "i"}}
                ],
                "actif": True,
                "publie": True,
                "verified": True
            }
            async for provider in db[self.collection_name].find(search_query).skip(skip).limit(limit):
                provider["id"] = str(provider["_id"])
                del provider["_id"]
                providers.append(provider)
            return providers
        except Exception as e:
            logger.error(f"Erreur: {e}")
            raise
    
    async def update_provider(self, provider_id: str, update_data: ProviderUpdate) -> bool:
        """Mettre à jour un provider"""
        try:
            db = get_database()
            update_dict = update_data.model_dump(exclude_unset=True)
            update_dict["date_modification"] = datetime.utcnow()
            
            if update_dict:
                result = await db[self.collection_name].update_one(
                    {"_id": ObjectId(provider_id)},
                    {"$set": update_dict}
                )
                return result.modified_count > 0
            return False
        except Exception as e:
            logger.error(f"Erreur: {e}")
            raise
    
    async def delete_provider(self, provider_id: str) -> bool:
        """Supprimer un provider"""
        try:
            db = get_database()
            result = await db[self.collection_name].delete_one({"_id": ObjectId(provider_id)})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Erreur: {e}")
            raise
    
    async def verify_provider(self, provider_id: str, verified: bool) -> bool:
        """Vérifier/Refuser un provider (ADMIN ONLY)"""
        try:
            db = get_database()
            result = await db[self.collection_name].update_one(
                {"_id": ObjectId(provider_id)},
                {"$set": {"verified": verified, "date_modification": datetime.utcnow()}}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Erreur: {e}")
            raise
    
    async def publish_provider(self, provider_id: str, published: bool) -> bool:
        """Publier/Dépublier un provider"""
        try:
            db = get_database()
            result = await db[self.collection_name].update_one(
                {"_id": ObjectId(provider_id)},
                {"$set": {"publie": published, "date_modification": datetime.utcnow()}}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Erreur: {e}")
            raise
