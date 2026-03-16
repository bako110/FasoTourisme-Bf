from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime
from app.models.user import UserRole
import re


class TokenRequest(BaseModel):
    """Requête de connexion"""
    login: str = Field(..., min_length=3, description="Email ou numéro de téléphone")
    motdepasse: str = Field(..., min_length=8)
    
    @field_validator('login')
    @classmethod
    def validate_login(cls, v: str) -> str:
        """Valider que le login est un email ou un numéro de téléphone"""
        # Vérifier si c'est un email
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        # Vérifier si c'est un numéro de téléphone (format international ou local)
        phone_pattern = r'^[\+]?[(]?[0-9]{1,4}[)]?[-\s\.]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{1,9}$'
        
        if not (re.match(email_pattern, v) or re.match(phone_pattern, v)):
            raise ValueError('Le login doit être un email valide ou un numéro de téléphone')
        return v


class TokenResponse(BaseModel):
    """Réponse de token JWT"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user_id: str
    email: str
    role: UserRole


class UserRegister(BaseModel):
    """Enregistrement d'un nouvel utilisateur"""
    email: EmailStr
    nom_complet: str = Field(..., min_length=3, max_length=100)
    motdepasse: str = Field(..., min_length=8)
    role: Optional[UserRole] = UserRole.TOURIST  # Rôle par défaut: tourist
    profil_type: Optional[str] = None  # "guide", "artisan", "restaurant"
    telephone: Optional[str] = None
    
    @field_validator('motdepasse')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Valider le mot de passe - minimum 8 caractères"""
        if len(v) < 8:
            raise ValueError('Le mot de passe doit contenir au moins 8 caractères')
        return v


class UserResponse(BaseModel):
    """Réponse utilisateur"""
    id: str
    email: str
    telephone: Optional[str] = None
    photo_url: Optional[str] = None
    nom_complet: str
    role: UserRole
    actif: bool
    verifiee: bool
    profil_type: Optional[str] = None
    date_creation: datetime
    
    class Config:
        populate_by_name = True


class PasswordUpdate(BaseModel):
    """Mise à jour du mot de passe"""
    ancien_motdepasse: str = Field(..., min_length=8, max_length=72)
    nouveau_motdepasse: str = Field(..., min_length=8, max_length=72)
    confirmation: str


class TokenPayload(BaseModel):
    """Payload du JWT (ce qui est décodé)"""
    sub: str  # user_id
    email: str
    role: UserRole
    permissions: list = []
    exp: Optional[int] = None
