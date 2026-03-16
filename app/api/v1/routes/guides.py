from fastapi import APIRouter, Depends, HTTPException, Query, status, File, UploadFile
from typing import List
from app.core.database import get_database
from app.core.security import get_current_user, require_admin
from app.core.permissions import Permission, OwnershipCheck
from app.schemas.auth import TokenPayload
from app.models.user import UserRole
from app.services.guide_service import GuideService
from app.services.cloudinary_service import cloudinary_service
from app.schemas.guide import GuideCreate, GuideUpdate, GuideResponse, GuideProfileCreate
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/guides",
    tags=["Guides"],
    responses={404: {"description": "Not found"}},
)


def get_guide_service():
    """Dépendance pour obtenir le service des guides"""
    return GuideService(get_database())


@router.post("/", response_model=dict, status_code=201)
async def create_guide(
    guide: GuideCreate,
    current_user: TokenPayload = Depends(get_current_user),
    service: GuideService = Depends(get_guide_service)
):
    """Créer un nouveau guide (GUIDE ONLY)"""
    try:
        Permission.check_guide(current_user)
        guide_id = await service.create_guide(guide)
        return {"id": guide_id, "message": "Guide créé avec succès"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.post("/profile", response_model=dict, status_code=201)
async def create_guide_profile(
    profile: GuideProfileCreate,
    current_user: TokenPayload = Depends(get_current_user),
    service: GuideService = Depends(get_guide_service)
):
    """Créer/compléter le profil guide (mobile app)"""
    try:
        # Vérifier que l'utilisateur est bien un guide
        if current_user.sub != profile.user_id:
            raise HTTPException(status_code=403, detail="Non autorisé")
        
        if current_user.role != "guide":
            raise HTTPException(status_code=403, detail="Seuls les guides peuvent créer un profil guide")
        
        # Créer le profil guide
        guide_id = await service.create_guide_profile(profile, current_user.sub)
        return {"id": guide_id, "message": "Profil guide créé avec succès"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur création profil guide: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")


@router.get("/me", response_model=GuideResponse, response_model_by_alias=True)
async def get_my_guide_profile(
    current_user: TokenPayload = Depends(get_current_user),
    service: GuideService = Depends(get_guide_service)
):
    """Récupérer mon profil guide (guide connecté)"""
    try:
        # Vérifier que l'utilisateur est bien un guide
        if current_user.role != "guide":
            raise HTTPException(status_code=403, detail="Seuls les guides peuvent accéder à cette ressource")
        
        # Récupérer le profil guide lié à cet utilisateur
        guide = await service.get_guide_by_user_id(current_user.sub)
        if not guide:
            raise HTTPException(status_code=404, detail="Profil guide non trouvé")
        
        logger.info(f"Retour profil guide pour {current_user.sub}: {guide.get('nom_complet')}")
        return guide
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur récupération profil guide: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")


@router.post("/me/photo", response_model=dict)
async def upload_guide_photo(
    file: UploadFile = File(...),
    current_user: TokenPayload = Depends(get_current_user),
    service: GuideService = Depends(get_guide_service)
):
    """Upload photo de profil du guide connecté"""
    try:
        # Vérifier que l'utilisateur est bien un guide
        if current_user.role != "guide":
            raise HTTPException(status_code=403, detail="Seuls les guides peuvent uploader une photo")
        
        # Vérifier le type de fichier
        if not file.content_type or not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Le fichier doit être une image")
        
        # Lire le contenu du fichier
        file_content = await file.read()
        
        # Upload vers Cloudinary
        result = await cloudinary_service.upload_image(
            file_content=file_content,
            folder="guides/profiles",
            public_id=f"guide_{current_user.sub}"
        )
        
        # Mettre à jour le profil du guide avec l'URL de la photo
        db = get_database()
        photo_url = result.get("secure_url")
        
        update_result = await db["guides"].update_one(
            {"user_id": current_user.sub},
            {"$set": {"image": photo_url}}
        )
        
        if update_result.modified_count == 0:
            logger.warning(f"Photo uploadée mais profil guide non trouvé pour user_id: {current_user.sub}")
        
        logger.info(f"Photo de profil uploadée pour guide {current_user.sub}: {photo_url}")
        
        return {
            "message": "Photo de profil uploadée avec succès",
            "photo_url": photo_url,
            "public_id": result.get("public_id")
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur upload photo guide: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")


@router.get("/{guide_id}", response_model=GuideResponse, response_model_by_alias=True)
async def get_guide(
    guide_id: str,
    current_user: TokenPayload = Depends(get_current_user),
    service: GuideService = Depends(get_guide_service)
):
    """Récupérer un guide par ID (authentifié requis)"""
    try:
        guide = await service.get_guide(guide_id)
        if not guide:
            raise HTTPException(status_code=404, detail="Guide non trouvé")
        return guide
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/", response_model=List[GuideResponse], response_model_by_alias=True)
async def get_all_guides(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: TokenPayload = Depends(get_current_user),
    service: GuideService = Depends(get_guide_service)
):
    """Récupérer tous les guides (authentifié requis)"""
    try:
        return await service.get_all_guides(skip=skip, limit=limit)
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/city/{ville}", response_model=List[GuideResponse])
async def get_guides_by_city(
    ville: str,
    current_user: TokenPayload = Depends(get_current_user),
    service: GuideService = Depends(get_guide_service)
):
    """Récupérer les guides par ville (authentifié requis)"""
    try:
        return await service.get_guides_by_city(ville)
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/language/{langue}", response_model=List[GuideResponse])
async def get_guides_by_language(
    langue: str,
    current_user: TokenPayload = Depends(get_current_user),
    service: GuideService = Depends(get_guide_service)
):
    """Récupérer les guides parlant une langue (authentifié requis)"""
    try:
        return await service.get_guides_by_language(langue)
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/specialty/{specialite}", response_model=List[GuideResponse])
async def get_guides_by_specialty(
    specialite: str,
    current_user: TokenPayload = Depends(get_current_user),
    service: GuideService = Depends(get_guide_service)
):
    """Récupérer les guides par spécialité (authentifié requis)"""
    try:
        return await service.get_guides_by_specialty(specialite)
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/with-vehicle/", response_model=List[GuideResponse])
async def get_guides_with_vehicle(
    current_user: TokenPayload = Depends(get_current_user),
    service: GuideService = Depends(get_guide_service)
):
    """Récupérer les guides disposant d'un véhicule (authentifié requis)"""
    try:
        return await service.get_guides_with_vehicle()
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/top-rated/", response_model=List[GuideResponse])
async def get_top_rated_guides(
    limit: int = Query(5, ge=1, le=20),
    current_user: TokenPayload = Depends(get_current_user),
    service: GuideService = Depends(get_guide_service)
):
    """Récupérer les guides les mieux notés (authentifié requis)"""
    try:
        return await service.get_top_rated_guides(limit=limit)
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.put("/{guide_id}", response_model=dict)
async def update_guide(
    guide_id: str,
    guide_update: GuideUpdate,
    current_user: TokenPayload = Depends(get_current_user),
    service: GuideService = Depends(get_guide_service)
):
    """Mettre à jour un guide (propriétaire ou ADMIN)"""
    try:
        # Vérifier que c'est le propriétaire ou admin
        guide = await service.get_guide(guide_id)
        if not guide:
            raise HTTPException(status_code=404, detail="Guide non trouvé")
        
        # Assuming guide has owner_id field
        if hasattr(guide, "owner_id"):
            OwnershipCheck.ensure_ownership(current_user, guide["owner_id"], "profil")
        else:
            Permission.check_guide(current_user)
        
        success = await service.update_guide(guide_id, guide_update)
        if not success:
            raise HTTPException(status_code=404, detail="Guide non trouvé ou aucune mise à jour")
        return {"message": "Guide mis à jour avec succès"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.delete("/{guide_id}", response_model=dict)
async def delete_guide(
    guide_id: str,
    current_user: TokenPayload = Depends(get_current_user),
    service: GuideService = Depends(get_guide_service)
):
    """Supprimer un guide (propriétaire ou ADMIN)"""
    try:
        guide = await service.get_guide(guide_id)
        if not guide:
            raise HTTPException(status_code=404, detail="Guide non trouvé")
        
        if hasattr(guide, "owner_id"):
            OwnershipCheck.ensure_ownership(current_user, guide["owner_id"], "profil")
        else:
            Permission.check_guide(current_user)
        
        success = await service.delete_guide(guide_id)
        if not success:
            raise HTTPException(status_code=404, detail="Guide non trouvé")
        return {"message": "Guide supprimé avec succès"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


# ============ ADMIN GLOBAL VIEWS ============

@router.get("/admin/all", response_model=List[GuideResponse])
async def admin_get_all_guides(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    admin: TokenPayload = Depends(require_admin)
):
    """Vue globale de tous les guides pour l'admin"""
    try:
        from app.core.database import get_database
        db = get_database()
        guides = []
        
        cursor = db["guides"].find().skip(skip).limit(limit)
        async for guide in cursor:
            guide["_id"] = str(guide["_id"])
            guides.append(guide)
        
        return guides
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/admin/stats", response_model=dict)
async def admin_get_guides_stats(admin: TokenPayload = Depends(require_admin)):
    """Statistiques sur les guides pour l'admin"""
    try:
        from app.core.database import get_database
        db = get_database()
        
        total = await db["guides"].count_documents({})
        with_vehicle = await db["guides"].count_documents({"avec_vehicule": True})
        avg_rating = await db["guides"].aggregate([
            {"$group": {"_id": None, "avg_note": {"$avg": "$note"}}}
        ]).to_list(1)
        
        return {
            "total_guides": total,
            "with_vehicle": with_vehicle,
            "average_rating": avg_rating[0].get("avg_note", 0) if avg_rating else 0
        }
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")
