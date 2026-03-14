from fastapi import APIRouter, HTTPException, Query, Depends, status
from typing import List
from app.core.security import get_current_user, require_admin
from app.core.permissions import Permission, OwnershipCheck, AdminView
from app.schemas.auth import TokenPayload
from app.models.user import UserRole
from app.schemas.review import ReviewCreate, ReviewUpdate, ReviewResponse
from app.services.review_service import ReviewService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/reviews", tags=["Reviews"])
review_service = ReviewService()


@router.post("/", response_model=dict, status_code=201)
async def create_review(
    review: ReviewCreate,
    current_user: TokenPayload = Depends(get_current_user)
):
    """Créer un avis/évaluation (TOURIST ONLY)"""
    try:
        Permission.check_tourist(current_user)
        review_id = await review_service.create_review(review, current_user.sub)
        return {"id": review_id, "message": "Avis créé avec succès"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/", response_model=List[ReviewResponse])
async def list_reviews(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: TokenPayload = Depends(get_current_user)
):
    """Récupérer les avis publiés (authentifié requis)"""
    try:
        return await review_service.get_all_reviews(skip, limit)
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/resource/{resource_id}", response_model=List[ReviewResponse])
async def get_by_resource(
    resource_id: str,
    current_user: TokenPayload = Depends(get_current_user)
):
    """Récupérer les avis d'une ressource (authentifié requis)"""
    try:
        return await review_service.get_reviews_by_resource(resource_id)
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/top-rated", response_model=List[ReviewResponse])
async def get_top_rated(
    limit: int = Query(10, ge=1, le=50),
    current_user: TokenPayload = Depends(get_current_user)
):
    """Récupérer les meilleurs avis (authentifié requis)"""
    try:
        return await review_service.get_top_reviews(limit)
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/average/{resource_id}", response_model=dict)
async def get_average(
    resource_id: str,
    current_user: TokenPayload = Depends(get_current_user)
):
    """Récupérer la note moyenne d'une ressource (authentifié requis)"""
    try:
        avg = await review_service.get_average_rating(resource_id)
        if avg is None:
            raise HTTPException(status_code=404, detail="Aucun avis pour cette ressource")
        return {"resource_id": resource_id, "average_rating": avg}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/{review_id}", response_model=ReviewResponse)
async def get_one(
    review_id: str,
    current_user: TokenPayload = Depends(get_current_user)
):
    """Récupérer un avis (authentifié requis)"""
    try:
        review = await review_service.get_review(review_id)
        if not review:
            raise HTTPException(status_code=404, detail="Avis non trouvé")
        return review
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.put("/{review_id}")
async def update_one(
    review_id: str,
    review: ReviewUpdate,
    current_user: TokenPayload = Depends(get_current_user)
):
    """Mettre à jour un avis (propriétaire, MODERATOR ou ADMIN)"""
    try:
        existing = await review_service.get_review(review_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Avis non trouvé")
        
        # Vérifier les permissions
        if current_user.role not in [UserRole.MODERATOR, UserRole.ADMIN]:
            if existing.get("author_id") != current_user.sub:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Vous ne pouvez modifier que vos propres avis"
                )
        
        success = await review_service.update_review(review_id, review)
        if not success:
            raise HTTPException(status_code=404, detail="Avis non trouvé")
        return {"message": "Avis mis à jour"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.post("/{review_id}/helpful")
async def mark_helpful(
    review_id: str,
    current_user: TokenPayload = Depends(get_current_user)
):
    """Marquer un avis comme utile (authentifié requis)"""
    try:
        success = await review_service.mark_helpful(review_id)
        if not success:
            raise HTTPException(status_code=404, detail="Avis non trouvé")
        return {"message": "Avis marqué comme utile"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.delete("/{review_id}")
async def delete_one(
    review_id: str,
    current_user: TokenPayload = Depends(get_current_user)
):
    """Supprimer un avis (propriétaire, MODERATOR ou ADMIN)"""
    try:
        existing = await review_service.get_review(review_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Avis non trouvé")
        
        # Vérifier les permissions
        if current_user.role not in [UserRole.MODERATOR, UserRole.ADMIN]:
            if existing.get("author_id") != current_user.sub:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Vous ne pouvez supprimer que vos propres avis"
                )
        
        success = await review_service.delete_review(review_id)
        if not success:
            raise HTTPException(status_code=404, detail="Avis non trouvé")
        return {"message": "Avis supprimé"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


# ============ ADMIN & MODERATOR VIEWS ============

@router.get("/admin/all", response_model=List[ReviewResponse])
async def admin_get_all_reviews(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    admin: TokenPayload = Depends(require_admin)
):
    """Vue globale de tous les avis pour l'admin"""
    try:
        from app.core.database import get_database
        db = get_database()
        reviews = []
        
        cursor = db["reviews"].find().skip(skip).limit(limit)
        async for rev in cursor:
            rev["_id"] = str(rev["_id"])
            reviews.append(rev)
        
        return reviews
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.post("/admin/{review_id}/flag")
async def flag_review_inappropriate(
    review_id: str,
    reason: str,
    admin: TokenPayload = Depends(require_admin)
):
    """Signaler un avis comme inapproprié (ADMIN)"""
    try:
        success = await review_service.flag_review(review_id, reason)
        if not success:
            raise HTTPException(status_code=404, detail="Avis non trouvé")
        return {"message": "Avis signalé comme inapproprié"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/admin/stats", response_model=dict)
async def admin_get_reviews_stats(admin: TokenPayload = Depends(require_admin)):
    """Statistiques sur les avis pour l'admin"""
    try:
        from app.core.database import get_database
        db = get_database()
        
        total = await db["reviews"].count_documents({})
        flagged = await db["reviews"].count_documents({"flagged": True})
        avg_rating = await db["reviews"].aggregate([
            {"$group": {"_id": None, "avg_note": {"$avg": "$note"}}}
        ]).to_list(1)
        
        return {
            "total_reviews": total,
            "flagged_reviews": flagged,
            "average_rating": avg_rating[0].get("avg_note", 0) if avg_rating else 0
        }
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")
