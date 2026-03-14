from typing import List, Optional
from bson import ObjectId
from app.models.user import User, UserRole
from app.schemas.auth import UserRegister, TokenResponse
from app.core.database import get_database
from app.core.security import hash_password, verify_password, create_access_token
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class UserService:
    """Service pour gérer les utilisateurs"""
    
    def __init__(self):
        self.collection_name = "users"
    
    async def register_user(self, user_data: UserRegister) -> str:
        """Enregistrer un nouvel utilisateur"""
        try:
            db = get_database()
            
            # Vérifier que l'email n'existe pas déjà
            existing = await db[self.collection_name].find_one({"email": user_data.email})
            if existing:
                raise ValueError("Email déjà utilisé")
            
            # Vérifier que le téléphone n'existe pas déjà (si fourni)
            if user_data.telephone:
                existing_phone = await db[self.collection_name].find_one({"telephone": user_data.telephone})
                if existing_phone:
                    raise ValueError("Numéro de téléphone déjà utilisé")
            
            # Créer le document utilisateur
            # Empêcher l'auto-attribution du rôle ADMIN (sécurité)
            role = user_data.role if user_data.role != UserRole.ADMIN else UserRole.TOURIST
            
            user_dict = {
                "email": user_data.email,
                "nom_complet": user_data.nom_complet,
                "motdepasse_hash": hash_password(user_data.motdepasse),
                "role": role.value,
                "profil_type": user_data.profil_type,
                "telephone": user_data.telephone,
                "actif": True,
                "verifiee": False,  # À vérifier par email
                "date_creation": datetime.utcnow(),
                "permissions_specifiques": []
            }
            
            result = await db[self.collection_name].insert_one(user_dict)
            logger.info(f"Nouvel utilisateur créé: {result.inserted_id}")
            return str(result.inserted_id)
            
        except Exception as e:
            logger.error(f"Erreur lors de l'enregistrement: {e}")
            raise
    
    async def authenticate_user(self, login: str, motdepasse: str) -> Optional[dict]:
        """Authentifier un utilisateur avec email OU téléphone"""
        try:
            db = get_database()
            
            # Chercher par email OU téléphone
            import re
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            
            if re.match(email_pattern, login):
                # C'est un email
                user = await db[self.collection_name].find_one({"email": login})
            else:
                # C'est un numéro de téléphone
                user = await db[self.collection_name].find_one({"telephone": login})
            
            if not user:
                return None
            
            if not user.get("actif"):
                raise ValueError("Utilisateur désactivé")
            
            if not verify_password(motdepasse, user.get("motdepasse_hash", "")):
                return None
            
            # Mettre à jour la dernière connexion
            await db[self.collection_name].update_one(
                {"_id": user["_id"]},
                {"$set": {"date_derniere_connexion": datetime.utcnow()}}
            )
            
            return user
            
        except Exception as e:
            logger.error(f"Erreur lors de l'authentification: {e}")
            raise
    
    async def get_user_by_id(self, user_id: str) -> Optional[dict]:
        """Récupérer un utilisateur par ID"""
        try:
            db = get_database()
            user = await db[self.collection_name].find_one({"_id": ObjectId(user_id)})
            if user:
                user["id"] = str(user["_id"])
            return user
        except Exception as e:
            logger.error(f"Erreur lors de la récupération: {e}")
            raise
    
    async def get_user_by_email(self, email: str) -> Optional[dict]:
        """Récupérer un utilisateur par email"""
        try:
            db = get_database()
            user = await db[self.collection_name].find_one({"email": email})
            if user:
                user["id"] = str(user["_id"])
            return user
        except Exception as e:
            logger.error(f"Erreur: {e}")
            raise
    
    async def update_user_role(self, user_id: str, new_role: UserRole) -> bool:
        """Changer le rôle d'un utilisateur (ADMIN ONLY)"""
        try:
            db = get_database()
            result = await db[self.collection_name].update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"role": new_role.value}}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Erreur: {e}")
            raise
    
    async def deactivate_user(self, user_id: str) -> bool:
        """Désactiver un utilisateur"""
        try:
            db = get_database()
            result = await db[self.collection_name].update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"actif": False}}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Erreur: {e}")
            raise
    
    async def get_users_by_role(self, role: UserRole) -> List[dict]:
        """Récupérer tous les utilisateurs avec un rôle spécifique"""
        try:
            db = get_database()
            users = []
            async for user in db[self.collection_name].find({"role": role.value}):
                user["id"] = str(user["_id"])
                users.append(user)
            return users
        except Exception as e:
            logger.error(f"Erreur: {e}")
            raise
