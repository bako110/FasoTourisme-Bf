from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from app.core.database import get_database
from app.core.security import get_current_user, require_admin
from app.core.permissions import Permission
from app.schemas.auth import TokenPayload
from app.services.destination_service import DestinationService
from app.schemas.destination import DestinationCreate, DestinationUpdate, DestinationResponse
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/destinations",
    tags=["Destinations"],
    responses={404: {"description": "Not found"}},
)


def get_destination_service():
    """Dépendance pour obtenir le service des destinations"""
    return DestinationService(get_database())


@router.post("/", response_model=dict, status_code=201)
async def create_destination(
    destination: DestinationCreate,
    admin: TokenPayload = Depends(require_admin),
    service: DestinationService = Depends(get_destination_service)
):
    """Créer une nouvelle destination (ADMIN ONLY)"""
    try:
        destination_id = await service.create_destination(destination)
        return {"id": destination_id, "message": "Destination créée avec succès"}
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/{destination_id}", response_model=DestinationResponse)
async def get_destination(
    destination_id: str,
    current_user: TokenPayload = Depends(get_current_user),
    service: DestinationService = Depends(get_destination_service)
):
    """Récupérer une destination par ID (authentifié requis)"""
    try:
        destination = await service.get_destination(destination_id)
        if not destination:
            raise HTTPException(status_code=404, detail="Destination non trouvée")
        return destination
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/", response_model=List[DestinationResponse])
async def get_all_destinations(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: TokenPayload = Depends(get_current_user),
    service: DestinationService = Depends(get_destination_service)
):
    """Récupérer les destinations publiées (authentifié requis)"""
    try:
        return await service.get_all_destinations(skip=skip, limit=limit)
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/region/{region}", response_model=List[DestinationResponse])
async def get_destinations_by_region(
    region: str,
    current_user: TokenPayload = Depends(get_current_user),
    service: DestinationService = Depends(get_destination_service)
):
    """Récupérer les destinations par région (authentifié requis)"""
    try:
        return await service.get_destinations_by_region(region)
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/type/{type_destination}", response_model=List[DestinationResponse])
async def get_destinations_by_type(
    type_destination: str,
    current_user: TokenPayload = Depends(get_current_user),
    service: DestinationService = Depends(get_destination_service)
):
    """Récupérer les destinations par type (authentifié requis)"""
    try:
        return await service.get_destinations_by_type(type_destination)
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/top-rated/", response_model=List[DestinationResponse])
async def get_top_rated_destinations(
    limit: int = Query(5, ge=1, le=20),
    current_user: TokenPayload = Depends(get_current_user),
    service: DestinationService = Depends(get_destination_service)
):
    """Récupérer les destinations les mieux notées (authentifié requis)"""
    try:
        return await service.get_top_rated_destinations(limit=limit)
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.put("/{destination_id}", response_model=dict)
async def update_destination(
    destination_id: str,
    destination_update: DestinationUpdate,
    admin: TokenPayload = Depends(require_admin),
    service: DestinationService = Depends(get_destination_service)
):
    """Mettre à jour une destination (ADMIN ONLY)"""
    try:
        success = await service.update_destination(destination_id, destination_update)
        if not success:
            raise HTTPException(status_code=404, detail="Destination non trouvée ou aucune mise à jour")
        return {"message": "Destination mise à jour avec succès"}
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.delete("/{destination_id}", response_model=dict)
async def delete_destination(
    destination_id: str,
    admin: TokenPayload = Depends(require_admin),
    service: DestinationService = Depends(get_destination_service)
):
    """Supprimer une destination (ADMIN ONLY)"""
    try:
        success = await service.delete_destination(destination_id)
        if not success:
            raise HTTPException(status_code=404, detail="Destination non trouvée")
        return {"message": "Destination supprimée avec succès"}
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


# ============ ADMIN GLOBAL VIEWS ============

@router.get("/admin/all", response_model=List[DestinationResponse])
async def admin_get_all_destinations(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    admin: TokenPayload = Depends(require_admin)
):
    """Vue globale de toutes les destinations pour l'admin"""
    try:
        from app.core.database import get_database
        db = get_database()
        destinations = []
        
        cursor = db["destinations"].find().skip(skip).limit(limit)
        async for dest in cursor:
            dest["_id"] = str(dest["_id"])
            destinations.append(dest)
        
        return destinations
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/admin/stats", response_model=dict)
async def admin_get_destinations_stats(admin: TokenPayload = Depends(require_admin)):
    """Statistiques sur les destinations pour l'admin"""
    try:
        from app.core.database import get_database
        db = get_database()
        
        total = await db["destinations"].count_documents({})
        regions = await db["destinations"].distinct("region")
        types = await db["destinations"].distinct("type_destination")
        
        return {
            "total_destinations": total,
            "regions": regions,
            "types": types,
            "regions_count": len(regions),
            "types_count": len(types)
        }
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")
