from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.auth import (
    TokenRequest, TokenResponse, UserRegister, UserResponse,
    PasswordUpdate, TokenPayload
)
from app.services.user_service import UserService
from app.core.security import (
    get_current_user, require_admin, create_access_token,
    verify_password, hash_password
)
from app.models.user import UserRole
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentification"])
user_service = UserService()


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(user_data: UserRegister):
    """Créer un nouveau compte utilisateur"""
    try:
        # Vérifier l'email
        existing = await user_service.get_user_by_email(user_data.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email déjà utilisé"
            )
        
        # Créer l'utilisateur
        user_id = await user_service.register_user(user_data)
        user = await user_service.get_user_by_id(user_id)
        
        return UserResponse(
            id=user_id,
            email=user["email"],
            telephone=user.get("telephone"),
            nom_complet=user["nom_complet"],
            role=UserRole(user["role"]),
            actif=user["actif"],
            verifiee=user["verifiee"],
            profil_type=user.get("profil_type"),
            date_creation=user["date_creation"]
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Erreur lors de l'enregistrement: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.post("/login", response_model=TokenResponse)
async def login(credentials: TokenRequest):
    """Authentifier et obtenir un JWT token (avec email OU téléphone)"""
    try:
        # Vérifier les identifiants (email OU téléphone)
        user = await user_service.authenticate_user(credentials.login, credentials.motdepasse)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Identifiants incorrects",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Créer le token
        token, expire = create_access_token(
            user_id=str(user["_id"]),
            email=user["email"],
            role=UserRole(user["role"]),
            permissions=user.get("permissions_specifiques", [])
        )
        
        expires_in = int((expire - __import__('datetime').datetime.utcnow()).total_seconds())
        
        return TokenResponse(
            access_token=token,
            expires_in=expires_in,
            user_id=str(user["_id"]),
            email=user["email"],
            role=UserRole(user["role"])
        )
    except Exception as e:
        logger.error(f"Erreur lors de la connexion: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(current_user: TokenPayload = Depends(get_current_user)):
    """Récupérer le profil de l'utilisateur courant"""
    try:
        user = await user_service.get_user_by_id(current_user.sub)
        if not user:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
        
        return UserResponse(
            id=str(user["_id"]),
            email=user["email"],
            telephone=user.get("telephone"),
            nom_complet=user["nom_complet"],
            role=UserRole(user["role"]),
            actif=user["actif"],
            verifiee=user["verifiee"],
            profil_type=user.get("profil_type"),
            date_creation=user["date_creation"]
        )
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.put("/me/password")
async def change_password(
    password_data: PasswordUpdate,
    current_user: TokenPayload = Depends(get_current_user)
):
    """Changer le mot de passe"""
    try:
        user = await user_service.get_user_by_id(current_user.sub)
        
        # Vérifier ancien mot de passe
        if not verify_password(password_data.ancien_motdepasse, user["motdepasse_hash"]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ancien mot de passe incorrect"
            )
        
        # Vérifier confirmation
        if password_data.nouveau_motdepasse != password_data.confirmation:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Les nouveaux mots de passe ne correspondent pas"
            )
        
        # Mettre à jour
        from app.core.database import get_database
        from bson import ObjectId
        db = get_database()
        await db["users"].update_one(
            {"_id": ObjectId(current_user.sub)},
            {"$set": {"motdepasse_hash": hash_password(password_data.nouveau_motdepasse)}}
        )
        
        return {"message": "Mot de passe changé avec succès"}
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/admin/users")
async def list_all_users(admin: TokenPayload = Depends(require_admin)):
    """Lister tous les utilisateurs (ADMIN ONLY)"""
    try:
        from app.core.database import get_database
        db = get_database()
        users = []
        async for user in db["users"].find():
            users.append({
                "id": str(user["_id"]),
                "email": user["email"],
                "nom_complet": user["nom_complet"],
                "role": user["role"],
                "actif": user["actif"],
                "verifiee": user["verifiee"],
                "date_creation": user["date_creation"]
            })
        return users
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.put("/admin/users/{user_id}/role")
async def update_user_role(
    user_id: str,
    new_role: str,
    admin: TokenPayload = Depends(require_admin)
):
    """Changer le rôle d'un utilisateur (ADMIN ONLY)"""
    try:
        role = UserRole(new_role)
        success = await user_service.update_user_role(user_id, role)
        
        if not success:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
        
        return {"message": f"Rôle changé à {new_role}"}
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Rôle invalide: {new_role}")
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.delete("/admin/users/{user_id}")
async def deactivate_user(
    user_id: str,
    admin: TokenPayload = Depends(require_admin)
):
    """Désactiver un utilisateur (ADMIN ONLY)"""
    try:
        success = await user_service.deactivate_user(user_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
        
        return {"message": "Utilisateur désactivé"}
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")
