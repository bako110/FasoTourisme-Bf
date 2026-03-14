from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List
from app.models.provider import ProviderCreate, ProviderUpdate, ProviderResponse, ProviderType
from app.services.provider_service import ProviderService
from app.schemas.auth import TokenPayload
from app.core.security import get_current_user, require_admin
from app.models.user import UserRole
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/providers", tags=["Providers"])
provider_service = ProviderService()


# ============ ROUTES PUBLIQUES (Lecture) ============

@router.get("/", response_model=List[ProviderResponse])
async def list_providers(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    type_service: str = Query(None)
):
    """Lister les providers vérifiés et publiés"""
    try:
        if type_service:
            return await provider_service.get_providers_by_type(
                ProviderType(type_service), skip, limit
            )
        return await provider_service.get_all_providers(skip, limit)
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/search", response_model=List[ProviderResponse])
async def search_providers(
    q: str = Query(..., min_length=2),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100)
):
    """Rechercher des providers"""
    try:
        return await provider_service.search_providers(q, skip, limit)
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/hotels", response_model=List[ProviderResponse])
async def list_hotels(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100)
):
    """Lister tous les hôtels"""
    try:
        return await provider_service.get_providers_by_type(ProviderType.HOTEL, skip, limit)
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/restaurants", response_model=List[ProviderResponse])
async def list_restaurants(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100)
):
    """Lister tous les restaurants"""
    try:
        return await provider_service.get_providers_by_type(ProviderType.RESTAURANT, skip, limit)
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/artisans", response_model=List[ProviderResponse])
async def list_artisans(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100)
):
    """Lister tous les artisans"""
    try:
        return await provider_service.get_providers_by_type(ProviderType.ARTISAN, skip, limit)
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/restaurants", response_model=List[ProviderResponse])
async def list_restaurants(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100)
):
    """Lister tous les restaurants"""
    try:
        return await provider_service.get_providers_by_type(ProviderType.RESTAURANT, skip, limit)
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/transport", response_model=List[ProviderResponse])
async def list_transport(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100)
):
    """Lister tous les services de transport"""
    try:
        return await provider_service.get_providers_by_type(ProviderType.TRANSPORT, skip, limit)
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/pharmacies", response_model=List[ProviderResponse])
async def list_pharmacies(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100)
):
    """Lister toutes les pharmacies"""
    try:
        return await provider_service.get_providers_by_type(ProviderType.PHARMACIE, skip, limit)
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/agences", response_model=List[ProviderResponse])
async def list_agences(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100)
):
    """Lister toutes les agences de voyage"""
    try:
        return await provider_service.get_providers_by_type(ProviderType.AGENCE, skip, limit)
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/locations", response_model=List[ProviderResponse])
async def list_locations(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100)
):
    """Lister tous les services de location"""
    try:
        return await provider_service.get_providers_by_type(ProviderType.LOCATION, skip, limit)
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/commerces", response_model=List[ProviderResponse])
async def list_commerces(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100)
):
    """Lister tous les commerces"""
    try:
        return await provider_service.get_providers_by_type(ProviderType.COMMERCE, skip, limit)
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/services", response_model=List[ProviderResponse])
async def list_services_providers(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100)
):
    """Lister tous les prestataires de services divers"""
    try:
        return await provider_service.get_providers_by_type(ProviderType.SERVICE, skip, limit)
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/{provider_id}", response_model=ProviderResponse)
async def get_provider_detail(provider_id: str):
    """Récupérer les détails d'un provider"""
    try:
        provider = await provider_service.get_provider(provider_id)
        if not provider:
            raise HTTPException(status_code=404, detail="Provider non trouvé")
        return provider
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


# ============ ROUTES PROTÉGÉES (PROVIDER) ============

