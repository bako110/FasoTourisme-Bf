# 🔐 Configuration RBAC - Système de Gestion des Rôles

## Vue d'ensemble

L'application Tourisme Burkina Faso utilise un système **Role-Based Access Control (RBAC)** sophistiqué avec **5 rôles distincts** et une gestion fine des permissions.

---

## 🎭 Les 5 Rôles Principaux

### 1. 👑 **ADMIN** (Administrateur)
**Accès:** Vue globale complète du système

**Permissions:**
- ✅ Créer, modifier, supprimer TOUT le contenu (destinations, hôtels, activités, etc.)
- ✅ Gérer tous les utilisateurs (voir, modifier rôles, désactiver)
- ✅ Vérifier et publier les profils PROVIDERS
- ✅ Modérer tout le contenu (reviews, stories, comments)
- ✅ Accès aux statistiques et analytics
- ✅ Accès aux routes `/admin/*` (vues globales)
- ✅ Voir les réservations de tous les utilisateurs
- ✅ Signaler/modérer les contenus inappropriés

**Routes spécifiques ADMIN:**
```
POST   /api/v1/destinations/         # Créer une destination
PUT    /api/v1/destinations/{id}     # Modifier toute destination
DELETE /api/v1/destinations/{id}     # Supprimer toute destination
GET    /api/v1/destinations/admin/all       # Vue globale
GET    /api/v1/destinations/admin/stats     # Statistiques

POST   /api/v1/auth/admin/users/{id}/role   # Changer rôle utilisateur
DELETE /api/v1/auth/admin/users/{id}        # Désactiver utilisateur

PUT    /api/v1/providers/admin/{id}/verify  # Vérifier provider
PUT    /api/v1/providers/admin/{id}/publish # Publier provider
GET    /api/v1/providers/admin/pending      # Providers en attente

GET    /api/v1/bookings/analytics            # Analytics réservations
GET    /api/v1/reviews/admin/all             # Tous les avis
POST   /api/v1/reviews/admin/{id}/flag       # Signaler avis inapproprié
```

---

### 2. 🏨 **PROVIDER** (Prestataire: Artisan + Restaurant)
**Accès:** Peut ajouter et gérer son propre contenu professionnel

**Permissions:**
- ✅ S'inscrire via `/auth/register`
- ✅ Créer son profil Provider (artisan OU restaurant)
- ✅ Créer et gérer ses propres hôtels
- ✅ Créer et gérer ses propres événements
- ✅ Créer et gérer ses propres services
- ✅ Voir ses propres réservations
- ✅ Répondre aux reviews concernant ses services
- ❌ Modifier le contenu des autres providers
- ❌ Accès aux vues globales admin

**Workflow PROVIDER:**
1. Inscription → Compte créé avec `role=PROVIDER`
2. Création profil → `POST /providers/` (statut: pending_verification)
3. Admin vérifie → `PUT /providers/admin/{id}/verify`
4. Profil publié → `PUT /providers/admin/{id}/publish`
5. Provider peut maintenant ajouter son contenu (hôtels, événements)

**Routes PROVIDER:**
```
# Profil Provider
POST   /api/v1/providers/              # Créer son profil
GET    /api/v1/providers/me/providers  # Voir son profil
PUT    /api/v1/providers/{id}          # Modifier SON profil uniquement
DELETE /api/v1/providers/{id}          # Supprimer SON profil uniquement

# Contenu Provider
POST   /api/v1/hotels/                 # Créer un hôtel
GET    /api/v1/hotels/me/hotels        # Ses hôtels
PUT    /api/v1/hotels/{id}             # Modifier SON hôtel uniquement
DELETE /api/v1/hotels/{id}             # Supprimer SON hôtel uniquement

POST   /api/v1/events/                 # Créer un événement
GET    /api/v1/events/me/events        # Ses événements
PUT    /api/v1/events/{id}             # Modifier SON événement uniquement
DELETE /api/v1/events/{id}             # Supprimer SON événement uniquement

# Réservations
GET    /api/v1/bookings/               # Voir ses réservations uniquement
GET    /api/v1/bookings/{id}           # Voir SA réservation uniquement
```

---

### 3. 🎒 **GUIDE** (Guide Touristique)
**Accès:** Peut créer et gérer son profil de guide et organiser des activités

**Permissions:**
- ✅ S'inscrire via `/auth/register`
- ✅ Créer son profil Guide avec spécialisations
- ✅ Créer et gérer ses propres activités touristiques
- ✅ Créer et gérer ses propres événements/tours
- ✅ Voir les réservations liées à ses services
- ✅ Répondre aux reviews
- ❌ Modifier les profils d'autres guides
- ❌ Voir toutes les réservations

