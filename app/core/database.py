from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Variable globale pour la connexion
client: AsyncIOMotorClient = None
db: AsyncIOMotorDatabase = None


async def connect_to_mongo():
    """Connexion à MongoDB"""
    global client, db
    try:
        client = AsyncIOMotorClient(settings.MONGODB_URL)
        db = client[settings.DATABASE_NAME]
        # Test de connexion
        await client.admin.command("ping")
        logger.info("Connecté à MongoDB avec succès")
    except Exception as e:
        logger.error(f"Erreur de connexion à MongoDB: {e}")
        raise


async def close_mongo_connection():
    """Fermeture de la connexion MongoDB"""
    global client
    if client:
        client.close()
        logger.info("Connexion MongoDB fermée")


def get_database() -> AsyncIOMotorDatabase:
    """Retourne l'instance de la base de données"""
    return db
