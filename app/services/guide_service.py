from typing import List, Optional
from bson import ObjectId
from app.schemas.guide import GuideCreate, GuideUpdate, GuideProfileCreate
from app.core.database import get_database
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class GuideService:
    """Service pour gérer les guides touristiques"""
    
    def __init__(self, db=None):
        self.db = db
        self.collection_name = "guides"
    
    def _get_db(self):
        if self.db is not None:
            return self.db
        return get_database()
    
    def _format_guide(self, guide: dict) -> dict:
        """Convertir un document MongoDB en dict pour le frontend - convertir tous les ObjectId en strings"""
        if guide:
            # Convertir _id à un string
            guide["_id"] = str(guide["_id"])
            guide["id"] = guide["_id"]
            
            # Convertir user_id si présent
            if "user_id" in guide and guide["user_id"] and not isinstance(guide["user_id"], str):
                guide["user_id"] = str(guide["user_id"])
            
            # Mapper les champs pour le frontend
            guide["nom_complet"] = f"{guide.get('nom', '')} {guide.get('prenom', '')}".strip()
            guide["bio"] = guide.get("biographie")
            guide["langues_parlees"] = guide.get("langues", [])
            guide["regions_couvertes"] = guide.get("destinations_principales", [])
            guide["tarif_journee"] = guide.get("tarif_journee_fcfa")
            guide["experience_annees"] = guide.get("annees_experience")
            
            # Normaliser les images: photo (ancien) → image (nouveau)
            image = guide.get("image") or guide.get("photo")
            if image:
                if isinstance(image, str):
                    guide["image"] = image
                elif isinstance(image, dict) and "url" in image:
                    guide["image"] = image["url"]
                else:
                    guide["image"] = str(image) if image else None
            else:
                guide["image"] = None
            
            # Pour backward compatibility avec l'ancien champ
            guide["photo_profil"] = guide.get("image")
                
            guide["certifications"] = guide.get("certifications", [])
            guide["tours_proposes"] = guide.get("tours_proposes", [])
        
        return guide
    
    async def create_guide_profile(self, profile: GuideProfileCreate, user_id: str) -> str:
        """Créer un profil guide depuis l'application mobile"""
        try:
            db = self._get_db()
            
            # Séparer le nom complet en nom et prénom
            nom_parts = profile.nom_complet.strip().split(maxsplit=1)
            nom = nom_parts[0] if len(nom_parts) > 0 else ""
            prenom = nom_parts[1] if len(nom_parts) > 1 else ""
            
            # Récupérer l'utilisateur pour obtenir son email
            user = await db["users"].find_one({"_id": ObjectId(user_id)})
            if not user:
                raise ValueError("Utilisateur non trouvé")
            
            # Construire le document guide
            guide_dict = {
                "user_id": user_id,
                "nom": nom,
                "prenom": prenom,
                "telephone": profile.telephone,
                "email": user.get("email"),
                "photo": profile.photo,
                "ville": "",  # À compléter plus tard
                "region": profile.regions_couvertes[0] if profile.regions_couvertes else "",
                "langues": profile.langues_parlees,
                "specialites": profile.specialites,
                "licence_guide": True,
                "articles_guides": None,
                "annees_experience": profile.experience_annees,
                "destinations_principales": profile.regions_couvertes,
                "tarif_journee_fcfa": profile.tarif_journee,
                "tarif_demi_journee_fcfa": profile.tarif_journee / 2,
                "biographie": profile.bio,
                "possede_vehicule": profile.possede_vehicule,
                "type_vehicule": profile.type_vehicule,
                "disponible": profile.disponible,
                "jours_disponibilite": ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"],
                "note_moyenne": 0,
                "nombre_avis": 0,
                "nombre_clients_satisfaits": 0,
                "activites_animees": [],
                "destinations_reconnues": [],
                "tours_proposes": getattr(profile, "tours_proposes", []),
                "actif": True,
                "verified": False,
                "date_inscription": datetime.utcnow(),
                "date_modification": datetime.utcnow()
            }
            
            existing_guide = await db[self.collection_name].find_one({"user_id": user_id})

            if existing_guide:
                guide_dict["date_inscription"] = existing_guide.get("date_inscription", datetime.utcnow())
                result = await db[self.collection_name].update_one(
                    {"_id": existing_guide["_id"]},
                    {"$set": guide_dict}
                )
                logger.info(f"Profil guide mis à jour via create profile: {existing_guide['_id']}, modifié: {result.modified_count > 0}")
                return str(existing_guide["_id"])

            result = await db[self.collection_name].insert_one(guide_dict)
            logger.info(f"Profil guide créé: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Erreur lors de la création du profil guide: {e}", exc_info=True)
            raise
    
    async def create_guide(self, guide: GuideCreate) -> str:
        """Créer un nouveau guide"""
        try:
            db = self._get_db()
            guide_dict = guide.model_dump()
            result = await db[self.collection_name].insert_one(guide_dict)
            logger.info(f"Guide créé: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Erreur lors de la création d'un guide: {e}")
            raise
    
    async def get_guide(self, guide_id: str) -> Optional[dict]:
        """Récupérer un guide par ID"""
        try:
            db = self._get_db()
            guide = await db[self.collection_name].find_one({"_id": ObjectId(guide_id)})
            return self._format_guide(guide) if guide else None
        except Exception as e:
            logger.error(f"Erreur lors de la récupération du guide: {e}")
            raise
    
    async def get_guide_by_user_id(self, user_id: str) -> Optional[dict]:
        """Récupérer un guide par user_id"""
        try:
            db = self._get_db()
            guide = await db[self.collection_name].find_one({"user_id": user_id})
            if guide:
                guide = self._format_guide(guide)
                logger.info(f"Guide récupéré pour user_id {user_id}: {guide.get('nom_complet')}")
            return guide
        except Exception as e:
            logger.error(f"Erreur lors de la récupération du guide par user_id: {e}")
            raise
    
    async def get_all_guides(self, skip: int = 0, limit: int = 10) -> List[dict]:
        """Récupérer tous les guides"""
        try:
            db = self._get_db()
            guides = []
            async for guide in db[self.collection_name].find({"actif": True}).skip(skip).limit(limit):
                guides.append(self._format_guide(guide))
            return guides
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des guides: {e}")
            raise
    
    async def get_guides_by_city(self, ville: str) -> List[dict]:
        """Récupérer les guides par ville"""
        try:
            db = self._get_db()
            guides = []
            async for guide in db[self.collection_name].find({"ville": ville, "actif": True}):
                guides.append(self._format_guide(guide))
            return guides
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des guides par ville: {e}")
            raise
    
    async def get_guides_by_language(self, langue: str) -> List[dict]:
        """Récupérer les guides parlant une langue"""
        try:
            db = self._get_db()
            guides = []
            async for guide in db[self.collection_name].find({
                "langues": langue,
                "actif": True
            }):
                guides.append(self._format_guide(guide))
            return guides
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des guides par langue: {e}")
            raise
    
    async def get_guides_by_specialty(self, specialite: str) -> List[dict]:
        """Récupérer les guides par spécialité"""
        try:
            db = get_database()
            guides = []
            async for guide in db[self.collection_name].find({
                "specialites": specialite,
                "actif": True
            }):
                guide["id"] = str(guide["_id"])
                guides.append(guide)
            return guides
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des guides par spécialité: {e}")
            raise
    
    async def get_guides_with_vehicle(self) -> List[dict]:
        """Récupérer les guides disposant d'un véhicule"""
        try:
            db = get_database()
            guides = []
            async for guide in db[self.collection_name].find({
                "possede_vehicule": True,
                "actif": True
            }):
                guide["id"] = str(guide["_id"])
                guides.append(guide)
            return guides
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des guides avec véhicule: {e}")
            raise
    
    async def update_guide(self, guide_id: str, guide_update: GuideUpdate) -> bool:
        """Mettre à jour un guide"""
        try:
            db = self._get_db()
            # Convertir le modèle en dict en utilisant les noms de champs (pas les alias)
            update_data = guide_update.model_dump(exclude_unset=True, by_alias=False)
            update_data["date_modification"] = datetime.utcnow()
            
            logger.info(f"Mise à jour guide {guide_id} avec: {update_data}")
            
            if update_data:
                result = await db[self.collection_name].update_one(
                    {"_id": ObjectId(guide_id)},
                    {"$set": update_data}
                )
                logger.info(
                    f"Guide mis à jour: {guide_id}, trouvé: {result.matched_count > 0}, modifié: {result.modified_count > 0}"
                )
                return result.matched_count > 0
            return False
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour du guide: {e}")
            raise
    
    async def delete_guide(self, guide_id: str) -> bool:
        """Supprimer un guide"""
        try:
            db = self._get_db()
            result = await db[self.collection_name].delete_one({"_id": ObjectId(guide_id)})
            logger.info(f"Guide supprimé: {guide_id}")
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Erreur lors de la suppression du guide: {e}")
            raise
    
    async def get_top_rated_guides(self, limit: int = 5) -> List[dict]:
        """Récupérer les guides les mieux notés"""
        try:
            db = self._get_db()
            guides = []
            async for guide in db[self.collection_name].find({"actif": True, "verified": True}).sort("note_moyenne", -1).limit(limit):
                guides.append(self._format_guide(guide))
            return guides
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des meilleurs guides: {e}")
            raise
