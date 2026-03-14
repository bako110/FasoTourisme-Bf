from fastapi import APIRouter, HTTPException, Query, Depends, status
from typing import List
from app.core.security import get_current_user, require_admin
from app.core.permissions import Permission
from app.schemas.auth import TokenPayload
from app.models.user import UserRole
from app.schemas.story import StoryCreate, StoryUpdate, StoryResponse
from app.services.story_service import StoryService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/stories", tags=["Visitor Stories"])
story_service = StoryService()


@router.post("/", response_model=dict, status_code=201)
async def create_story(
    story: StoryCreate,
    current_user: TokenPayload = Depends(get_current_user)
):
    """Créer une histoire de visiteur (TOURIST ONLY)"""
    try:
        Permission.check_tourist(current_user)
        story_id = await story_service.create_story(story, current_user.sub)
        return {"id": story_id, "message": "Histoire créée avec succès"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/", response_model=List[StoryResponse])
async def list_stories(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: TokenPayload = Depends(get_current_user)
):
    """Récupérer les histoires publiées (authentifié requis)"""
    try:
        return await story_service.get_all_stories(skip, limit)
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/type/{traveler_type}", response_model=List[StoryResponse])
async def get_by_traveler_type(
    traveler_type: str,
    current_user: TokenPayload = Depends(get_current_user)
):
    """Récupérer les histoires par type de voyageur (authentifié requis)"""
    try:
        return await story_service.get_stories_by_traveler_type(traveler_type)
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/featured", response_model=List[StoryResponse])
async def get_featured(current_user: TokenPayload = Depends(get_current_user)):
    """Récupérer les histoires en avant (authentifié requis)"""
    try:
        return await story_service.get_featured_stories()
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/emotional", response_model=List[StoryResponse])
async def get_emotional(current_user: TokenPayload = Depends(get_current_user)):
    """Récupérer les histoires les plus émouvantes (authentifié requis)"""
    try:
        return await story_service.get_most_emotional_stories()
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/top-rated", response_model=List[StoryResponse])
async def get_top_rated(current_user: TokenPayload = Depends(get_current_user)):
    """Récupérer les histoires les mieux notées (authentifié requis)"""
    try:
        return await story_service.get_top_rated_stories()
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/{story_id}", response_model=StoryResponse)
async def get_one(
    story_id: str,
    current_user: TokenPayload = Depends(get_current_user)
):
    """Récupérer une histoire (authentifié requis)"""
    try:
        story = await story_service.get_story(story_id)
        if not story:
            raise HTTPException(status_code=404, detail="Histoire non trouvée")
        return story
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.put("/{story_id}")
async def update_one(
    story_id: str,
    story: StoryUpdate,
    current_user: TokenPayload = Depends(get_current_user)
):
    """Mettre à jour une histoire (propriétaire, MODERATOR ou ADMIN)"""
    try:
        existing = await story_service.get_story(story_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Histoire non trouvée")
        
        # Vérifier les permissions
        if current_user.role not in [UserRole.MODERATOR, UserRole.ADMIN]:
            if existing.get("author_id") != current_user.sub:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Vous ne pouvez modifier que vos propres histoires"
                )
        
        success = await story_service.update_story(story_id, story)
        if not success:
            raise HTTPException(status_code=404, detail="Histoire non trouvée")
        return {"message": "Histoire mise à jour"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.post("/{story_id}/feature")
async def feature_story(
    story_id: str,
    admin: TokenPayload = Depends(require_admin)
):
    """Mettre en avant une histoire (ADMIN ONLY)"""
    try:
        success = await story_service.feature_story(story_id)
        if not success:
            raise HTTPException(status_code=404, detail="Histoire non trouvée")
        return {"message": "Histoire mise en avant"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.delete("/{story_id}")
async def delete_one(
    story_id: str,
    current_user: TokenPayload = Depends(get_current_user)
):
    """Supprimer une histoire (propriétaire, MODERATOR ou ADMIN)"""
    try:
        existing = await story_service.get_story(story_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Histoire non trouvée")
        
        # Vérifier les permissions
        if current_user.role not in [UserRole.MODERATOR, UserRole.ADMIN]:
            if existing.get("author_id") != current_user.sub:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Vous ne pouvez supprimer que vos propres histoires"
                )
        
        success = await story_service.delete_story(story_id)
        if not success:
            raise HTTPException(status_code=404, detail="Histoire non trouvée")
        return {"message": "Histoire supprimée"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


# ============ ADMIN GLOBAL VIEWS ============

@router.get("/admin/all", response_model=List[StoryResponse])
async def admin_get_all_stories(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    admin: TokenPayload = Depends(require_admin)
):
    """Vue globale de toutes les histoires pour l'admin"""
    try:
        from app.core.database import get_database
        db = get_database()
        stories = []
        
        cursor = db["stories"].find().skip(skip).limit(limit)
        async for story in cursor:
            story["_id"] = str(story["_id"])
            stories.append(story)
        
        return stories
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.post("/admin/{story_id}/flag")
async def flag_story(
    story_id: str,
    reason: str,
    admin: TokenPayload = Depends(require_admin)
):
    """Signaler une histoire comme inappropriée (ADMIN)"""
    try:
        success = await story_service.flag_story(story_id, reason)
        if not success:
            raise HTTPException(status_code=404, detail="Histoire non trouvée")
        return {"message": "Histoire signalée comme inappropriée"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/admin/stats", response_model=dict)
async def admin_get_stories_stats(admin: TokenPayload = Depends(require_admin)):
    """Statistiques sur les histoires pour l'admin"""
    try:
        from app.core.database import get_database
        db = get_database()
        
        total = await db["stories"].count_documents({})
        featured = await db["stories"].count_documents({"featured": True})
        flagged = await db["stories"].count_documents({"flagged": True})
        
        return {
            "total_stories": total,
            "featured_stories": featured,
            "flagged_stories": flagged
        }
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")
