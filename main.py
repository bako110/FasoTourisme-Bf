from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import connect_to_mongo, close_mongo_connection
from app.api.v1.routes import (
    auth, destinations, hotels, activities, guides, providers,
    bookings, reviews, events, artisans, cuisines, stories,
    health, security, emergency, roads, services,
    health_advisory, tourist_info, support
)
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Création de l'application FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API pour valoriser le tourisme local au Burkina Faso - Ultra complète avec sécurité et santé",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Événements de cycle de vie
@app.on_event("startup")
async def startup_event():
    """Exécuté au démarrage de l'application"""
    logger.info("Démarrage de l'application...")
    await connect_to_mongo()
    logger.info("Connexion à MongoDB établie")


@app.on_event("shutdown")
async def shutdown_event():
    """Exécuté à l'arrêt de l'application"""
    logger.info("Arrêt de l'application...")
    await close_mongo_connection()
    logger.info("Connexion à MongoDB maintenant fermée")


# Routes de santé
@app.get("/health", tags=["Health"])
async def health_check():
    """Vérifier l'état de l'application"""
    return {"status": "ok", "app": settings.APP_NAME, "version": settings.APP_VERSION}


# ============================================
# ROUTES AUTHENTIFICATION (TOUJOURS EN PREMIER)
# ============================================
app.include_router(auth.router, prefix=settings.API_V1_PREFIX)

# ============================================
# ROUTES CORE TOURISM (Destinations, Hotels, Activities, Guides, Providers)
# ============================================
app.include_router(destinations.router, prefix=settings.API_V1_PREFIX)
app.include_router(hotels.router, prefix=settings.API_V1_PREFIX)
app.include_router(activities.router, prefix=settings.API_V1_PREFIX)
app.include_router(guides.router, prefix=settings.API_V1_PREFIX)
app.include_router(providers.router, prefix=settings.API_V1_PREFIX)

# ============================================
# ROUTES BUSINESS & LOCAL (Bookings, Reviews, Events, Artisans, Cuisines, Stories)
# ============================================
app.include_router(bookings.router, prefix=settings.API_V1_PREFIX)
app.include_router(reviews.router, prefix=settings.API_V1_PREFIX)
app.include_router(events.router, prefix=settings.API_V1_PREFIX)
app.include_router(artisans.router, prefix=settings.API_V1_PREFIX)
app.include_router(cuisines.router, prefix=settings.API_V1_PREFIX)
app.include_router(stories.router, prefix=settings.API_V1_PREFIX)

# ============================================
# ROUTES CRITICAL INFRASTRUCTURE (Health, Security, Emergency, Roads, Services)
# PRIORITY 1: SANTÉ & SÉCURITÉ (Most sensitive areas)
# ============================================
app.include_router(health.router, prefix=settings.API_V1_PREFIX)
app.include_router(security.router, prefix=settings.API_V1_PREFIX)
app.include_router(emergency.router, prefix=settings.API_V1_PREFIX)
app.include_router(roads.router, prefix=settings.API_V1_PREFIX)
app.include_router(services.router, prefix=settings.API_V1_PREFIX)
app.include_router(health_advisory.router, prefix=settings.API_V1_PREFIX)
app.include_router(tourist_info.router, prefix=settings.API_V1_PREFIX)

# ============================================
# ROUTES SUPPORT & CONTACT (Bien visible et sécurisé)
# ============================================
app.include_router(support.router, prefix=settings.API_V1_PREFIX)


# Route racine
@app.get("/", tags=["Root"])
async def root():
    """Route racine - Information sur l'API"""
    return {
        "message": f"Bienvenue dans {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "description": "API complète pour tourisme Burkina Faso",
        "documentation": "/api/docs",
        "structure": {
            "core_tourism": {
                "destinations": f"{settings.API_V1_PREFIX}/destinations",
                "hotels": f"{settings.API_V1_PREFIX}/hotels",
                "activities": f"{settings.API_V1_PREFIX}/activities",
                "guides": f"{settings.API_V1_PREFIX}/guides",
            },
            "business_local": {
                "bookings": f"{settings.API_V1_PREFIX}/bookings",
                "reviews": f"{settings.API_V1_PREFIX}/reviews",
                "events": f"{settings.API_V1_PREFIX}/events",
                "artisans": f"{settings.API_V1_PREFIX}/artisans",
                "cuisines": f"{settings.API_V1_PREFIX}/cuisines",
                "stories": f"{settings.API_V1_PREFIX}/stories",
            },
            "critical_infrastructure": {
                "health_facilities": f"{settings.API_V1_PREFIX}/health-facilities",
                "security_alerts": f"{settings.API_V1_PREFIX}/security-alerts",
                "emergency_services": f"{settings.API_V1_PREFIX}/emergency-services",
                "roads": f"{settings.API_V1_PREFIX}/roads",
                "essential_services": f"{settings.API_V1_PREFIX}/essential-services",
                "health_advisories": f"{settings.API_V1_PREFIX}/health-advisories",
                "tourist_info": f"{settings.API_V1_PREFIX}/tourist-info",
            },
            "support_contact": {
                "support_info": f"{settings.API_V1_PREFIX}/support",
                "contact_form": f"{settings.API_V1_PREFIX}/support/contact",
                "status": f"{settings.API_V1_PREFIX}/support/status",
                "faq": f"{settings.API_V1_PREFIX}/support/faq",
                "documentation": f"{settings.API_V1_PREFIX}/support/documentation",
                "emergency": f"{settings.API_V1_PREFIX}/support/emergency",
            }
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
