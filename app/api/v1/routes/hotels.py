from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List
from app.core.database import get_database
from app.core.security import get_current_user, require_admin
from app.core.permissions import Permission, OwnershipCheck
from app.schemas.auth import TokenPayload
from app.models.user import UserRole
from app.services.hotel_service import HotelService
from app.schemas.hotel import HotelCreate, HotelUpdate, HotelResponse
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/hotels",
    tags=["Hôtels"],
    responses={404: {"description": "Not found"}},
)


def get_hotel_service():
    """Dépendance pour obtenir le service des hôtels"""
    return HotelService(get_database())


@router.post("/", response_model=dict, status_code=201)
async def create_hotel(
    hotel: HotelCreate,
    current_user: TokenPayload = Depends(get_current_user),
    service: HotelService = Depends(get_hotel_service)
):
    """Créer un nouvel hôtel (PROVIDER ou ADMIN)"""
    try:
        # Seuls les PROVIDERS et ADMIN peuvent créer des hôtels
        if current_user.role not in [UserRole.PROVIDER, UserRole.ADMIN]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Seuls les providers peuvent créer des hôtels"
            )
        
        hotel_id = await service.create_hotel(hotel, current_user.sub)
        return {"id": hotel_id, "message": "Hôtel créé avec succès"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/{hotel_id}", response_model=HotelResponse)
async def get_hotel(
    hotel_id: str,
    current_user: TokenPayload = Depends(get_current_user),
    service: HotelService = Depends(get_hotel_service)
):
    """Récupérer un hôtel par ID (authentifié requis)"""
    try:
        hotel = await service.get_hotel(hotel_id)
        if not hotel:
            raise HTTPException(status_code=404, detail="Hôtel non trouvé")
        return hotel
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/", response_model=List[HotelResponse])
async def get_all_hotels(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: TokenPayload = Depends(get_current_user),
    service: HotelService = Depends(get_hotel_service)
):
    """Récupérer tous les hôtels publiés (authentifié requis)"""
    try:
        return await service.get_all_hotels(skip=skip, limit=limit)
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/city/{ville}", response_model=List[HotelResponse])
async def get_hotels_by_city(
    ville: str,
    service: HotelService = Depends(get_hotel_service)
):
    """Récupérer les hôtels par ville"""
    return await service.get_hotels_by_city(ville)


@router.get("/category/{categorie}", response_model=List[HotelResponse])
async def get_hotels_by_category(
    categorie: str,
    service: HotelService = Depends(get_hotel_service)
):
    """Récupérer les hôtels par catégorie"""
    return await service.get_hotels_by_category(categorie)


@router.get("/price-range/", response_model=List[HotelResponse])
async def get_hotels_by_price_range(
    min_price: float = Query(..., ge=0),
    max_price: float = Query(..., ge=0),
    service: HotelService = Depends(get_hotel_service)
):
    """Récupérer les hôtels par gamme de prix"""
    if min_price > max_price:
        raise HTTPException(status_code=400, detail="min_price doit être inférieur ou égal à max_price")
    return await service.get_hotels_by_price_range(min_price, max_price)


@router.get("/top-rated/", response_model=List[HotelResponse])
async def get_top_rated_hotels(
    limit: int = Query(5, ge=1, le=20),
    service: HotelService = Depends(get_hotel_service)
):
    """Récupérer les hôtels les mieux notés"""
    return await service.get_top_rated_hotels(limit=limit)


@router.put("/{hotel_id}", response_model=dict)
async def update_hotel(
    hotel_id: str,
    hotel_update: HotelUpdate,
    current_user: TokenPayload = Depends(get_current_user),
    service: HotelService = Depends(get_hotel_service)
):
    """Mettre à jour un hôtel (propriétaire ou ADMIN)"""
    try:
        hotel = await service.get_hotel(hotel_id)
        if not hotel:
            raise HTTPException(status_code=404, detail="Hôtel non trouvé")
        
        # Vérifier la propriété
        if current_user.role != UserRole.ADMIN:
            if hotel.get("owner_id") != current_user.sub:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Vous ne pouvez modifier que vos propres hôtels"
                )
        
        success = await service.update_hotel(hotel_id, hotel_update)
        if not success:
            raise HTTPException(status_code=404, detail="Hôtel non trouvé ou aucune mise à jour")
        return {"message": "Hôtel mis à jour avec succès"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.delete("/{hotel_id}", response_model=dict)
async def delete_hotel(
    hotel_id: str,
    current_user: TokenPayload = Depends(get_current_user),
    service: HotelService = Depends(get_hotel_service)
):
    """Supprimer un hôtel (propriétaire ou ADMIN)"""
    try:
        hotel = await service.get_hotel(hotel_id)
        if not hotel:
            raise HTTPException(status_code=404, detail="Hôtel non trouvé")
        
        # Vérifier la propriété
        if current_user.role != UserRole.ADMIN:
            if hotel.get("owner_id") != current_user.sub:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Vous ne pouvez supprimer que vos propres hôtels"
                )
        
        success = await service.delete_hotel(hotel_id)
        if not success:
            raise HTTPException(status_code=404, detail="Hôtel non trouvé")
        return {"message": "Hôtel supprimé avec succès"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


# ============ ROUTES POUR PROVIDERS (Mes Hôtels) ============

@router.get("/me/hotels", response_model=List[HotelResponse])
async def get_my_hotels(
    current_user: TokenPayload = Depends(get_current_user)
):
    """Récupérer mes hôtels (PROVIDER)"""
    try:
        if current_user.role not in [UserRole.PROVIDER, UserRole.ADMIN]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès réservé aux providers"
            )
        
        from app.core.database import get_database
        db = get_database()
        hotels = []
        
        cursor = db["hotels"].find({"owner_id": current_user.sub})
        async for hotel in cursor:
            hotel["_id"] = str(hotel["_id"])
            hotels.append(hotel)
        
        return hotels
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


# ============ ADMIN GLOBAL VIEWS ============

@router.get("/admin/all", response_model=List[HotelResponse])
async def admin_get_all_hotels(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    admin: TokenPayload = Depends(require_admin)
):
    """Vue globale de tous les hôtels pour l'admin"""
    try:
        from app.core.database import get_database
        db = get_database()
        hotels = []
        
        cursor = db["hotels"].find().skip(skip).limit(limit)
        async for hotel in cursor:
            hotel["_id"] = str(hotel["_id"])
            hotels.append(hotel)
        
        return hotels
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")
