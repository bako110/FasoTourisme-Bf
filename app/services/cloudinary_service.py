"""
Service pour gérer les uploads d'images vers Cloudinary
"""
import cloudinary
import cloudinary.uploader
from app.core.config import settings
import logging
from typing import Optional, Dict

logger = logging.getLogger(__name__)

# Configuration Cloudinary
cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True
)

class CloudinaryService:
    """Service pour gérer les uploads d'images"""
    
    @staticmethod
    async def upload_image(
        file_content: bytes,
        folder: str = "guides",
        public_id: Optional[str] = None,
        transformation: Optional[Dict] = None
    ) -> Dict:
        """
        Upload une image vers Cloudinary
        
        Args:
            file_content: Contenu du fichier en bytes
            folder: Dossier dans Cloudinary (ex: 'guides', 'destinations')
            public_id: ID public optionnel pour l'image
            transformation: Transformations à appliquer (resize, crop, etc.)
            
        Returns:
            Dict avec url, secure_url, public_id, etc.
        """
        try:
            upload_options = {
                "folder": folder,
                "resource_type": "image",
                "overwrite": True,
            }
            
            if public_id:
                upload_options["public_id"] = public_id
            
            if transformation:
                upload_options["transformation"] = transformation
            else:
                # Transformation par défaut pour les photos de profil
                upload_options["transformation"] = [
                    {"width": 500, "height": 500, "crop": "fill", "gravity": "face"},
                    {"quality": "auto"},
                    {"fetch_format": "auto"}
                ]
            
            result = cloudinary.uploader.upload(
                file_content,
                **upload_options
            )
            
            logger.info(f"Image uploaded successfully: {result.get('secure_url')}")
            return {
                "url": result.get("url"),
                "secure_url": result.get("secure_url"),
                "public_id": result.get("public_id"),
                "width": result.get("width"),
                "height": result.get("height"),
                "format": result.get("format"),
                "resource_type": result.get("resource_type"),
            }
        except Exception as e:
            logger.error(f"Erreur lors de l'upload Cloudinary: {e}")
            raise Exception(f"Erreur lors de l'upload de l'image: {str(e)}")
    
    @staticmethod
    async def delete_image(public_id: str) -> bool:
        """
        Supprimer une image de Cloudinary
        
        Args:
            public_id: L'ID public de l'image à supprimer
            
        Returns:
            True si suppression réussie
        """
        try:
            result = cloudinary.uploader.destroy(public_id)
            logger.info(f"Image deleted: {public_id}")
            return result.get("result") == "ok"
        except Exception as e:
            logger.error(f"Erreur lors de la suppression Cloudinary: {e}")
            return False
    
    @staticmethod
    def get_optimized_url(
        public_id: str,
        width: int = 500,
        height: int = 500,
        crop: str = "fill"
    ) -> str:
        """
        Générer une URL optimisée pour une image existante
        
        Args:
            public_id: L'ID public de l'image
            width: Largeur souhaitée
            height: Hauteur souhaitée
            crop: Mode de crop ('fill', 'fit', 'scale', etc.)
            
        Returns:
            URL de l'image optimisée
        """
        try:
            url = cloudinary.CloudinaryImage(public_id).build_url(
                width=width,
                height=height,
                crop=crop,
                quality="auto",
                fetch_format="auto"
            )
            return url
        except Exception as e:
            logger.error(f"Erreur génération URL optimisée: {e}")
            return ""

cloudinary_service = CloudinaryService()