@router.post("/", response_model=dict, status_code=201)
async def create_provider(
    provider_data: ProviderCreate,
    current_user: TokenPayload = Depends(get_current_user)
):
    """Créer un nouveau provider (PROVIDER ou ADMIN ONLY)"""
    try:
        if current_user.role not in [UserRole.PROVIDER, UserRole.ADMIN]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Seuls les providers peuvent créer un profil"
            )
        
        provider_id = await provider_service.create_provider(
            provider_data,
            current_user.sub,
            current_user.email
        )
        
        return {
            "id": provider_id,
            "message": "Provider créé avec succès",
            "status": "pending_verification"
        }
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/me/providers")
async def get_my_providers(current_user: TokenPayload = Depends(get_current_user)):
    """Récupérer mes providers personnels"""
    try:
        if current_user.role not in [UserRole.PROVIDER, UserRole.ADMIN]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès refusé"
            )
        
        return await provider_service.get_providers_by_owner(current_user.sub)
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.put("/{provider_id}")
async def update_provider(
    provider_id: str,
    update_data: ProviderUpdate,
    current_user: TokenPayload = Depends(get_current_user)
):
    """Mettre à jour un provider"""
    try:
        # Vérifier que c'est le propriétaire ou admin
        provider = await provider_service.get_provider(provider_id)
        if not provider:
            raise HTTPException(status_code=404, detail="Provider non trouvé")
        
        if provider["owner_id"] != current_user.sub and current_user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Vous ne pouvez modifier que vos propres profiles"
            )
        
        success = await provider_service.update_provider(provider_id, update_data)
        
        if not success:
            raise HTTPException(status_code=404, detail="Provider non trouvé")
        
        return {"message": "Provider mis à jour"}
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.delete("/{provider_id}")
async def delete_provider(
    provider_id: str,
    current_user: TokenPayload = Depends(get_current_user)
):
    """Supprimer un provider"""
    try:
        provider = await provider_service.get_provider(provider_id)
        if not provider:
            raise HTTPException(status_code=404, detail="Provider non trouvé")
        
        if provider["owner_id"] != current_user.sub and current_user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Vous ne pouvez supprimer que vos propres profiles"
            )
        
        success = await provider_service.delete_provider(provider_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Provider non trouvé")
        
        return {"message": "Provider supprimé"}
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


# ============ ROUTES PROTÉGÉES (ADMIN) ============

@router.put("/admin/{provider_id}/verify")
async def verify_provider(
    provider_id: str,
    verified: bool,
    admin: TokenPayload = Depends(require_admin)
):
    """Vérifier/Refuser un provider (ADMIN ONLY)"""
    try:
        success = await provider_service.verify_provider(provider_id, verified)
        
        if not success:
            raise HTTPException(status_code=404, detail="Provider non trouvé")
        
        status_text = "vérifié" if verified else "refusé"
        return {"message": f"Provider {status_text}"}
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.put("/admin/{provider_id}/publish")
async def publish_provider(
    provider_id: str,
    published: bool,
    admin: TokenPayload = Depends(require_admin)
):
    """Publier/Dépublier un provider (ADMIN ONLY)"""
    try:
        success = await provider_service.publish_provider(provider_id, published)
        
        if not success:
            raise HTTPException(status_code=404, detail="Provider non trouvé")
        
        status_text = "publié" if published else "dépublié"
        return {"message": f"Provider {status_text}"}
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")


@router.get("/admin/pending")
async def get_pending_providers(admin: TokenPayload = Depends(require_admin)):
    """Récupérer les providers en attente de vérification (ADMIN ONLY)"""
    try:
        from app.core.database import get_database
        db = get_database()
        providers = []
        async for provider in db["providers"].find({"verified": False}):
            providers.append({
                "id": str(provider["_id"]),
                "nom_entreprise": provider["nom_entreprise"],
                "type_service": provider["type_service"],
                "owner_email": provider["owner_email"],
                "date_creation": provider["date_creation"]
            })
        return providers
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail="Erreur serveur")