**Routes GUIDE:**
```
# Profil Guide
POST   /api/v1/guides/                 # Créer son profil guide
GET    /api/v1/guides/{id}             # Voir un profil guide
PUT    /api/v1/guides/{id}             # Modifier SON profil uniquement
DELETE /api/v1/guides/{id}             # Supprimer SON profil uniquement

# Activités Guide
POST   /api/v1/events/                 # Créer un événement/tour
GET    /api/v1/events/me/events        # Ses événements
PUT    /api/v1/events/{id}             # Modifier SON événement uniquement
DELETE /api/v1/events/{id}             # Supprimer SON événement uniquement
```

---

### 4. 🧳 **TOURIST** (Touriste)
**Accès:** Consommateur de contenu, peut réserver et partager son expérience

**Permissions:**
- ✅ S'inscrire via `/auth/register`
- ✅ Consulter tout le contenu publié (destinations, hôtels, activités, guides, providers)
- ✅ Créer des réservations
- ✅ Gérer ses propres réservations (annuler, modifier)
- ✅ Créer des reviews/avis
- ✅ Créer des stories/histoires de voyage
- ✅ Modifier/supprimer ses propres reviews et stories
- ❌ Créer du contenu professionnel (hôtels, activités)
- ❌ Voir les réservations des autres

**Routes TOURIST:**
```
# Consultation
GET    /api/v1/destinations/           # Voir destinations
GET    /api/v1/hotels/                 # Voir hôtels
GET    /api/v1/activities/             # Voir activités
GET    /api/v1/guides/                 # Voir guides
GET    /api/v1/providers/              # Voir providers

# Réservations
POST   /api/v1/bookings/               # Créer une réservation
GET    /api/v1/bookings/               # Voir SES réservations
PUT    /api/v1/bookings/{id}           # Modifier SA réservation
POST   /api/v1/bookings/{id}/cancel    # Annuler SA réservation

# Reviews & Stories
POST   /api/v1/reviews/                # Créer un avis
PUT    /api/v1/reviews/{id}            # Modifier SON avis uniquement
DELETE /api/v1/reviews/{id}            # Supprimer SON avis uniquement
POST   /api/v1/reviews/{id}/helpful    # Marquer avis utile

POST   /api/v1/stories/                # Créer une histoire
PUT    /api/v1/stories/{id}            # Modifier SON histoire uniquement
DELETE /api/v1/stories/{id}            # Supprimer SON histoire uniquement
```

---

### 5. 👮 **MODERATOR** (Modérateur)
**Accès:** Modération du contenu utilisateur

**Permissions:**
- ✅ Voir tout le contenu
- ✅ Modérer les reviews (approuver, rejeter, supprimer)
- ✅ Modérer les stories (approuver, rejeter, supprimer)
- ✅ Signaler du contenu inapproprié
- ✅ Voir les rapports de modération
- ❌ Modifier le contenu système (destinations, hôtels)
- ❌ Gérer les utilisateurs (rôles, désactivation)

**Routes MODERATOR:**
```
PUT    /api/v1/reviews/{id}            # Modifier tout avis
DELETE /api/v1/reviews/{id}            # Supprimer tout avis
POST   /api/v1/reviews/admin/{id}/flag # Signaler avis

PUT    /api/v1/stories/{id}            # Modifier toute histoire
DELETE /api/v1/stories/{id}            # Supprimer toute histoire
POST   /api/v1/stories/admin/{id}/flag # Signaler histoire
```

---

## 🔒 Mécanismes de Sécurité

### 1. **Authentification JWT**
- Token Bearer avec expiration 24h
- Secret key configurable dans `.env`
- Hash bcrypt pour les mots de passe

```python
# Exemple d'utilisation dans les routes
@router.get("/protected")
async def protected_route(current_user: TokenPayload = Depends(get_current_user)):
    # current_user contient: sub (user_id), email, role, permissions
    pass
```

### 2. **Vérification des Rôles**
```python
# Require un rôle spécifique
@router.post("/admin-only")
async def admin_route(admin: TokenPayload = Depends(require_admin)):
    pass

# Require un des rôles spécifiés
from app.core.permissions import Permission
Permission.check_any_role(current_user, [UserRole.PROVIDER, UserRole.GUIDE])
```

### 3. **Vérification de Propriété**
```python
from app.core.permissions import OwnershipCheck

# Vérifier que l'utilisateur est propriétaire de la ressource
OwnershipCheck.ensure_ownership(current_user, resource.owner_id, "hôtel")
# Lance HTTPException 403 si non propriétaire et non admin
```

### 4. **Validation des Mots de Passe**
Requis pour l'inscription:
- Minimum 8 caractères
- Au moins 1 majuscule
- Au moins 1 minuscule  
- Au moins 1 chiffre
- Au moins 1 caractère spécial (@$!%*?&)

---

## 📊 Matrice des Permissions

