from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List
from app.core.database import get_database
from app.core.security import get_current_user, require_admin
from app.core.permissions import Permission
from app.schemas.auth import TokenPayload
from app.services.activity_service import ActivityService
from app.schemas.activity import ActivityCreate, ActivityUpdate, ActivityResponse
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/activities",
    tags=["Activités"],
    responses={404: {"description": "Not found"}},
)


def get_activity_service():
    """Dépendance pour obtenir le service des activités"""
    return ActivityService(get_database())


@router.post("/", response_model=dict, status_code=201)
async def create_activity(
    activity: ActivityCreate,
    admin: TokenPayload = Depends(require_admin),
    service: ActivityService = Depends(get_activity_service)
):
    """Créer une nouvelle activité (ADMIN ONLY)"""
    try:
        activity_id = await service.create_activity(activity)
        return {"id": activity_id, "message": "Activité créée avec succès"}
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/{activity_id}", response_model=ActivityResponse)
async def get_activity(
    activity_id: str,
    current_user: TokenPayload = Depends(get_current_user),
    service: ActivityService = Depends(get_activity_service)
):
    """Récupérer une activité par ID (authentifié requis)"""
    try:
        activity = await service.get_activity(activity_id)
        if not activity:
            raise HTTPException(status_code=404, detail="Activité non trouvée")
        return activity
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/", response_model=List[ActivityResponse])
async def get_all_activities(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: TokenPayload = Depends(get_current_user),
    service: ActivityService = Depends(get_activity_service)
):
    """Récupérer toutes les activités (authentifié requis)"""
    try:
        return await service.get_all_activities(skip=skip, limit=limit)
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/destination/{destination_id}", response_model=List[ActivityResponse])
async def get_activities_by_destination(
    destination_id: str,
    current_user: TokenPayload = Depends(get_current_user),
    service: ActivityService = Depends(get_activity_service)
):
    """Récupérer les activités pour une destination (authentifié requis)"""
    try:
        return await service.get_activities_by_destination(destination_id)
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/type/{type_activite}", response_model=List[ActivityResponse])
async def get_activities_by_type(
    type_activite: str,
    current_user: TokenPayload = Depends(get_current_user),
    service: ActivityService = Depends(get_activity_service)
):
    """Récupérer les activités par type (authentifié requis)"""
    try:
        return await service.get_activities_by_type(type_activite)
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/city/{ville}", response_model=List[ActivityResponse])
async def get_activities_by_city(
    ville: str,
    current_user: TokenPayload = Depends(get_current_user),
    service: ActivityService = Depends(get_activity_service)
):
    """Récupérer les activités par ville (authentifié requis)"""
    try:
        return await service.get_activities_by_city(ville)
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/difficulty/{niveau_difficulte}", response_model=List[ActivityResponse])
async def get_activities_by_difficulty(
    niveau_difficulte: str,
    current_user: TokenPayload = Depends(get_current_user),
    service: ActivityService = Depends(get_activity_service)
):
    """Récupérer les activités par niveau de difficulté (authentifié requis)"""
    try:
        return await service.get_activities_by_difficulty(niveau_difficulte)
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/top-rated/", response_model=List[ActivityResponse])
async def get_top_rated_activities(
    limit: int = Query(5, ge=1, le=20),
    current_user: TokenPayload = Depends(get_current_user),
    service: ActivityService = Depends(get_activity_service)
):
    """Récupérer les activités les mieux notées (authentifié requis)"""
    try:
        return await service.get_top_rated_activities(limit=limit)
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.put("/{activity_id}", response_model=dict)
async def update_activity(
    activity_id: str,
    activity_update: ActivityUpdate,
    admin: TokenPayload = Depends(require_admin),
    service: ActivityService = Depends(get_activity_service)
):
    """Mettre à jour une activité (ADMIN ONLY)"""
    try:
        success = await service.update_activity(activity_id, activity_update)
        if not success:
            raise HTTPException(status_code=404, detail="Activité non trouvée ou aucune mise à jour")
        return {"message": "Activité mise à jour avec succès"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.delete("/{activity_id}", response_model=dict)
async def delete_activity(
    activity_id: str,
    admin: TokenPayload = Depends(require_admin),
    service: ActivityService = Depends(get_activity_service)
):
    """Supprimer une activité (ADMIN ONLY)"""
    try:
        success = await service.delete_activity(activity_id)
        if not success:
            raise HTTPException(status_code=404, detail="Activité non trouvée")
        return {"message": "Activité supprimée avec succès"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


# ============ ADMIN GLOBAL VIEWS ============

@router.get("/admin/all", response_model=List[ActivityResponse])
async def admin_get_all_activities(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    admin: TokenPayload = Depends(require_admin)
):
    """Vue globale de toutes les activités pour l'admin"""
    try:
        from app.core.database import get_database
        db = get_database()
        activities = []
        
        cursor = db["activities"].find().skip(skip).limit(limit)
        async for activity in cursor:
            activity["_id"] = str(activity["_id"])
            activities.append(activity)
        
        return activities
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/admin/stats", response_model=dict)
async def admin_get_activities_stats(admin: TokenPayload = Depends(require_admin)):
    """Statistiques sur les activités pour l'admin"""
    try:
        from app.core.database import get_database
        db = get_database()
        
        total = await db["activities"].count_documents({})
        types = await db["activities"].distinct("type_activite")
        difficulties = await db["activities"].distinct("niveau_difficulte")
        
        return {
            "total_activities": total,
            "activity_types": types,
            "difficulty_levels": difficulties,
            "types_count": len(types)
        }
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")
