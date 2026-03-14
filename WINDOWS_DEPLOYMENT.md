# 🪟 Guide Fly.io pour Windows

## Installation (PowerShell en tant qu'Administrateur)

```powershell
# Installer Fly CLI
iwr https://fly.io/install.ps1 -useb | iex

# Redémarrer le terminal après l'installation
# Vérifier l'installation
fly version
```

## Authentification

```powershell
# Se connecter à Fly.io
fly auth login
```

## MongoDB Atlas (Recommandé pour Windows)

1. Créez un compte sur https://www.mongodb.com/cloud/atlas
2. Créez un cluster gratuit (M0)
3. Ajoutez un utilisateur de base de données
4. Autorisez toutes les IPs: 0.0.0.0/0
5. Copiez l'URL de connexion

## Déploiement

```powershell
# Naviguer vers le dossier backend
cd C:\Users\PC1\projetSah\perso\Tourisme\backend

# Créer l'app Fly.io (première fois seulement)
fly launch --name tourisme-burkina-api --region cdg

# Configurer les secrets
fly secrets set MONGODB_URL="mongodb+srv://user:password@cluster.mongodb.net/tourisme_burkina?retryWrites=true&w=majority"

# Générer une clé secrète (PowerShell)
$secret = -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 64 | % {[char]$_})
fly secrets set SECRET_KEY="$secret"

# CORS (ajoutez vos domaines)
fly secrets set ALLOWED_ORIGINS="https://votre-domaine.com,https://www.votre-domaine.com"

# Déployer
fly deploy

# Ouvrir dans le navigateur
fly open /api/docs
```

## Commandes Utiles

```powershell
# Voir les logs
fly logs

# Logs en direct
fly logs -f

# Statut de l'application
fly status

# Tableau de bord
fly dashboard

# Redémarrer
fly apps restart tourisme-burkina-api

# SSH dans le container
fly ssh console

# Voir les secrets configurés (valeurs masquées)
fly secrets list

# Scaler l'application
fly scale memory 512  # Augmenter la mémoire à 512MB
fly scale count 2     # 2 machines

# Régions disponibles
fly regions list

# Ajouter une région
fly regions add jnb  # Johannesburg, Afrique du Sud
```

## Dépannage

### "fly: command not found"
- Relancez PowerShell
- Ou ajoutez manuellement au PATH: `$env:Path += ";$env:USERPROFILE\.fly\bin"`

### Erreur de connexion MongoDB
```powershell
# Testez depuis le container
fly ssh console
# Puis dans le container:
python -c "from pymongo import MongoClient; client = MongoClient('VOTRE_URL'); print(client.server_info())"
```

### Port 8080 déjà utilisé localement
```powershell
# Trouver le processus
netstat -ano | findstr :8080
# Tuer le processus (remplacez PID par le numéro trouvé)
taskkill /PID [PID] /F
```

## Test Local avec Docker (Optionnel)

```powershell
# Construire l'image
docker build -t tourisme-api .

# Lancer le container
docker run -p 8080:8080 -e MONGODB_URL="votre_url" -e SECRET_KEY="test" tourisme-api

# Tester
curl http://localhost:8080/health
```

## Monitoring

```powershell
# Métriques
fly dashboard

# VM info
fly vm status

# Releases
fly releases
```

## Nettoyage

```powershell
# Supprimer l'application (⚠️ ATTENTION!)
fly apps destroy tourisme-burkina-api
```

## Variables d'environnement pour Windows (Dev local)

Créez un fichier `.env` à partir de `.env.example`:

```powershell
Copy-Item .env.example .env
# Éditez .env avec vos valeurs
notepad .env
```

## Structure des fichiers créés

```
backend/
├── Dockerfile              ← Configuration Docker
├── .dockerignore          ← Fichiers à exclure du build
├── fly.toml               ← Configuration Fly.io
├── DEPLOYMENT.md          ← Guide complet
├── DEPLOY_QUICK_START.md  ← Commandes rapides
└── WINDOWS_DEPLOYMENT.md  ← Ce fichier (Windows-specific)
```

## URLs finales

Remplacez `tourisme-burkina-api` par votre nom d'app:

- API: `https://tourisme-burkina-api.fly.dev`
- Docs: `https://tourisme-burkina-api.fly.dev/api/docs`
- Health: `https://tourisme-burkina-api.fly.dev/health`

## Support

- Documentation Fly.io: https://fly.io/docs/
- Community: https://community.fly.io/
- Status: https://status.fly.io/
