from fastapi import APIRouter, HTTPException, Query, Depends, status
from typing import List, Optional
from app.core.security import get_current_user, require_admin
from app.core.permissions import Permission, OwnershipCheck
from app.schemas.auth import TokenPayload
from app.models.user import UserRole
from app.schemas.booking import BookingCreate, BookingUpdate, BookingResponse
from app.services.booking_service import BookingService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/bookings", tags=["Bookings"])
booking_service = BookingService()


@router.post("/", response_model=dict, status_code=201)
async def create_booking(
    booking: BookingCreate,
    current_user: TokenPayload = Depends(get_current_user)
):
    """Créer une réservation (TOURIST ONLY)"""
    try:
        Permission.check_tourist(current_user)
        booking_id = await booking_service.create_booking(booking, current_user.sub)
        return {"id": booking_id, "message": "Réservation créée avec succès"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/", response_model=List[BookingResponse])
async def list_bookings(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: TokenPayload = Depends(get_current_user)
):
    """Récupérer ses propres réservations (ou toutes pour ADMIN)"""
    try:
        if current_user.role == UserRole.ADMIN:
            return await booking_service.get_all_bookings(skip, limit)
        else:
            # Utilisateurs normaux ne voient que leurs réservations
            return await booking_service.get_bookings_by_client(current_user.sub, skip, limit)
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/status/{statut}", response_model=List[BookingResponse])
async def get_by_status(
    statut: str,
    current_user: TokenPayload = Depends(get_current_user)
):
    """Récupérer les réservations par statut (ADMIN ou ses propres réservations)"""
    try:
        if current_user.role == UserRole.ADMIN:
            return await booking_service.get_bookings_by_status(statut)
        else:
            # Filtrer par client et statut
            all_bookings = await booking_service.get_bookings_by_client(current_user.sub)
            return [b for b in all_bookings if b.get("statut_paiement") == statut]
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/high-value", response_model=List[BookingResponse])
async def get_high_value(
    min_amount: float = Query(100000),
    admin: TokenPayload = Depends(require_admin)
):
    """Récupérer les réservations de haute valeur (ADMIN ONLY)"""
    try:
        return await booking_service.get_high_value_bookings(min_amount)
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/me", response_model=List[BookingResponse])
@router.get("/client/me", response_model=List[BookingResponse])
async def get_my_bookings(
    current_user: TokenPayload = Depends(get_current_user)
):
    """Récupérer les réservations de l'utilisateur connecté"""
    try:
        return await booking_service.get_bookings_by_client(current_user.sub)
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/guide/me", response_model=List[BookingResponse])
async def get_my_guide_bookings(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    current_user: TokenPayload = Depends(get_current_user)
):
    """Récupérer les réservations liées au guide connecté"""
    try:
        Permission.check_guide(current_user)
        return await booking_service.get_bookings_by_guide(current_user.sub, skip, limit)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/client/{client_id}", response_model=List[BookingResponse])
async def get_by_client(
    client_id: str,
    current_user: TokenPayload = Depends(get_current_user)
):
    """Récupérer les réservations d'un client (propriétaire ou ADMIN)"""
    try:
        if current_user.role != UserRole.ADMIN and current_user.sub != client_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Vous ne pouvez voir que vos propres réservations"
            )
        return await booking_service.get_bookings_by_client(client_id)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/analytics", response_model=dict)
async def get_revenue(
    start_date: str = Query(..., description="YYYY-MM-DD"),
    end_date: str = Query(..., description="YYYY-MM-DD"),
    admin: TokenPayload = Depends(require_admin)
):
    """Calculer le revenu sur une période (ADMIN ONLY)"""
    from datetime import datetime
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        return await booking_service.get_revenue_by_date_range(start, end)
    except ValueError:
        raise HTTPException(status_code=400, detail="Format de date invalide")
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/{booking_id}", response_model=BookingResponse)
async def get_one(
    booking_id: str,
    current_user: TokenPayload = Depends(get_current_user)
):
    """Récupérer une réservation (propriétaire ou ADMIN)"""
    try:
        booking = await booking_service.get_booking(booking_id)
        if not booking:
            raise HTTPException(status_code=404, detail="Réservation non trouvée")
        
        # Vérifier que c'est le propriétaire ou un admin
        if current_user.role != UserRole.ADMIN and booking.get("client_id") != current_user.sub:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Vous ne pouvez voir que vos propres réservations"
            )
        
        return booking
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.put("/{booking_id}")
async def update_one(
    booking_id: str,
    booking: BookingUpdate,
    current_user: TokenPayload = Depends(get_current_user)
):
    """Mettre à jour une réservation (propriétaire ou ADMIN)"""
    try:
        existing = await booking_service.get_booking(booking_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Réservation non trouvée")
        
        # Vérifier les permissions
        if current_user.role != UserRole.ADMIN:
            if existing.get("client_id") != current_user.sub:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Vous ne pouvez modifier que vos propres réservations"
                )
        
        success = await booking_service.update_booking(booking_id, booking)
        if not success:
            raise HTTPException(status_code=404, detail="Réservation non trouvée")
        return {"message": "Réservation mise à jour"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.post("/{booking_id}/cancel")
@router.put("/{booking_id}/cancel")
async def cancel(
    booking_id: str,
    raison: Optional[str] = Query(None),
    current_user: TokenPayload = Depends(get_current_user)
):
    """Annuler une réservation (propriétaire ou ADMIN)"""
    try:
        existing = await booking_service.get_booking(booking_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Réservation non trouvée")
        
        # Vérifier les permissions
        if current_user.role != UserRole.ADMIN:
            if existing.get("client_id") != current_user.sub:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Vous ne pouvez annuler que vos propres réservations"
                )
        
        success = await booking_service.cancel_booking(booking_id, raison)
        if not success:
            raise HTTPException(status_code=404, detail="Réservation non trouvée")
        return {"message": "Réservation annulée"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


# ============ ADMIN GLOBAL VIEWS ============

@router.get("/admin/all", response_model=List[BookingResponse])
async def admin_get_all_bookings(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    admin: TokenPayload = Depends(require_admin)
):
    """Vue globale de toutes les réservations pour l'admin"""
    try:
        from app.core.database import get_database
        db = get_database()
        bookings = []
        
        cursor = db["bookings"].find().skip(skip).limit(limit)
        async for booking in cursor:
            booking["_id"] = str(booking["_id"])
            bookings.append(booking)
        
        return bookings
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/admin/stats", response_model=dict)
async def admin_get_bookings_stats(admin: TokenPayload = Depends(require_admin)):
    """Statistiques sur les réservations pour l'admin"""
    try:
        from app.core.database import get_database
        db = get_database()
        
        total = await db["bookings"].count_documents({})
        confirmed = await db["bookings"].count_documents({"statut_paiement": "confirmed"})
        cancelled = await db["bookings"].count_documents({"statut_paiement": "cancelled"})
        revenue = await db["bookings"].aggregate([
            {"$match": {"statut_paiement": "confirmed"}},
            {"$group": {"_id": None, "total": {"$sum": "$montant_total"}}}
        ]).to_list(1)
        
        return {
            "total_bookings": total,
            "confirmed_bookings": confirmed,
            "cancelled_bookings": cancelled,
            "total_revenue": revenue[0].get("total", 0) if revenue else 0
        }
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.delete("/{booking_id}")
async def delete_one(booking_id: str):
    """Supprimer une réservation"""
    success = await booking_service.delete_booking(booking_id)
    if not success:
        raise HTTPException(status_code=404, detail="Booking not found")
    return {"message": "Booking deleted"}
