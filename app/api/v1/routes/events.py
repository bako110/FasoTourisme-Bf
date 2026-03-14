from fastapi import APIRouter, HTTPException, Query, Depends, status
from typing import List
from app.core.security import get_current_user, require_admin
from app.core.permissions import Permission
from app.schemas.auth import TokenPayload
from app.models.user import UserRole
from app.schemas.event import EventCreate, EventUpdate, EventResponse
from app.services.event_service import EventService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/events", tags=["Local Events"])
event_service = EventService()


@router.post("/", response_model=dict, status_code=201)
async def create_event(
    event: EventCreate,
    current_user: TokenPayload = Depends(get_current_user)
):
    """Créer un événement local (PROVIDER, GUIDE ou ADMIN)"""
    try:
        # Providers, Guides et Admins peuvent créer des événements
        if current_user.role not in [UserRole.PROVIDER, UserRole.GUIDE, UserRole.ADMIN]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Seuls les providers et guides peuvent créer des événements"
            )
        
        event_id = await event_service.create_event(event, current_user.sub)
        return {"id": event_id, "message": "Événement créé avec succès"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/", response_model=List[EventResponse])
async def list_events(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: TokenPayload = Depends(get_current_user)
):
    """Récupérer tous les événements (authentifié requis)"""
    try:
        return await event_service.get_all_events(skip, limit)
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/city/{ville}", response_model=List[EventResponse])
async def get_by_city(
    ville: str,
    current_user: TokenPayload = Depends(get_current_user)
):
    """Récupérer les événements d'une ville (authentifié requis)"""
    try:
        return await event_service.get_events_by_city(ville)
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/upcoming", response_model=List[EventResponse])
async def get_upcoming(current_user: TokenPayload = Depends(get_current_user)):
    """Récupérer les événements à venir (authentifié requis)"""
    try:
        return await event_service.get_upcoming_events()
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/type/{type_event}", response_model=List[EventResponse])
async def get_by_type(
    type_event: str,
    current_user: TokenPayload = Depends(get_current_user)
):
    """Récupérer les événements par type (authentifié requis)"""
    try:
        return await event_service.get_events_by_type(type_event)
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/{event_id}", response_model=EventResponse)
async def get_one(
    event_id: str,
    current_user: TokenPayload = Depends(get_current_user)
):
    """Récupérer un événement (authentifié requis)"""
    try:
        event = await event_service.get_event(event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Événement non trouvé")
        return event
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.put("/{event_id}")
async def update_one(
    event_id: str,
    event: EventUpdate,
    current_user: TokenPayload = Depends(get_current_user)
):
    """Mettre à jour un événement (propriétaire ou ADMIN)"""
    try:
        existing = await event_service.get_event(event_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Événement non trouvé")
        
        # Vérifier les permissions
        if current_user.role != UserRole.ADMIN:
            if existing.get("organizer_id") != current_user.sub:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Vous ne pouvez modifier que vos propres événements"
                )
        
        success = await event_service.update_event(event_id, event)
        if not success:
            raise HTTPException(status_code=404, detail="Événement non trouvé")
        return {"message": "Événement mis à jour"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.delete("/{event_id}")
async def delete_one(
    event_id: str,
    current_user: TokenPayload = Depends(get_current_user)
):
    """Supprimer un événement (propriétaire ou ADMIN)"""
    try:
        existing = await event_service.get_event(event_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Événement non trouvé")
        
        # Vérifier les permissions
        if current_user.role != UserRole.ADMIN:
            if existing.get("organizer_id") != current_user.sub:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Vous ne pouvez supprimer que vos propres événements"
                )
        
        success = await event_service.delete_event(event_id)
        if not success:
            raise HTTPException(status_code=404, detail="Événement non trouvé")
        return {"message": "Événement supprimé"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


# ============ ROUTES POUR PROVIDERS/GUIDES (Mes Événements) ============

@router.get("/me/events", response_model=List[EventResponse])
async def get_my_events(current_user: TokenPayload = Depends(get_current_user)):
    """Récupérer mes événements (PROVIDER ou GUIDE)"""
    try:
        if current_user.role not in [UserRole.PROVIDER, UserRole.GUIDE, UserRole.ADMIN]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès réservé aux providers et guides"
            )
        
        from app.core.database import get_database
        db = get_database()
        events = []
        
        cursor = db["events"].find({"organizer_id": current_user.sub})
        async for event in cursor:
            event["_id"] = str(event["_id"])
            events.append(event)
        
        return events
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


# ============ ADMIN GLOBAL VIEWS ============

@router.get("/admin/all", response_model=List[EventResponse])
async def admin_get_all_events(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    admin: TokenPayload = Depends(require_admin)
):
    """Vue globale de tous les événements pour l'admin"""
    try:
        from app.core.database import get_database
        db = get_database()
        events = []
        
        cursor = db["events"].find().skip(skip).limit(limit)
        async for event in cursor:
            event["_id"] = str(event["_id"])
            events.append(event)
        
        return events
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")
