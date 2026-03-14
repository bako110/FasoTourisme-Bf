# 🚀 Déploiement Rapide sur Fly.io

## Commandes Rapides

```bash
# 1. Installer Fly CLI (Windows PowerShell)
iwr https://fly.io/install.ps1 -useb | iex

# 2. Se connecter
fly auth login

# 3. Lancer l'application (Fly détecte automatiquement fly.toml)
fly launch

# 4. Configurer MongoDB (utilisez MongoDB Atlas - gratuit)
# Obtenez votre URL depuis https://www.mongodb.com/cloud/atlas
fly secrets set MONGODB_URL="mongodb+srv://user:pass@cluster.mongodb.net/tourisme_burkina"

# 5. Configurer la clé secrète JWT
fly secrets set SECRET_KEY="$(openssl rand -hex 32)"

# 6. Configurer CORS (ajoutez vos domaines)
fly secrets set ALLOWED_ORIGINS="https://votre-app.com"

# 7. Déployer
fly deploy

# 8. Ouvrir l'app
fly open /api/docs
```

## Vérification Rapide

```bash
# Statut
fly status

# Logs
fly logs

# Accès SSH
fly ssh console
```

## URLs de votre API

- API Docs: https://tourisme-burkina-api.fly.dev/api/docs
- Health Check: https://tourisme-burkina-api.fly.dev/health
- API: https://tourisme-burkina-api.fly.dev/api/v1/

## En cas de problème

```bash
# Voir les logs en temps réel
fly logs -f

# Redémarrer
fly apps restart

# Revenir à la version précédente
fly releases rollback
```

Consultez [DEPLOYMENT.md](DEPLOYMENT.md) pour le guide complet.