| Action | ADMIN | PROVIDER | GUIDE | TOURIST | MODERATOR |
|--------|-------|----------|-------|---------|-----------|
| **Créer Destination** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Créer Hôtel** | ✅ | ✅ (son propre) | ❌ | ❌ | ❌ |
| **Créer Activité** | ✅ | ❌ | ✅ (son propre) | ❌ | ❌ |
| **Créer Événement** | ✅ | ✅ (son propre) | ✅ (son propre) | ❌ | ❌ |
| **Créer Profil Provider** | ✅ | ✅ | ❌ | ❌ | ❌ |
| **Créer Profil Guide** | ✅ | ❌ | ✅ | ❌ | ❌ |
| **Créer Réservation** | ✅ | ❌ | ❌ | ✅ | ❌ |
| **Créer Review** | ✅ | ❌ | ❌ | ✅ | ❌ |
| **Créer Story** | ✅ | ❌ | ❌ | ✅ | ❌ |
| **Voir Tout le Contenu** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Modifier Contenu Autres** | ✅ | ❌ | ❌ | ❌ | ✅ (reviews/stories) |
| **Vérifier Providers** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Gérer Utilisateurs** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Voir Analytics** | ✅ | ❌ | ❌ | ❌ | ❌ |

---

## 🚀 Flux d'Inscription par Rôle

### Provider (Artisan/Restaurant)
```
1. POST /auth/register 
   Body: { email, motdepasse, nom_complet, profil_type: "artisan" }
   → Compte créé avec role=PROVIDER

2. POST /auth/login
   → Obtenir token JWT

3. POST /providers/
   Body: { type_service: "ARTISAN", nom_entreprise, ... }
   → Profil créé (verified=False, publie=False)

4. Admin vérifie:
   PUT /providers/admin/{id}/verify { verified: true }
   PUT /providers/admin/{id}/publish { published: true }

5. Provider peut maintenant créer du contenu:
   POST /hotels/ (avec owner_id automatique)
   POST /events/ (avec organizer_id automatique)
```

### Guide
```
1. POST /auth/register
   Body: { email, motdepasse, nom_complet, profil_type: "guide" }
   → Compte créé avec role=GUIDE

2. POST /auth/login
   → Obtenir token JWT

3. POST /guides/
   Body: { nom, langues_parlees, specialites, ... }
   → Profil guide créé

4. Guide peut créer des événements/tours:
   POST /events/ (avec organizer_id automatique)
```

### Tourist
```
1. POST /auth/register
   Body: { email, motdepasse, nom_complet }
   → Compte créé avec role=TOURIST

2. POST /auth/login
   → Obtenir token JWT

3. Utilisation:
   GET /destinations/ → Voir destinations
   POST /bookings/ → Réserver
   POST /reviews/ → Laisser avis
   POST /stories/ → Partager expérience
```

---

## 🛡️ Sécurité et Bonnes Pratiques

### Configuration Requise
```bash
# .env
SECRET_KEY="votre-cle-secrete-ultra-securisee-256-bits-minimum"
MONGODB_URL="mongodb://localhost:27017"
DATABASE_NAME="tourisme_burkina"
```

### Headers d'Authentification
```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Gestion des Erreurs
```python
403 Forbidden → Pas les permissions nécessaires
401 Unauthorized → Token invalide ou expiré
404 Not Found → Ressource inexistante
500 Internal Server Error → Erreur serveur
```

---

## 📝 Fichiers Clés

```
app/
├── core/
│   ├── security.py           # JWT, hash, get_current_user, require_admin
│   ├── permissions.py        # Permission, OwnershipCheck, RolePermissions
│   └── config.py             # SECRET_KEY, settings
├── models/
│   ├── user.py               # UserRole enum (5 rôles)
│   └── provider.py           # Provider unified model
├── schemas/
│   └── auth.py               # TokenRequest, UserRegister, TokenPayload
├── services/
│   ├── user_service.py       # register_user, authenticate_user
│   └── provider_service.py   # create_provider, verify_provider
└── api/v1/routes/
    ├── auth.py               # /register, /login, /me, /admin/users
    ├── providers.py          # Provider CRUD avec ownership
    ├── destinations.py       # ADMIN create, tous read
    ├── guides.py             # GUIDE create son profil
    ├── hotels.py             # PROVIDER create ses hôtels
    ├── events.py             # PROVIDER/GUIDE create événements
    ├── activities.py         # ADMIN create, tous read
    ├── bookings.py           # TOURIST create/manage
    ├── reviews.py            # TOURIST create, MODERATOR moderate
    └── stories.py            # TOURIST create, MODERATOR moderate
```

---

## ✅ Résumé

Le système RBAC est **complet et dynamique** avec:
- ✅ **5 rôles distincts** avec permissions granulaires
- ✅ **Providers et Guides** peuvent ajouter leur propre contenu
- ✅ **Admins** ont vue globale et contrôle total
- ✅ **Tourists** peuvent réserver et partager expériences
- ✅ **Moderators** maintiennent la qualité du contenu
- ✅ **Ownership tracking** pour chaque ressource
- ✅ **JWT sécurisé** avec expiration
- ✅ **Routes `/me/*`** pour gérer son propre contenu
- ✅ **Routes `/admin/*`** pour vues globales admin

L'application est **bien organisée**, **sécurisée** et **scalable** ! 🚀
