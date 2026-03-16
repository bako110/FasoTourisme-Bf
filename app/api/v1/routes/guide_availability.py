"""
Routes API pour la gestion de la disponibilité des guides
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from app.schemas.guide_availability import (
    AvailabilitySlotCreate,
    AvailabilitySlotUpdate,
    AvailabilitySlotResponse,
    BulkAvailabilityCreate,
    AvailabilityCheckRequest,
    AvailabilityCheckResponse
)
from app.schemas.auth import TokenPayload
from app.services.guide_availability_service import GuideAvailabilityService
from app.core.security import get_current_user
from app.models.guide_availability import AvailabilityStatus
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


def get_availability_service() -> GuideAvailabilityService:
    """Obtenir une instance du service de disponibilité"""
    return GuideAvailabilityService()


@router.post("/slots", response_model=dict, status_code=201)
async def create_availability_slot(
    slot_data: AvailabilitySlotCreate,
    current_user: TokenPayload = Depends(get_current_user),
    service: GuideAvailabilityService = Depends(get_availability_service)
):
    """Créer une nouvelle plage de disponibilité"""
    try:
        # Seuls les guides peuvent créer leurs disponibilités
        if current_user.role != "guide":
            raise HTTPException(
                status_code=403,
                detail="Seuls les guides peuvent gérer leur disponibilité"
            )
        
        guide_id = current_user.sub
        slot_id = await service.create_availability_slot(guide_id, slot_data)
        
        return {
            "id": slot_id,
            "message": "Plage de disponibilité créée avec succès"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Erreur création disponibilité: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")


@router.post("/slots/bulk", response_model=dict, status_code=201)
async def create_bulk_availability(
    bulk_data: BulkAvailabilityCreate,
    current_user: TokenPayload = Depends(get_current_user),
    service: GuideAvailabilityService = Depends(get_availability_service)
):
    """Créer plusieurs plages de disponibilité en une fois"""
    try:
        if current_user.role != "guide":
            raise HTTPException(
                status_code=403,
                detail="Seuls les guides peuvent gérer leur disponibilité"
            )
        
        guide_id = current_user.sub
        slot_ids = await service.create_bulk_availability(guide_id, bulk_data)
        
        return {
            "created_count": len(slot_ids),
            "slot_ids": slot_ids,
            "message": f"{len(slot_ids)} plages créées avec succès"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Erreur création disponibilités: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")


@router.get("/guides/{guide_id}/slots", response_model=List[AvailabilitySlotResponse])
async def get_guide_availability(
    guide_id: str,
    start_date: Optional[str] = Query(None, description="Date de début (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="Date de fin (YYYY-MM-DD)"),
    status: Optional[AvailabilityStatus] = Query(None, description="Filtrer par statut"),
    service: GuideAvailabilityService = Depends(get_availability_service)
):
    """Récupérer les disponibilités d'un guide (accepte l'_id du guide OU le user_id)"""
    try:
        from app.core.database import get_database
        from bson import ObjectId

        # Les créneaux sont stockés avec guide_id = user_id du guide.
        # Si on reçoit l'_id MongoDB du guide, on résout vers son user_id.
        resolved_id = guide_id
        try:
            db = get_database()
            guide_doc = await db["guides"].find_one({"_id": ObjectId(guide_id)})
            if guide_doc and guide_doc.get("user_id"):
                resolved_id = guide_doc["user_id"]
                logger.info(f"Résolution guide_id {guide_id} → user_id {resolved_id}")
        except Exception:
            pass  # guide_id n'est pas un ObjectId valide → on l'utilise tel quel

        availabilities = await service.get_guide_availability(
            resolved_id,
            start_date,
            end_date,
            status
        )
        return availabilities
    except Exception as e:
        logger.error(f"Erreur récupération disponibilités: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")


@router.get("/my-slots", response_model=List[AvailabilitySlotResponse])
async def get_my_availability(
    start_date: Optional[str] = Query(None, description="Date de début (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="Date de fin (YYYY-MM-DD)"),
    status: Optional[AvailabilityStatus] = Query(None, description="Filtrer par statut"),
    current_user: TokenPayload = Depends(get_current_user),
    service: GuideAvailabilityService = Depends(get_availability_service)
):
    """Récupérer mes disponibilités (guide connecté)"""
    try:
        if current_user.role != "guide":
            raise HTTPException(
                status_code=403,
                detail="Seuls les guides peuvent accéder à cette ressource"
            )
        
        guide_id = current_user.sub
        availabilities = await service.get_guide_availability(
            guide_id,
            start_date,
            end_date,
            status
        )
        return availabilities
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur récupération disponibilités: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")


@router.put("/slots/{slot_id}", response_model=dict)
async def update_availability_slot(
    slot_id: str,
    update_data: AvailabilitySlotUpdate,
    current_user: TokenPayload = Depends(get_current_user),
    service: GuideAvailabilityService = Depends(get_availability_service)
):
    """Mettre à jour une plage de disponibilité"""
    try:
        if current_user.role != "guide":
            raise HTTPException(
                status_code=403,
                detail="Seuls les guides peuvent gérer leur disponibilité"
            )
        
        guide_id = current_user.sub
        success = await service.update_availability_slot(slot_id, guide_id, update_data)
        
        if not success:
            raise HTTPException(
                status_code=404,
                detail="Plage de disponibilité non trouvée"
            )
        
        return {"message": "Plage de disponibilité mise à jour avec succès"}
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Erreur mise à jour disponibilité: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")


@router.delete("/slots/{slot_id}", response_model=dict)
async def delete_availability_slot(
    slot_id: str,
    current_user: TokenPayload = Depends(get_current_user),
    service: GuideAvailabilityService = Depends(get_availability_service)
):
    """Supprimer une plage de disponibilité"""
    try:
        if current_user.role != "guide":
            raise HTTPException(
                status_code=403,
                detail="Seuls les guides peuvent gérer leur disponibilité"
            )
        
        guide_id = current_user.sub
        success = await service.delete_availability_slot(slot_id, guide_id)
        
        if not success:
            raise HTTPException(
                status_code=404,
                detail="Plage de disponibilité non trouvée"
            )
        
        return {"message": "Plage de disponibilité supprimée avec succès"}
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Erreur suppression disponibilité: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")


@router.post("/check", response_model=AvailabilityCheckResponse)
async def check_availability(
    check_request: AvailabilityCheckRequest,
    service: GuideAvailabilityService = Depends(get_availability_service)
):
    """Vérifier si un guide est disponible pour une période donnée"""
    try:
        result = await service.check_availability(check_request)
        return result
    except Exception as e:
        logger.error(f"Erreur vérification disponibilité: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")
